import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from my_robot_interfaces.srv import Taskassign
from std_msgs.msg import String
import tf2_geometry_msgs
from geometry_msgs.msg import PoseStamped

class TFListenerNode(Node):
    def __init__(self):
        super().__init__('tf_listener_node')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        self.subscriber_ = self.create_subscription(
            String, 'goal_status', self.reseting_callback, 10)
        self.goal_x = None
        self.goal_y = None

        self.client = self.create_client(Taskassign, 'task')
        while not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Service not available, waiting...')
        self._initial_done = False
        self.create_timer(2.0, self._initial_call)

    def _initial_call(self):
        if not self._initial_done:
            self._initial_done = True
            self.service_calling()

    def service_calling(self):
        request = Taskassign.Request()
        request.ask = True
        future = self.client.call_async(request)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        result = future.result()
        if not result.success:
            self.get_logger().info(result.message)
            return

        self.goal_x = result.goal[0]
        self.goal_y = result.goal[1]

        msg = PoseStamped()
        msg.header.stamp = rclpy.time.Time().to_msg() 
        msg.header.frame_id = 'camera_frame'
        msg.pose.position.x = self.goal_x
        msg.pose.position.y = self.goal_y

        try:
            if not self.tf_buffer.can_transform(
                'base_link', 'camera_frame',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=2.0)
            ):
                self.get_logger().warn('Transform not ready, retrying in 1s...')
                self.create_timer(1.0, lambda: self.goal_response_callback(future))
                return

            point_base = self.tf_buffer.transform(
                msg, 'base_link',
                timeout=rclpy.duration.Duration(seconds=2.0)
            )
            self.get_logger().info(
                f'Goal in base_link: ({point_base.pose.position.x:.2f}, '
                f'{point_base.pose.position.y:.2f})'
            )
            self.goal_pub.publish(point_base)

        except Exception as e:
            self.get_logger().warn(f'Transform failed: {e}')

    def reseting_callback(self, msg):
        if msg.data == 'Goal Reached':
            self.service_calling()

def main(args=None):
    rclpy.init(args=args)
    node = TFListenerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()