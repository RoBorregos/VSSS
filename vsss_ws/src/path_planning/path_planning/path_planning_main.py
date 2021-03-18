import time
from matplotlib import pyplot as plt
from path_planning.modules.point import Point
from path_planning.modules.rrt import RRT
from path_planning.modules.rrt_star import RRTStar


def main():
    r = 0.5
    obstacles = [
        (Point(7.89, 7.05), r), 
        (Point(4, 10), r), 
        (Point(7, 7), r), 
        (Point(8, 6), r), 
        (Point(13, 12), r)
    ]
    start = Point(4.0, 1.0)
    goal = Point(10.0, 10.0)
    max_iter = 25

    t0 = time.perf_counter()
    rrt = RRTStar(start, 90.0, goal, 90.0, obstacles, max_iter)
    path = rrt.planning()
    print(path)
    control = rrt.package(path, 1)
    t1 = time.perf_counter() - t0
    print(f"Function took {t1*(10**3):.1f}ms to finish")

    # lo de abajo ocupa matplotlib
    if control:
        # print('    x       y     deg')
        # for x, y, deg in control:
        #     print(f'({x:.3f}, {y:.3f}, {deg:.3f})')
        # coords = ((pos.x, pos.y) for pos in path)
        # x, y = list(zip(*coords))
        # plt.plot(x, y)

        for point, r in obstacles:
            circle = plt.Circle((point.x, point.y), r, color='black')
            plt.gca().add_patch(circle)
        for x, y, _ in control:
            circle = plt.Circle((x, y), 0.2, color='green')
            plt.gca().add_patch(circle)
        for point in (start, goal):
            circle = plt.Circle((point.x, point.y), 0.15, color='red')
            plt.gca().add_patch(circle)
        plt.xlim([0, 15])
        plt.ylim([0, 20])
        plt.show()
        print('matplotlib brr')
    else:
        print('fail')

if __name__ == '__main__':
    main()
