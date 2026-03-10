import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math
import time
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped

class NavigationActionServer(Node):
    def __init__(self):
        super().__init__('nav_action_server')
        self.odom_sub = self.create_subscription(Odometry,'odom',self.odom_callback,10)
        self.goal_status=self.create_publisher(String,'goal_status',10)
        self.goal_pub = self.create_subscription(PoseStamped, 'goal_pose',self.goals, 10)
        self.current_x = 0.0
        self.current_y = 0.0
        self.goal_x = None
        self.goal_y = None
        self.has_goal = False
        self.timer = self.create_timer(0.5, self.check_progress)
        self.get_logger().info('Navigation action server ready')

    def odom_callback(self,msg):
        self.current_x=msg.pose.pose.position.x
        self.current_y=msg.pose.pose.position.y

    
    def check_progress(self):
        if not self.has_goal:
            return
        
        dx=self.goal_x-self.current_x
        dy=self.goal_y-self.current_y
        distance=math.sqrt(dx**2+dy**2)
        
        self.get_logger().info(
            f'Distance to goal: {distance:.2f}m | '
            f'Current: ({self.current_x:.2f}, {self.current_y:.2f})',
            throttle_duration_sec=1.0
        )
        
        
        if distance<0.01:
            self.get_logger().info('✓ Goal reached!')
            msg=String()
            msg.data='Goal Reached'
            self.goal_status.publish(msg)
            self.has_goal=False

    def goals(self,msg):
        self.goal_x=msg.pose.position.x
        self.goal_y=msg.pose.position.y
        self.get_logger().info(f"{self.goal_x,self.goal_y}")
        self.has_goal=True

def main(args=None):
    rclpy.init(args=args)
    node = NavigationActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()