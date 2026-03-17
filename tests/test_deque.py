import pytest

from pure_python_ds.linear.deque import Deque


def test_deque_append():
    d = Deque()
    d.append(1)
    d.append(2)
    assert len(d) == 2
    assert d.peek() == 2
    assert d.peekleft() == 1


def test_deque_appendleft():
    d = Deque()
    d.appendleft(1)
    d.appendleft(2)
    assert len(d) == 2
    assert d.peek() == 1
    assert d.peekleft() == 2


def test_deque_pop():
    d = Deque([1, 2, 3])
    assert d.pop() == 3
    assert len(d) == 2
    assert d.pop() == 2
    assert d.pop() == 1
    assert d.is_empty()

    with pytest.raises(IndexError):
        d.pop()


def test_deque_popleft():
    d = Deque([1, 2, 3])
    assert d.popleft() == 1
    assert len(d) == 2
    assert d.popleft() == 2
    assert d.popleft() == 3
    assert d.is_empty()

    with pytest.raises(IndexError):
        d.popleft()

def test_deque_clear():
    d = Deque([1, 2, 3])
    d.clear()
    assert len(d) == 0
    assert d.is_empty()
