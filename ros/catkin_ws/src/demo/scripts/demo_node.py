#!/usr/bin/env python
from cv_bridge import CvBridge, CvBridgeError
from duckietown_msgs.msg import Twist2DStamped
from sensor_msgs.msg import CompressedImage, Image
import rospy

#!/usr/bin/env python
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
from duckietown_msgs.msg import Twist2DStamped
from sensor_msgs.msg import CompressedImage, Image
import rospy
import numpy as np
import math
import sys
sys.path.append(sys.path.pop(1))
sys.path.append(sys.path.pop(1))
import cv2

def calc_angle(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height = image.shape[0]
    width = image.shape[1]

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    canny_image = cv2.Canny(gray_image, 100, 200)


    lines = cv2.HoughLinesP(canny_image,
                            rho=1,
                            theta=np.pi / 180,
                            threshold=100,
                            lines=np.array([]),
                            minLineLength=100,
                            maxLineGap=10)

    #TODO:  Come up with an algorithm that will process the lines

    return 0.0;


def img_to_cv2(image_msg):
    """
    Convert the image message into a cv2 image (numpy.ndarray)
    to be able to do OpenCV operations in it.
    :param Image or CompressedImage image_msg: the message to transform
    """
    type_as_str = str(type(image_msg))
    if type_as_str.find('sensor_msgs.msg._CompressedImage.CompressedImage') >= 0:
        np_arr = np.fromstring(image_msg.data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    elif type_as_str.find('sensor_msgs.msg._Image.Image') >= 0:
        try:
            return self.bridge.imgmsg_to_cv2(image_msg, image_msg.encoding)
        except CvBridgeError as e:
            rospy.logerr("Error when converting image: " + str(e))
            return None
        else:
            rospy.logerr("We don't know how to transform image of type " + str(type(image_msg)))
            return None


class DemoNode(object):
    def __init__(self):
        self.node_name = "LineDetectorNode"
        self.sub_image = rospy.Subscriber("/None/corrected_image/compressed", CompressedImage, self.cbImage, queue_size=1)
        self.pub_cmd = rospy.Publisher("/None/car_cmd", Twist2DStamped, queue_size=1)


    def cbImage(self, image_msg):
        msg = Twist2DStamped()
        msg.v = 0.3
        msg.omega = calc_angle(img_to_cv2(image_msg))
        self.pub_cmd.publish(msg)

if __name__ == '__main__': 
    rospy.init_node('demo',anonymous=False)
    demo_node = DemoNode()
    rospy.spin()
