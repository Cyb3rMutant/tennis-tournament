class Prize(object):
    def __init__(self, amount: int) -> None:
        self.__amount: int = amount

    def get_amount(self) -> int:
        return self.__amount

    def set_amount(self, amount: int) -> None:
        self.__amount = amount
