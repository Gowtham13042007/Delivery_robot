import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster

class TfPublisher(Node):
    def __init__(self):
        super().__init__('robot_state_publisher')
        self.static_broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_transforms()
        self.get_logger().info('Tf2_publisher started')

    def publish_static_transforms(self):
        t1 = TransformStamped()
        t1.header.stamp = self.get_clock().now().to_msg() 
        t1.header.frame_id = 'base_link'
        t1.child_frame_id = 'camera_frame'
        t1.transform.translation.x = 0.1
        t1.transform.translation.y = 0.3
        t1.transform.translation.z = 0.0
        t1.transform.rotation.x = 0.0
        t1.transform.rotation.y = 0.0
        t1.transform.rotation.z = 0.0
        t1.transform.rotation.w = 1.0
        self.static_broadcaster.sendTransform(t1)

def main(args=None):
    rclpy.init(args=args)
    node = TfPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()