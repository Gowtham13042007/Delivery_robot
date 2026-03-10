#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction


def generate_launch_description():
 
    return LaunchDescription(
        [
        
        
        Node(
            package='delivery_robot',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen'
        ),
        
        
        
        Node(
            package='delivery_robot',
            executable='mission_planner',
            name='mission_planner',
            output='screen'
        ),

         Node(
            package='delivery_robot',
            executable='nav_action_server',
            name='nav_action_server',
            output='screen'
        )
         
        ,

         Node(
            package='delivery_robot',
            executable='tf2_publisher',
            name='tf2_publisher',
            output='screen'
        ),

         Node(
            package='delivery_robot',
            executable='tf2_listener',
            name='tf2_listener',
            output='screen'
        )
    


    
    ])