from typing import List, Tuple
from path_planning.modules.point import Point


class Node:
    def __init__(self, point: 'Point', parent: 'Node' = None) -> None:
        self.point = point
        self.parent = parent
        self.path = []
        self.cost = 0.0

    def new_cost(self, other: 'Node') -> float:
        return self.cost + self.point.distance(other.point)

    def nearest_node_index(self, others: List['Node']) -> int:
        distances = [self.point.distance(node.point) for node in others]
        return distances.index(min(distances))

    def check_collision(self, obstacles: List[Tuple['Point', float]]) -> bool:
        for pos, radius in obstacles:
            distances = (pos.dx(point)**2 + pos.dy(point)
                         ** 2 for point in self.path)
            if min(distances) <= radius**2:
                return False
        return True

    def copy_attributes(self, other: 'Node'):
        other.point = self.point.copy()
        other.parent = self.parent
        other.path = self.path
        other.cost = self.cost
        return
