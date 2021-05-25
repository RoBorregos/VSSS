import rclpy
from rclpy.node import Node
from vsss_interfaces.msg import VisionTopic
from geometry_msgs.msg import Pose, Point, Twist

class Vision(Node):
    def __init__(self):
        super().__init__('vision')
        self.publisher_ = self.create_publisher(VisionTopic, 'vision_output', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = VisionTopic()
        [msg.robot_positions.append(Pose()) for _ in range(6)]
        [msg.robot_speeds.append(Twist()) for _ in range(6)]
        msg.ball_position = Point()
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing robots positions, speeds and ball position.")


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = Vision()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()