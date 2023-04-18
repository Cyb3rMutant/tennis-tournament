class Prize(object):
    def __init__(self, amount: int, currency: str) -> None:
        self.__amount: int = amount
        self.__currency: int = currency

    def get_amount(self) -> int:
        return self.__amount

    def get_currency(self) -> int:
        return self.__currency
