from user import User


class Admin(User):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
