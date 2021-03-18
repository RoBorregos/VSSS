import random
import math
from typing import List, Tuple
from path_planning.modules.node import Node
from path_planning.modules.point import Point


class RRT:
    def __init__(self,
                 start: 'Point',
                 start_angle: float,
                 end: 'Point',
                 end_angle: float,
                 obstacles: List[Tuple['Point', float]],
                 max_iter: int,
                 SAMPLE_RATE: int = 5,
                 PATH_RESOLUTION: float = 0.5,
                 WIDTH: int = 15,
                 HEIGHT: int = 20,
                 EXPAND: float = 3.0) -> None:

        self.start = Node(start)
        self.start_angle = start_angle
        self.end = Node(end)
        self.end_angle = end_angle
        self.max_iter = max_iter
        self.obstacles = obstacles
        self.node_list = []
        self.SAMPLE_RATE = SAMPLE_RATE
        self.PATH_RESOLUTION = PATH_RESOLUTION
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.EXPAND = EXPAND

    def get_random_node(self) -> 'Node':
        if random.randint(0, 100) > self.SAMPLE_RATE:
            rand_point = Point(
                random.uniform(0, self.WIDTH),
                random.uniform(0, self.HEIGHT))
            return Node(rand_point)
        return Node(self.end.point.copy())

    def dist_to_goal(self, other: 'Node') -> float:
        return self.end.point.distance(other.point)

    def path(self, goal_index: int = -1) -> List['Point']:
        path = [self.end.point]
        node = self.node_list[goal_index]
        while node.parent:
            if node.point == path[-1]:
                node = node.parent
                continue
            path.append(node.point)
            node = node.parent
        path.append(node.point)
        return path

    def steer(self, origin: Node, goal: Node) -> Node:
        new_node = Node(origin.point.copy())

        distance = new_node.point.distance(goal.point)
        theta = new_node.point.angle(goal.point)

        new_node.path = [new_node.point.copy()]

        extend = min(self.EXPAND, distance)

        n_expand = math.floor(extend / self.PATH_RESOLUTION)

        x_theta = math.cos(theta)
        y_theta = math.sin(theta)

        for _ in range(n_expand):
            new_node.point.x += self.PATH_RESOLUTION * x_theta
            new_node.point.y += self.PATH_RESOLUTION * y_theta
            new_node.path.append(new_node.point.copy())

        distance = new_node.point.distance(goal.point)

        if distance <= self.PATH_RESOLUTION:
            new_node.path.append(goal.point.copy())
            new_node.point = goal.point.copy()
        new_node.parent = origin
        return new_node

    def planning(self) -> List['Point']:
        self.node_list = [self.start]

        for _ in range(self.max_iter):
            rand_node = self.get_random_node()
            near_index = rand_node.nearest_node_index(self.node_list)
            near_node = self.node_list[near_index]

            new_node = self.steer(near_node, rand_node)

            if new_node.check_collision(self.obstacles):
                self.node_list.append(new_node)

            if self.dist_to_goal(self.node_list[-1]) <= self.EXPAND:
                final_node = self.steer(self.node_list[-1], self.end)
                if final_node.check_collision(self.obstacles):
                    return self.path()
        return []

    def package(self,  path: List['Point'], distance: float) -> List[Tuple[float, ...]]:
        # TODO if path is None
        n = len(path)
        control_path = [(self.end.point.x, self.end.point.y, self.end_angle)]
        if n <= 1:
            return control_path
        carry_over = 0.0
        for i in range(1, n):
            last = path[i-1]
            current = path[i]
            v = current - last
            v_length = v.length()
            u = v / v_length
            angle = math.degrees(current.angle(last))
            coords = max(0, math.floor((v_length + carry_over) / distance))
            if coords == 0:
                carry_over += v_length
                continue
            for j in range(1, coords+1):
                pos: 'Point' = last + (u * (distance * j - carry_over))
                control_path.append((pos.x, pos.y, angle))
            carry_over = distance - \
                ((distance * (coords+1)) - v_length - carry_over)
        return control_path
