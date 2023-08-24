class Parser:
    @staticmethod
    def parse(data: str) -> tuple:
        name, *args = list(filter(lambda x: x != "", data.split()))
        return name, *args
