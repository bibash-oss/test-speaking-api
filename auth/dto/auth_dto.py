class LoginUserDTO:
    def __init__(self, email: str, password: str):
        self.email = email.strip().lower() if email else ""
        self.password = password or ""

    @staticmethod
    def from_dict(data: dict):
        if not data:
            raise ValueError("Payload cannot be empty")
        email = data.get("email", "").strip()
        password = data.get("password", "")
        if not email or not password:
            raise ValueError("Fields 'email' and 'password' are required")
        return LoginUserDTO(email=email, password=password)

