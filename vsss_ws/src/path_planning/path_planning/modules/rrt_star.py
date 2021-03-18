import math
from typing import List, Tuple
from path_planning.modules.node import Node
from path_planning.modules.point import Point
from path_planning.modules.rrt import RRT


class RRTStar(RRT):
    CONNECT_CIRCLE_DIST = 50.0
    SEARCH_FINISH = True

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
                 EXPAND: float = 30.0,
                 CIRCLE_DIST: float = 50.0,
                 FULL_SEARCH: int = True) -> None:
        super().__init__(start, start_angle, end, end_angle, obstacles, max_iter,
                         SAMPLE_RATE, PATH_RESOLUTION, WIDTH, HEIGHT, EXPAND)
        self.CIRCLE_DIST = CIRCLE_DIST
        self.FULL_SEARCH = FULL_SEARCH

    def planning(self) -> List['Point']:
        self.node_list = [self.start]

        for _ in range(self.max_iter):
            rand_node = self.get_random_node()
            near_index = rand_node.nearest_node_index(self.node_list)
            new_node = self.steer(self.node_list[near_index], rand_node)
            near_node = self.node_list[near_index]
            new_node.cost = near_node.new_cost(new_node)

            if new_node.check_collision(self.obstacles):
                near_indexes = self.near_nodes(new_node)
                node_updated = self.choose_parent(new_node, near_indexes)
                if node_updated:
                    self.rewire(node_updated, near_indexes)
                    self.node_list.append(node_updated)
                else:
                    self.node_list.append(new_node)
            
            if not self.FULL_SEARCH and new_node:
                break
            
        last_index = self.search_goal_node()
        if last_index is not None:
            return self.path(last_index)

        return None

    def choose_parent(self, new_node: 'Node', near_indexes: List[int]) -> 'Node':
        if not near_indexes:
            return None

        cost = float('inf')
        index = 0
        for i in near_indexes:
            near_node = self.node_list[i]
            t_node = self.steer(near_node, new_node)
            if t_node and t_node.check_collision(self.obstacles):
                new_cost = near_node.new_cost(new_node)
                if new_cost < cost:
                    cost = new_cost
                    index = i

        if cost == float('inf'):
            return None

        new_node = self.steer(self.node_list[index], new_node)
        new_node.cost = cost

        return new_node

    def search_goal_node(self) -> int:
        to_goal = [i for i in range(len(self.node_list)) 
                    if self.dist_to_goal(self.node_list[i]) <= self.EXPAND]

        safe_goal = []
        for i in to_goal:
            t_node = self.steer(self.node_list[i], self.end)
            if t_node.check_collision(self.obstacles):
                safe_goal.append(i)

        if not safe_goal:
            print('Not Safe')
            return None

        index = 0
        minVal = float('inf')
        for i in safe_goal:
            if self.node_list[i].cost <= minVal:
                minVal = self.node_list[i].cost
                index = i

        return index

    def near_nodes(self, new_node: 'Node') -> List[int]:
        n = len(self.node_list) + 1
        r = min(self.EXPAND, self.CIRCLE_DIST * math.sqrt(math.log(n) / n))
        distances_list = [new_node.point.distance(
            node.point) for node in self.node_list]
        near_indexes = [i for i in range(
            len(distances_list)) if distances_list[i] <= r**2]
        return near_indexes

    def rewire(self, new_node: 'Node', near_indexes: List[int]) -> None:
        for i in near_indexes:
            near_node = self.node_list[i]
            edge_node = self.steer(new_node, near_node)
            if not edge_node:
                continue
            edge_node.cost = new_node.new_cost(near_node)

            improvement = near_node.cost > edge_node.cost
            if edge_node.check_collision(self.obstacles) and improvement:
                edge_node.copy_attributes(near_node)
                self.cost_to_leaves(new_node)

    def cost_to_leaves(self, parent_node: 'Node') -> None:
        for node in self.node_list:
            if node.parent == parent_node:
                node.cost = parent_node.new_cost(node)
                self.cost_to_leaves(node)
