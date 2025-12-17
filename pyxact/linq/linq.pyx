from typing import Any, Callable, TypeVar


_range = range
TS = TypeVar("TS")
TR = TypeVar("TR")
TF = TypeVar("TF")


class linq(list[TS]):
    """LINQ-like list extension class"""

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    @property
    def __is_empty(self) -> bool:
        return self.__len__() <= 0

    def any(self, pred: Callable[[TS], bool] | None = None) -> bool:
        if pred is None:
            return not self.__is_empty
        return [0 for e in self if pred(e)].__len__() > 0

    def count(self, pred: Callable[[TS], bool] | None = None) -> int:
        if pred is None:
            return self.__len__()
        return [0 for e in self if pred(e)].__len__()

    def where(self, pred: Callable[[TS], bool]) -> "linq[TS]":
        return linq([e for e in self if pred(e)])

    def select(self, func: Callable[[TS], TR]) -> "linq[TR]":
        return linq([func(e) for e in self])

    def find_index(self, pred: Callable[[TS], bool]) -> int:
        for i, e in enumerate(self):
            if pred(e):
                return i
        return -1

    def find(self, pred: Callable[[TS], bool]) -> TS | None:
        for e in self:
            if pred(e):
                return e
        return None

    def find_last(self, pred: Callable[[TS], bool]) -> TS | None:
        for e in self.__reversed__():
            if pred(e):
                return e
        return None

    def find_last_index(self, pred: Callable[[TS], bool]) -> int:
        for i, e in enumerate(self.__reversed__()):
            if pred(e):
                return i
        return -1

    def first(self, pred: Callable[[TS], bool] | None = None) -> TS | None:
        if self.__is_empty:
            return None
        if pred is None:
            return self[0]
        for e in self:
            if pred(e):
                return e
        return None

    def first_or_default(
        self, default: TS, pred: Callable[[TS], bool] | None = None
    ) -> TS:
        if self.__is_empty:
            return default
        if pred is None:
            return self[0]
        for e in self:
            if pred(e):
                return e
        return default

    def last(self, pred: Callable[[TS], bool] | None = None) -> TS | None:
        if self.__is_empty:
            return None
        if pred is None:
            return self[-1]
        for e in self.__reversed__():
            if pred(e):
                return e
        return None

    def last_or_default(
        self, default: TS, pred: Callable[[TS], bool] | None = None
    ) -> TS:
        if self.__is_empty:
            return default
        if pred is None:
            return self[-1]
        for e in self.__reversed__():
            if pred(e):
                return e
        return default

    def order_by(self, key: Callable[[TS], Any]) -> "linq[TS]":
        return linq(sorted(self, key=key))

    def order_by_descending(self, key: Callable[[TS], Any]) -> "linq[TS]":
        return linq(sorted(self, key=key, reverse=True))


def range(s: int, c: int) -> linq[int]:
    return linq([i for i in _range(s, c)])


def repeat(v: TF, c: int) -> linq[TF]:
    return linq([v for _ in _range(c)])
