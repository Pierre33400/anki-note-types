
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Generic, Iterator, Mapping, TypeVar

K = TypeVar("K")
V = TypeVar("V")

@dataclass(frozen=True, slots=True)
class Catalog(Generic[K, V]):
    items: Mapping[K, V]

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", MappingProxyType(dict(self.items)))

    def get(self, key: K) -> V | None:
        return self.items.get(key)

    def require(self, key: K) -> V:
        try:
            return self.items[key]
        except KeyError as exc:
            raise KeyError(f"Unknown identifier: {key}") from exc

    def contains(self, key: K) -> bool:
        return key in self.items

    def values(self):
        return self.items.values()

    def keys(self):
        return self.items.keys()

    def __iter__(self) -> Iterator[V]:
        return iter(self.items.values())

    def __len__(self) -> int:
        return len(self.items)
