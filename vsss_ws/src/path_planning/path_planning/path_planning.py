import rclpy
from rclpy.node import Node
from vsss_interfaces.msg import StrategyTopic, PathPlanningTopic
from geometry_msgs.msg import Pose, PoseArray

class PathPlanning(Node):
    def __init__(self):
        super().__init__('path_planning')
        self.suscriber_ = self.create_subscription(StrategyTopic, 'strategy_output', self.callback_path_planning, 10)
        self.publisher_ = self.create_publisher(PathPlanningTopic, 'path_planning_output', 10)

    def callback_path_planning(self, msg):
        for robot in msg.robot_positions:
            self.get_logger().info("Receiving robot information")
        self.get_logger().info("Robots info received")

        newMsg = PathPlanningTopic()
        [newMsg.trajectories.append(PoseArray()) for _ in range(3)]
        self.publisher_.publish(newMsg)
        self.get_logger().info("Robots path sento to control.")

def main(args=None):
    rclpy.init(args=args)

    node = PathPlanning()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()