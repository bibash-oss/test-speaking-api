import os
from models import db
from models.organizations import Organization
from models.enums.userEnum import UserRole
from common.auth import generate_token


def login_user(email: str, password: str):
    """
    Authenticate organization/admin credentials.
    Returns (token, role, org_dict) on success, or raises/returns None.
    """
    email_clean = email.strip().lower() if email else ""
    org = Organization.query.filter_by(email=email_clean).first()

    if not org or not org.check_password(password):
        return None, "Invalid email or password", 401

    if not org.is_active:
        return None, "Organization account has been deactivated", 403

    token = generate_token(org)
    role_val = org.role.value if hasattr(org.role, "value") else str(org.role)
    return {
        "token": token,
        "role": role_val,
        "organization": org.to_dict(),
    }, None, 200


def seed_default_organization():
    """Helper to initialize the default admin organization if none exists."""
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if not inspector.has_table("organizations"):
            return None

        if Organization.query.first() is None:
            admin_name = os.getenv("ADMIN_NAME", "Ktmbees")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@ktmbees.com").strip().lower()
            admin_password = os.getenv("ADMIN_PASSWORD", "!@ktm@#23int_erview")

            org = Organization(
                name=admin_name,
                email=admin_email,
                role=UserRole.ADMIN,
                is_active=True,
            )
            org.set_password(admin_password)
            db.session.add(org)
            db.session.commit()
            print(f" Initialized default organization: {admin_email} (role: {UserRole.ADMIN.value})")
            return org
    except Exception as e:
        print(f" Organization seed notice: {e}")
        db.session.rollback()
    return None


def seed_super_admin(name: str = None, email: str = None, password: str = None):
    """
    Helper to initialize or update the Super Admin user.
    Reads defaults from environment variables:
      SUPER_ADMIN_NAME (default: 'Super Admin')
      SUPER_ADMIN_EMAIL (default: 'superadmin@ktmbees.com')
      SUPER_ADMIN_PASSWORD (default: '!@ktm@#superadmin23')
    """
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if not inspector.has_table("organizations"):
            return None

        super_name = name or os.getenv("SUPER_ADMIN_NAME", "Super Admin")
        super_email = (email or os.getenv("SUPER_ADMIN_EMAIL", "superadmin@ktmbees.com")).strip().lower()
        super_password = password or os.getenv("SUPER_ADMIN_PASSWORD", "!@ktm@#superadmin23")

        existing_user = Organization.query.filter_by(email=super_email).first()

        if existing_user:
            updated = False
            current_role = existing_user.role.value if hasattr(existing_user.role, "value") else str(existing_user.role)
            if current_role != UserRole.SUPER_ADMIN.value:
                existing_user.role = UserRole.SUPER_ADMIN
                updated = True
            if not existing_user.is_active:
                existing_user.is_active = True
                updated = True
            if password:
                existing_user.set_password(super_password)
                updated = True
            if updated:
                db.session.commit()
                print(f" Updated account to Super Admin: {super_email} (role: {UserRole.SUPER_ADMIN.value})")
            else:
                print(f" Super Admin already exists and configured: {super_email}")
            return existing_user

        super_admin = Organization(
            name=super_name,
            email=super_email,
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )
        super_admin.set_password(super_password)
        db.session.add(super_admin)
        db.session.commit()
        print(f" Initialized Super Admin: {super_email} (role: {UserRole.SUPER_ADMIN.value})")
        return super_admin

    except Exception as e:
        print(f" Super admin seed notice: {e}")
        db.session.rollback()
        return None

