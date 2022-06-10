from sqlalchemy import select

from evaluate_api.database import engine, Base, db_session
from evaluate_api.model import Challenge, Result
from insert_data import load_challenges_to_db, load_results_to_db


def test_db_create():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_load_challenge():
    load_challenges_to_db(db_session)
    challenges = db_session.execute(select(Challenge)).fetchone()
    assert challenges[0] is not None


def test_load_results():
    load_results_to_db(db_session)
    results = db_session.execute(select(Result)).fetchone()
    assert results[0] is not None
