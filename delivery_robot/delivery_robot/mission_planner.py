import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import Taskassign

class MissionPlanner(Node):
    def __init__(self):
        super().__init__('mission_planner')
        self.waypoints = [
            {'name': 'Pickup Station', 'x': 2.0, 'y': 1.0},
            {'name': 'Delivery Point A', 'x': 5.0, 'y': 3.0},
            {'name': 'Delivery Point B', 'x': 3.0, 'y': 5.0},
            {'name': 'Return to Base', 'x': 0.0, 'y': 0.0},
        ]
        self.current_waypoint_index=0
        self.get_logger().info(f'Mission planner started - {len(self.waypoints)} waypoints')
        self.assign_task=self.create_service(Taskassign,'task',self.task_assigning)

    def task_assigning(self,request,response):
         if self.current_waypoint_index >= len(self.waypoints):
            self.get_logger().info('✓ Mission complete - all waypoints visited')
            response.goal=[0.0,0.0,0.0,1.0]
            response.message='all goals reached'
            response.success=False
            return response
         wp = self.waypoints[self.current_waypoint_index]
            
         if request.ask:
            response.goal=[wp['x'],wp['y'],0.0,1.0]
            self.current_waypoint_index+=1
            response.message=f"Move towards {wp['x']:.1f},{wp['y']:.1f}"
            response.success=True

         self.get_logger().info(
            f'📍 Waypoint {self.current_waypoint_index}/{len(self.waypoints)}: '
            f'{wp["name"]} at ({wp["x"]:.1f}, {wp["y"]:.1f})'
        )
         
         return response
         



def main(args=None):
    rclpy.init(args=args)
    node = MissionPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()