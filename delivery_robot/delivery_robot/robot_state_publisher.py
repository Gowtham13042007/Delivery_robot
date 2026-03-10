#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


class RobotStatePublisher(Node):
    def __init__(self):
        super().__init__('robot_state_publisher')
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.goal_pub=self.create_subscription(PoseStamped,'goal_pose',self.goal_assigning,10)
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0 
        self.vy = 0.0
        self.goal_x=None
        self.get_logger().info('Robot state publisher started')
        self.timer = self.create_timer(0.05, self.publish_dynamic_transforms)


    def publish_dynamic_transforms(self):
        if self.goal_x is None:
             return
             
        dt = 0.1
        dx = self.goal_x - self.x
        dy = self.goal_y - self.y
        
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 0.001:
            self.vx=0
            self.vy=0
            return

        dir_x = dx / distance
        dir_y = dy / distance

        speed=0.05

        self.vx = speed * dir_x
        self.vy = speed * dir_y
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        
        self.odom_pub.publish(odom)

    def goal_assigning(self,msg):
        self.timer.cancel()
        self.goal_x=msg.pose.position.x
        self.goal_y=msg.pose.position.y
        self.timer.reset()
          


    
def main(args=None):
    rclpy.init(args=args)
    node = RobotStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()