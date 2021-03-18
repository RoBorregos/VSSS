from typing import Union
import math


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f'({self.x:.3f}, {self.y:.3f})'

    def __eq__(self, other: 'Point'):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other: 'Point'):
        return not self.__eq__(other)

    def __add__(self, other: Union['Point', float]) -> 'Point':
        if type(other) == float:
            return Point(self.x + other, self.y + other)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Union['Point', float]) -> 'Point':
        if type(other) == float:
            return Point(self.x - other, self.y - other)
        return Point(self.x - other.x, self.y - other.y)

    def __truediv__(self, other: Union['Point', float]) -> 'Point':
        if type(other) == float:
            return Point(self.x / other, self.y / other)
        return Point(self.x / other.x, self.y / other.y)

    def __mul__(self, other: Union['Point', float]) -> 'Point':
        if type(other) == float:
            return Point(self.x * other, self.y * other)
        return Point(self.x * other.x, self.y * other.y)

    def distance(self, other: 'Point') -> float:
        return math.hypot(self.dx(other), self.dy(other))

    def angle(self, other: 'Point') -> float:
        return math.atan2(self.dy(other), self.dx(other))

    def dx(self, other: 'Point') -> float:
        return other.x - self.x

    def dy(self, other: 'Point') -> float:
        return other.y - self.y

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
