from datetime import datetime

from sqlalchemy import Column, Text, Integer, DateTime
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

from evaluate_api.database import Base


challenge_metric_link = Table('challenge_metric_link',
                              Base.metadata,
                              Column('challenge_id', Text, ForeignKey('Challenge.challenge_id')),
                              Column('metric_id', Integer, ForeignKey('Metric.metric_id'))
                              )


class Challenge(Base):
    __tablename__ = "Challenge"
    challenge_id = Column(Text, primary_key=True, unique=True, nullable=False)
    content = Column(Text)
    create_time = Column(DateTime, default=datetime.now())
    title = Column(Text)
    metrics = relationship("Metric", secondary=challenge_metric_link)

    def __repr__(self):
        return str(self.get_dict())

    def get_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class Metric(Base):
    __tablename__ = "Metric"
    metric_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    metric_name = Column(Text, unique=True)

    def __repr__(self):
        return str(self.get_dict())

    def get_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


# result_metric_link = Table('result_metric_link',
#                            Base.metadata,
#                            Column('result_id', Integer, ForeignKey('Result.result_id')),
#                            Column('metric_id', Integer, ForeignKey('Metric.metric_id')),
#                            Column('metric_score', Integer),
#                            )
#
#
#
# class Result(Base):
    # __tablename__ = "Result"
    # result_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    # user_name = Column(Text)
    # submission_id = Column(Text)
    # submission_time = Column(DateTime, default=datetime.now())
    #
    # challenge_id = Column(Text, ForeignKey("Challenge.challenge_id"))
    # metrics = relationship("Metric", secondary=result_metric_link)
