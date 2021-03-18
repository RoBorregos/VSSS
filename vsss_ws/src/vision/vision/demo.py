from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import numpy as np

import cv2
from sensor_msgs.msg import Image

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