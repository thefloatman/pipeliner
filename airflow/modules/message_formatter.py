import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    _id: str
    data: dict

    def as_dict(self):
        return self.__dict__


class MessageFormatter:
    def __init__(self):
        self.id_regex = "[^0-9a-zA-Z_-]+"


    def format_entry(self, entry):
        return Message(
            self.construct_id(entry['tweet']),
            entry,
        ).as_dict()

    def construct_id(self, title):
        return re.sub(self.id_regex, "", title).lower()
