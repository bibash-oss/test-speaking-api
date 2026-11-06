import os
import unittest
from flask import jsonify

os.environ["DATABASE"] = "sqlite:///:memory:"
os.environ["GOOGLE_API_KEY"] = "mock_api_key_for_testing"

from app import app
from models import db, Organization, UserRole, RoleEnum
from common.auth import generate_token, require_auth, require_role, require_super_admin
from auth.service.auth_service import seed_default_organization, seed_super_admin


class TestAuthAndSeeder(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_role_enum_values(self):
        """Test UserRole / RoleEnum values and types."""
        self.assertEqual(UserRole.ADMIN, "admin")
        self.assertEqual(UserRole.ADMIN.value, "admin")
        self.assertEqual(UserRole.SUPER_ADMIN, "super_admin")
        self.assertEqual(UserRole.SUPER_ADMIN.value, "super_admin")
        self.assertIs(UserRole, RoleEnum)

    def test_organization_role_assignment_and_properties(self):
        """Test Organization role persistence, properties, and to_dict serialization."""
        with self.app.app_context():
            org_admin = Organization(
                name="Admin Org",
                email="admin@test.com",
                role=UserRole.ADMIN,
            )
            org_admin.set_password("pass123")

            org_super = Organization(
                name="Super Org",
                email="super@test.com",
                role=UserRole.SUPER_ADMIN,
            )
            org_super.set_password("pass123")

            db.session.add_all([org_admin, org_super])
            db.session.commit()

            fetched_admin = Organization.query.filter_by(email="admin@test.com").first()
            fetched_super = Organization.query.filter_by(email="super@test.com").first()

            self.assertEqual(fetched_admin.role, UserRole.ADMIN)
            self.assertFalse(fetched_admin.is_super_admin)
            self.assertTrue(fetched_admin.is_admin)
            self.assertEqual(fetched_admin.to_dict()["role"], "admin")

            self.assertEqual(fetched_super.role, UserRole.SUPER_ADMIN)
            self.assertTrue(fetched_super.is_super_admin)
            self.assertTrue(fetched_super.is_admin)
            self.assertEqual(fetched_super.to_dict()["role"], "super_admin")

    def test_seed_super_admin_creates_new_user(self):
        """Test seed_super_admin successfully creates a new super admin."""
        with self.app.app_context():
            user = seed_super_admin(
                name="Main Super Admin",
                email="root@ktmbees.com",
                password="supersecretpassword",
            )
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "root@ktmbees.com")
            self.assertEqual(user.role, UserRole.SUPER_ADMIN)
            self.assertTrue(user.check_password("supersecretpassword"))
            self.assertTrue(user.is_active)

    def test_seed_super_admin_idempotent_and_updates_role(self):
        """Test seed_super_admin handles existing users and promotes non-super admins."""
        with self.app.app_context():
            # First create a normal admin
            existing = Organization(
                name="Existing User",
                email="upgrade@ktmbees.com",
                role=UserRole.ADMIN,
                is_active=True,
            )
            existing.set_password("initialpass")
            db.session.add(existing)
            db.session.commit()

            # Seed super admin with the same email
            promoted = seed_super_admin(
                name="Upgraded Admin",
                email="upgrade@ktmbees.com",
                password="newpassword",
            )
            self.assertEqual(promoted.id, existing.id)
            self.assertEqual(promoted.role, UserRole.SUPER_ADMIN)
            self.assertTrue(promoted.check_password("newpassword"))

            # Calling again should be idempotent without error
            rechecked = seed_super_admin(email="upgrade@ktmbees.com")
            self.assertEqual(rechecked.role, UserRole.SUPER_ADMIN)

    def test_login_returns_super_admin_role(self):
        """Test login endpoint returns 'super_admin' string in role field."""
        with self.app.app_context():
            seed_super_admin(
                name="Super Admin Login Test",
                email="super_login@ktmbees.com",
                password="loginpass123",
            )

        resp = self.client.post("/api/auth/login", json={
            "email": "super_login@ktmbees.com",
            "password": "loginpass123",
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("token", data)
        self.assertEqual(data["role"], "super_admin")

    def test_require_super_admin_decorator(self):
        """Test require_super_admin blocks regular admin and allows super_admin."""
        with self.app.app_context():
            admin_user = Organization(
                name="Admin User",
                email="standard_admin@test.com",
                role=UserRole.ADMIN,
                is_active=True,
            )
            admin_user.set_password("pass")

            super_user = Organization(
                name="Super User",
                email="super_user@test.com",
                role=UserRole.SUPER_ADMIN,
                is_active=True,
            )
            super_user.set_password("pass")

            db.session.add_all([admin_user, super_user])
            db.session.commit()

            admin_token = generate_token(admin_user)
            super_token = generate_token(super_user)

        @require_super_admin
        def protected_view():
            return jsonify({"status": "granted"}), 200

        # 1. Attempt with standard admin token -> 403 Forbidden
        with self.app.test_request_context(headers={"Authorization": f"Bearer {admin_token}"}):
            resp = protected_view()
            if isinstance(resp, tuple):
                response_obj, status_code = resp
            else:
                response_obj, status_code = resp, resp.status_code
            self.assertEqual(status_code, 403)
            self.assertIn("Insufficient", response_obj.get_json()["error"])

        # 2. Attempt with super admin token -> 200 OK
        with self.app.test_request_context(headers={"Authorization": f"Bearer {super_token}"}):
            resp = protected_view()
            if isinstance(resp, tuple):
                response_obj, status_code = resp
            else:
                response_obj, status_code = resp, resp.status_code
            self.assertEqual(status_code, 200)
            self.assertEqual(response_obj.get_json()["status"], "granted")


if __name__ == "__main__":
    unittest.main()
