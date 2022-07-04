from datetime import datetime
import json

from sqlalchemy import Column, Text, Integer, DateTime
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import types

from proj_stat.database import Base


class Hand:
    def get_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    def get_json(self):
        return json.dumps(self.get_dict())
    def __repl__(self):
        return str(self.get_dict())


class Challenge(Base, Hand):
    __tablename__ = "Challenge"
    challenge_id = Column(Text, primary_key=True, unique=True, nullable=False)
    content = Column(Text)
    create_time = Column(Text, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    title = Column(Text)
    metrics = Column(Text)


class Result(Base, Hand):
    __tablename__ = "Result"
    result_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_name = Column(Text)
    submission_id = Column(Text)
    challenge_id = Column(Text, ForeignKey("Challenge.challenge_id"))
    result_object = Column(Text)
