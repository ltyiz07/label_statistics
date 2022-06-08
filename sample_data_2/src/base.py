import hashlib
import random
import time


def get_metric(code, metrics):
    """
    {code}에 따라 deterministic하게 metric을 반환해주는 함수
    실제 채점과 유사하도록 {code}에 따라 1~6초의 딜레이가 걸립니다.

    Args:
        code(str): 코드 / 실제로 eval되지는 않음
        metrics(List[str]): 반환해야 할 metric 목록

    Returns(Dict[str, int]): 각 metric별로 0~100사이의 난수를 가지는 dict
    """
    hash_ = hashlib.sha256()
    hash_.update(code.encode())

    random.seed(hash_.digest())
    time.sleep(random.random() * 5 + 1)
    return {k: random.randint(0, 100) for k in metrics}
