import datetime


class Todo():
    def __init__(self, id: int, text: str, author: str):
        self.id = id
        self.text = text
        self.author = author
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"Id: {self.id}, Author: {self.author}, Text: {self.text}, Created at: {self.created_at}"
