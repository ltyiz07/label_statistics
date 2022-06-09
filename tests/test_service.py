from evaluate_api.service.base import get_metric


def test_get_metric():
    result_1 = get_metric("hello world", ["first", "second", "third"], is_test=True)
    print("test result *********************************************:")
    print(result_1)
    result_2 = get_metric("hello world", ["first", "second", "third"], is_test=False)
    result_3 = get_metric("this is it", ["first", "second", "third"], is_test=True)

    assert result_1 == result_2
    assert result_1 != result_3
