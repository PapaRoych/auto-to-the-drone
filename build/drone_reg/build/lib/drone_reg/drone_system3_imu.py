from drone_system_0 import DroneSystem0

import mavsdk
from mavsdk import System
import asyncio

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu


class ImuDrone(DroneSystem0):
    
    def __init__(self, node : Node ):
        self.publisher_imu = node.create_publisher(Imu,'topic_drone_imu',10)
        timer = 0.5
        self.timer = node.create_timer(timer,self.info_callback)
        
        self.drone = System()
        self.state_imu_acceleration = []
        self.state_imu_angular = []
        
    
    async def imu_data(self):
        if self.state.is_connected:

            async for self.data in self.drone.telemetry.imu():
                self.state_imu_acceleration.append(self.data.acceleration_frd)
                self.state_imu_angular.append(self.data.angular_velocity_frd)
    
                break
            self.a = self.state_imu_acceleration[0]
            self.b = self.state_imu_angular[0]
            print(self.a)
        
        else:
            print("Проверьте подключение к радиотелеметрии")

    def output(self):

        self.acceleration = self.a
        self.angular = self.b


    def info_callback(self):

        msg_imu = Imu()
        msg_imu.angular_velocity = self.angular
        msg_imu.linear_acceleration = self.acceleration
        print(msg_imu)
        self.publisher_imu.publish(msg_imu)


def main(args=None):

    rclpy.init(args=args)
    node_header = Node("async_gps_node")
    Topic = ImuDrone(node_header)
    asyncio.get_event_loop().run_until_complete(Topic.drone_connect())
    asyncio.get_event_loop().run_until_complete(Topic.imu_data())
    Topic.output()
    asyncio.get_event_loop().run_until_complete(rclpy.spin(node_header))            
    

    Topic.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
    
        
        