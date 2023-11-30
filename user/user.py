class User:
    def __init__(self, record):
        self.id = record[0]
        self.email = record[1]
        self.name = record[2]
        self.password = record[3]