import asyncio
from drone_system_0 import DroneSystem0

import mavsdk
from mavsdk import System 

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import  PoseStamped


class DroneReg():
    
    def __init__(self,node:Node):

        self.subscription_ = node.create_subscription(PoseStamped,'topic_drone_gps',self.decortov,10)
      
       
    
    def decortov(self,msg):
    
        self.position_X = msg.pose.position.x
        self.position_Y = msg.pose.position.y
        self.position_Z = msg.pose.position.z
        print(self.position_X)
    
    
        
    

def main(args=None):
    rclpy.init(args=args)
    node_header = Node("drone_reg_node")
    Topic = DroneReg(node_header)
    rclpy.spin(node_header)
    Topic.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
    