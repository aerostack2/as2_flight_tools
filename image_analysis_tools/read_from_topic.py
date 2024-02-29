#! /home/cvar/anaconda3/envs/ultralytics_pip/bin/python
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from rclpy.qos import qos_profile_sensor_data

import argparse

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topic', type = str, help="Topic to subscribe and read images from")
    parser.add_argument('-d', '--dir', type=str, help='Directory where images read from topic will be saved')
    args = parser.parse_args()
    print(args)
    return args

class ImageTopicReader(Node):

    def __init__(self, topic, dir):
        
        super().__init__('minimal_subscriber')

        self.topic = topic
        self.dir = dir

        self.subscription = self.create_subscription(
            Image,
            topic,
            self.listener_callback,
            qos_profile_sensor_data
        )

        self.subscription  # prevent unused variable warning
        self.bridge  = CvBridge()
        self.images = []
        self.i = 0
        print("Running")
 
    def listener_callback(self, msg: Image):
        image_message = self.bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')
        path = os.path.join(self.dir,str(self.i)+'_S.JPG') 
        self.images.append((path, image_message))
        self.get_logger().info('Reciving image')
        self.i += 1

def main(args):

    try:
        rclpy.init(args=None)

        os.makedirs(args["dir"], exist_ok=True)

        image_topic_reader = ImageTopicReader(args["topic"], args["dir"])

        rclpy.spin(image_topic_reader)

        image_topic_reader.destroy_node()
        rclpy.shutdown()

    except KeyboardInterrupt as kb:
       
        print("KeyboardInterrupt")
        for img_path, img in image_topic_reader.images:
            cv2.imwrite(img_path, img) 
            print("Saving image to ", img_path) 

if __name__ == '__main__':

    args = vars(options())
    main(args)