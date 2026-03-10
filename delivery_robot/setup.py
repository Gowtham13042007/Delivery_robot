from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'delivery_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gowtham',
    maintainer_email='gowtham@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tf2_publisher= delivery_robot.tf2_publisher:main',
            'robot_state_publisher = delivery_robot.robot_state_publisher:main',
            'tf2_listener= delivery_robot.tf2_listener:main',
            'nav_action_server = delivery_robot.nav_action_server:main',
            'mission_planner = delivery_robot.mission_planner:main',
        ],
    },
)
