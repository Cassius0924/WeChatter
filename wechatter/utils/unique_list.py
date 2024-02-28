import json
from typing import Generic, Iterable, List, TypeVar

T = TypeVar("T")


class UniqueList(Generic[T]):
    """
    唯一列表
    """

    def __init__(self, iterable: Iterable[T] = ()):
        self.elements: List[T] = []
        for element in iterable:
            self.add(element)

    def add(self, element: T):
        if element in self.elements:
            raise ValueError(f"元素 {element} 已存在")
        else:
            self.elements.append(element)

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value: T):
        if value not in self.elements:
            self.elements[index] = value

    def __delitem__(self, index):
        del self.elements[index]

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return str(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __repr__(self):
        return f"UniqueList({self.elements})"

    def index(self, element: T):
        return self.elements.index(element)


class UniqueListEncoder(json.JSONEncoder):
    """
    唯一列表编码器
    """

    def default(self, obj):
        if isinstance(obj, UniqueList):
            return {"is_unique_list": True, "elements": obj.elements}
        return super().default(obj)


class UniqueListDecoder(json.JSONDecoder):
    """
    唯一列表解码器
    """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if "is_unique_list" in dct:
            return UniqueList(dct["elements"])
        return dct
