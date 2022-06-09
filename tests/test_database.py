import json

from sqlalchemy import select
from sqlalchemy.orm import Bundle

from evaluate_api.database import engine, Base, db_session
from evaluate_api.model import Challenge, Metric, Result
from insert_data import load_challenges_to_db, load_results_to_db

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

load_challenges_to_db(db_session)
load_results_to_db(db_session)


def test_get_challenges():
    result = db_session.execute(
        select(Challenge)
        .from_statement(
            select(Bundle("Challenge", Challenge.create_time, Challenge.title, Challenge.challenge_id))
        )
    )
    assert len(result.fetchall()) == 5


def test_get_challenge():
    result = db_session.execute(
        select(Challenge).where(Challenge.challenge_id == r"4l5qtrv84gup")
    ).fetchone()
    assert result[0].title == "Growing Hunter"

    result = db_session.execute(
        select(Challenge).where(Challenge.challenge_id == r"4whxst3yztaw")
    ).fetchone()
    assert result[0].title == "The Dwindling Streams"


def test_get_restul():
    result = db_session.execute(
        select(Result).where(Result.submission_id == r"00968776d971")
    ).fetchone()
    print(result[0])
    assert json.loads(result[0].result_object)["submission_time"] == "2019-12-04 06:01:33"
