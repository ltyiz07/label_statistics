from annotation_statistics.services.base import get_metric, get_hash_from


def test_get_metric():
    result_1 = get_metric("hello world", ["first", "second", "third"], is_test=True)
    print("test result *********************************************:")
    print(result_1)
    result_2 = get_metric("hello world", ["first", "second", "third"], is_test=False)
    result_3 = get_metric("this is it", ["first", "second", "third"], is_test=True)

    assert result_1 == result_2
    assert result_1 != result_3


def test_base_service():
    h_1 = get_hash_from("ehdkfjektjw2", b"this is binary content")
    h_2 = get_hash_from("ehdkfjektjw2", "this is binary content")
    assert h_1 == h_2