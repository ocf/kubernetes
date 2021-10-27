import pytest

from ocfkube.utils.json import delve, shelve


class TestDelve:
    def test_basic_functionality(self):
        val = object()
        obj = {"a": {"b": {"c": val}, "d": True}}
        assert delve(obj, ("a", "b", "c")) is val

    def test_returns_none_on_nonexistent_key(self):
        obj = {"a": {"b": {"c": "foo"}, "d": True}}
        assert delve(obj, ("a", "b", "nonexistent")) is None


class TestShelve:
    def test_basic_functionality(self):
        obj = {"a": {"b": {"c": "foo"}, "d": True}}
        expected = {"a": {"b": {"c": "bar"}, "d": True}}
        assert shelve(obj, ("a", "b", "c"), "bar") == expected
        assert obj == expected

    def test_create_key(self):
        obj = {"a": {"c": "d"}}
        expected = {"a": {"c": "d", "foo": "bar"}}
        assert shelve(obj, ("a", "foo"), "bar") == expected
        assert obj == expected

    def test_parent_creation(self):
        obj = {}
        expected = {"a": {"b": {"c": "bar"}}}
        assert shelve(obj, ("a", "b", "c"), "bar", create_parents=True) == expected
        assert obj == expected

    def test_missing_segment(self):
        obj = {"a": {"c": "d"}}
        key = "foo"
        with pytest.raises(KeyError, match=key):
            shelve(obj, ("a", key, "junk"), "junk")

    def test_empty_path(self):
        obj = {}
        expected = "foo"
        assert shelve(obj, [], expected) == expected
