class Location(object):
    def __init__(self, address_line_1: str, address_line_2: str, post_code: str, city: str, country: str) -> None:

        self.__address_line_1: str = address_line_1

        self.__address_line_2: str = address_line_2

        self.__post_code: str = post_code

        self.__city: str = city

        self.__country: str = country

    def get_address_line_1(self) -> str:
        return self.__address_line_1

    def get_address_line_2(self) -> str:
        return self.__address_line_2

    def get_post_code(self) -> str:
        return self.__post_code

    def get_city(self) -> str:
        return self.__city

    def get_country(self) -> str:
        return self.__country
