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
        msg.robot_position = Pose()
        msg.ball_position = Point()
        msg.ball_orientation = Twist()
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing robot pos: {}, ball pos: {} and ball orien: {}".format(msg.robot_position, msg.ball_position, msg.ball_orientation))


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