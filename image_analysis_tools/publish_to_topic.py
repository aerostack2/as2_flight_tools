import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import time
from rclpy.qos import qos_profile_sensor_data

import argparse

def options():

    parser = argparse.ArgumentParser("Utility to publish local images to topic")
    parser.add_argument('-d', '--dir', type = str, help = "Path to local directory containing images")
    parser.add_argument('-t', '--topic', type = str, help = 'Topic to publish the images')
    parser.add_argument('-i', '--interval', type = float, help = 'Interval between images', default = 0)
    args = parser.parse_args()
    print(args)
    return args

class ImageTopicPublisher(Node):

    def __init__(self, dir, topic, interval):
        super().__init__('ImageTopicPublisher')

        self.publisher_ = self.create_publisher(Image, topic, qos_profile_sensor_data)
        self.i = 0
        self.interval = interval
        self.timer = self.create_timer(self.interval, self.timer_callback)

        self.images = self.load_images(dir)
        self.bridge  = CvBridge()


    def load_images(self,dir):
        images = [] 
        
        for f in filter(lambda x : '.jpg' in x.lower() or '.png' in x.lower() ,os.listdir(dir)):
            images.append((f,cv2.imread(os.path.join(dir, f))))
        
        return images

            
    def timer_callback(self):
        if self.i >= len(self.images):
            print("All images published")
            return
        msg = self.bridge.cv2_to_imgmsg(self.images[self.i][1], 'bgr8')
        # msg = self.bridge.cv2_to_compressed_imgmsg(self.images[self.i][1], 'jpg') 
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % self.images[self.i][0])
        self.i += 1 

def main(args):
    rclpy.init(args=None)

    file_path = args["dir"]
    topic = args["topic"]
    interval = args["interval"]

    minimal_publisher = ImageTopicPublisher(file_path, topic, interval)

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    args = vars(options())
    main(args)