import os
import uuid
from dotenv import load_dotenv

load_dotenv()

from app import app
from models import db
from models.organizations import Organization
from models.enums.userEnum import UserRole


def create_super_admin():
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass

        admin_email = os.getenv("SUPER_ADMIN_EMAIL", "superadmin@ktmbees.com").strip().lower()
        admin_password = os.getenv("SUPER_ADMIN_PASSWORD", "!@ktm@#superadmin23")
        admin_name = os.getenv("SUPER_ADMIN_NAME", "Super Admin")

        existing_admin = Organization.query.filter_by(email=admin_email).first()
        if existing_admin:
            current_role = existing_admin.role.value if hasattr(existing_admin.role, "value") else str(existing_admin.role)
            if current_role != UserRole.SUPER_ADMIN.value:
                existing_admin.role = UserRole.SUPER_ADMIN
                existing_admin.is_active = True
                db.session.commit()
                print(f"✅ Promoted existing account {admin_email} to Super Admin!")
                return
            print(f"⚠️ User with email {admin_email} is already Super Admin!")
            return

        new_admin = Organization(
            id=str(uuid.uuid4()),
            name=admin_name,
            email=admin_email,
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )
        new_admin.set_password(admin_password)

        try:
            db.session.add(new_admin)
            db.session.commit()
            print(f"✅ Successfully created Super Admin: {admin_email}")
            print(f"🔑 You can now log in with the password configured in .env.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Failed to create Super Admin: {e}")


if __name__ == "__main__":
    create_super_admin()
