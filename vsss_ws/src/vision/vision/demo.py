from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import numpy as np

import cv2
from sensor_msgs.msg import Image

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

class ImageConverter(Node):

  def __init__(self):
    super().__init__('demo')
    self.image_sub = self.create_subscription(Image, 'image_raw', self.callback, 10)
    self.image_pub = self.create_publisher(Image, 'image_topic_2', 10)
    self.bridge = CvBridge()

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      # print("drawing circle")
      cv2.circle(cv_image, (50,50), 50, (255, 0, 0), 6)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)


def main(args=None):
    rclpy.init(args=args)
    ic = ImageConverter()
    try:
      rclpy.spin(ic)
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ic.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main(sys.argv)