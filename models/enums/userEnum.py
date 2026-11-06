import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


RoleEnum = UserRole

