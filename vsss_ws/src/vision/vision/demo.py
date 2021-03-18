import cv_bridge
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import numpy as np


def test_cvtColorForDisplay():
    # convert label image to display
    label = np.zeros((480, 640), dtype=np.int32)
    height, width = label.shape[:2]
    label_value = 0
    grid_num_y, grid_num_x = 3, 4
    for grid_row in range(grid_num_y):
        grid_size_y = height // grid_num_y
        min_y = grid_size_y * grid_row
        max_y = min_y + grid_size_y
        for grid_col in range(grid_num_x):
            grid_size_x = width // grid_num_x
            min_x = grid_size_x * grid_col
            max_x = min_x + grid_size_x
            label[min_y:max_y, min_x:max_x] = label_value
            label_value += 1
    label_viz = cv_bridge.cvtColorForDisplay(label, '32SC1', 'bgr8')
    assert label_viz.dtype == np.uint8
    assert label_viz.min() == 0
    assert label_viz.max() == 255

    # Check that mono8 conversion returns the right shape.
    bridge = cv_bridge.CvBridge()
    mono = np.random.random((100, 100)) * 255
    mono = mono.astype(np.uint8)

    input_msg = bridge.cv2_to_imgmsg(mono, encoding='mono8')
    output = bridge.imgmsg_to_cv2(input_msg, desired_encoding='mono8')
    assert output.shape == (100, 100)


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()