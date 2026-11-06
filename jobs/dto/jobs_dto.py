class CreateJobDTO:
    def __init__(self, title: str, level: str, description: str, company_name: str = ""):
        self.title = title.strip() if title else ""
        self.level = level.strip() if level else "Junior"
        self.description = description.strip() if description else ""
        self.company_name = company_name.strip() if company_name else ""

    @staticmethod
    def from_dict(data: dict):
        if not data:
            raise ValueError("Payload cannot be empty")
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        if not title:
            raise ValueError("Field 'title' is required")
        if not description:
            raise ValueError("Field 'description' is required")

        return CreateJobDTO(
            title=title,
            level=data.get("level", "Junior"),
            description=description,
            company_name=data.get("company_name", ""),
        )

