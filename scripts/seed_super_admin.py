#!/usr/bin/env python3
"""
Seed script to create or update the Super Admin user in the database.

Usage:
    python scripts/seed_super_admin.py
    python scripts/seed_super_admin.py --email superadmin@example.com --password mysecret --name "Super Admin"
"""
import os
import sys
import argparse

# Add parent directory to sys.path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from auth.service.auth_service import seed_super_admin
from models import db, UserRole


def main():
    parser = argparse.ArgumentParser(description="Seed or update Super Admin user in the database.")
    parser.add_argument("--name", default=None, help="Full name of the super admin (defaults to SUPER_ADMIN_NAME env)")
    parser.add_argument("--email", default=None, help="Email of the super admin (defaults to SUPER_ADMIN_EMAIL env)")
    parser.add_argument("--password", default=None, help="Password of the super admin (defaults to SUPER_ADMIN_PASSWORD env)")
    args = parser.parse_args()

    with app.app_context():
        print("🌱 Seeding Super Admin user...")
        from models import db
        try:
            db.create_all()
        except Exception:
            pass

        user = seed_super_admin(name=args.name, email=args.email, password=args.password)
        if user:
            role_val = user.role.value if hasattr(user.role, "value") else str(user.role)
            print(f"✅ Success: Super Admin is '{user.name}' <{user.email}> with role '{role_val}'.")
            sys.exit(0)
        else:
            print("❌ Failed to seed Super Admin. Check logs and database connection.")
            sys.exit(1)


if __name__ == "__main__":
    main()
