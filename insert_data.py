import json
import os
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import select
from evaluate_api.model import Challenge, Result


def load_json(path: str):
    with open(path, 'r') as file:
        return json.load(file)


def load_text(path: str):
    with open(path, 'r') as file:
        return file.read()


def load_challenges_to_db(session, sample_dir: str = r"./sample_data_2"):
    # search_dir = r"./sample_data_2/challenges"
    search_dir = os.path.join(sample_dir, "challenges")

    for child_dir in os.listdir(search_dir):
        path = os.path.join(search_dir, child_dir)
        metadata_path = os.path.join(path, "metadata.json")
        content_path = os.path.join(path, "content.md")

        challenge = Challenge()

        metadata = load_json(metadata_path)
        metadata["content"] = load_text(content_path)

        ## 데이터에 오타있음...
        try:
            challenge.challenge_id = metadata["challenge_id"]
        except Exception:
            challenge.challenge_id = metadata["challange_id"]
        challenge.content = metadata["content"]
        # challenge.create_time = datetime.strptime(metadata["create_time"], "%Y-%m-%d %H:%M:%S")
        challenge.create_time = metadata["create_time"]
        challenge.title = metadata["title"]
        challenge.metrics = json.dumps(metadata["metrics"])

        # for metric_name in metadata["metrics"]:
        #     one = session.execute(select(Metric)).where(Metric.metric_name == metric_name)).fetchone()
        #     if one:
        #         challenge.metrics.append(one[0])
        #     else:
        #         metric = Metric()
        #         metric.metric_name = metric_name
        #         challenge.metrics.append(metric)
        session.add(challenge)
        session.commit()


def load_results_to_db(session, sample_dir: str = r"./sample_data_2"):
    search_dir = os.path.join(sample_dir, "challenges")

    for child_dir in os.listdir(search_dir):
        path = os.path.join(search_dir, child_dir)
        result_path = os.path.join(path, "submissions.json")
        metadata_path = os.path.join(path, "metadata.json")

        results = load_json(result_path)
        metadata = load_json(metadata_path)

        for submission_id, result_object in results.items():
            result = Result()
            result.user_name = "unknown"
            result.submission_id = submission_id
            result.result_object = json.dumps(result_object)
            try:
                result.challenge_id = metadata["challenge_id"]
            except Exception:
                result.challenge_id = metadata["challange_id"]
            session.add(result)
            session.commit()
