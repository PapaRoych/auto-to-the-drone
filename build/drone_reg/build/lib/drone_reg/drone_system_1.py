import math
from mavsdk import System
from mavsdk.telemetry import Telemetry
import asyncio
from  drone_system_0 import DroneSystem0 

from rclpy.node import Node
import rclpy

from geometry_msgs.msg import  PoseStamped
import rclpy.node

def coordinat(lat,lon,alt):
    
    Radius_ether = 6378137 
    
    latitude_rad = math.radians(lat)
    longitude_rad = math.radians(lon)

    x = (Radius_ether + alt) * math.cos(latitude_rad) * math.cos(longitude_rad)
    y = (Radius_ether + alt) * math.cos(latitude_rad) * math.sin(longitude_rad)
    z = (Radius_ether + alt) * math.sin(latitude_rad)
    return x, y, z
    

# class GpsData(DroneSystem0, Node):
class GpsData(DroneSystem0):

    # def __init__(self):
    def __init__(self, node: Node):
        # super().__init__('Topic')
        self.publishers_GPS = node.create_publisher(PoseStamped, 'topic_drone_gps',10)

        timer =  0.5
        self.timer_gps = node.create_timer(timer, self.info)

        self.drone = System()
        self.state_gps = []


    async def drone_connect(self):
        return await super().drone_connect()

    async def gps_data(self):
        if self.state.is_connected:
            async for self.data in self.drone.telemetry.raw_gps():
                self.state_gps.append(self.data.absolute_altitude_m)
                self.state_gps.append(self.data.latitude_deg) 
                self.state_gps.append(self.data.longitude_deg)
                break
            self.x, self.y, self.z  = coordinat(self.state_gps[1],self.state_gps[2],self.state_gps[0])
        else:
            print("Проверьте подключение к радиотелеметрии")

    def output(self):
        self.a = self.x
        self.b = self.y
        self.c = self.z

    def info(self):

        msg_pose = PoseStamped()
        msg_pose.pose.position.x = self.a
        msg_pose.pose.position.y = self.b
        msg_pose.pose.position.z = self.c
        print(msg_pose.pose.position)
        self.publishers_GPS.publish(msg_pose)
    
    
def main(args=None):
    rclpy.init(args=args)
    nh = Node("async_gps_node")
    Topic = GpsData(nh)
    asyncio.get_event_loop().run_until_complete(Topic.drone_connect())
    asyncio.get_event_loop().run_until_complete(Topic.gps_data())
    Topic.output()
    asyncio.get_event_loop().run_until_complete(rclpy.spin(nh))            
    

    Topic.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    


