class Account:
    def __init__(self):
        self.id = None
        self.friends_count = None
        self.spammed = False
        self.duplicate = False
        self.works = True
        self.phone_number = False
    def __str__(self) -> str:
        return f"{self.id} {self.friends_count} {self.spammed} {self.duplicate} {self.works} {self.phone_number}"