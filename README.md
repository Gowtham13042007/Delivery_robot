# 🤖 Delivery Robot — ROS 2 Package

A ROS 2-based autonomous delivery robot that uses a camera frame (via TF2 transforms) to receive goal coordinates and navigate the robot to sequential waypoints.

---

## 📁 Project Structure

```
delivery_robot/
├── delivery_robot/
│   ├── __init__.py
│   ├── mission_planner.py        # Waypoint service server
│   ├── nav_action_server.py      # Goal tracking & progress monitor
│   ├── robot_state_publisher.py  # Simulated robot motion (odometry)
│   ├── tf2_publisher.py          # Static TF2 transform broadcaster
│   └── tf2_listener.py           # TF2 listener + goal coordinator
├── launch/
│   └── delivery_robot.launch.py  # Launch all nodes together
├── resource/
├── test/
├── package.xml
├── setup.cfg
└── setup.py
```

---

## 🧠 System Architecture

```
MissionPlanner (Service Server)
        │
        │ Taskassign.srv (goal coordinates)
        ▼
TF2Listener (Service Client)
        │  Transforms goal from camera_frame → base_link
        │  Publishes to /goal_pose (PoseStamped)
        ▼
RobotStatePublisher          NavActionServer
  /goal_pose ──────────────► /goal_pose
  Moves robot (publishes      Monitors /odom distance
  /odom)                      Publishes /goal_status
        │                              │
        └──────────────────────────────┘
                  Loop continues until all waypoints are visited
```

---

## 🔧 Nodes

### 1. `mission_planner`
- **File:** `mission_planner.py`
- **Role:** Stores a list of predefined waypoints and serves them one by one via a ROS 2 service.
- **Service:** `/task` (`Taskassign`)
- **Waypoints (default):**
  | # | Name | X | Y |
  |---|------|---|---|
  | 1 | Pickup Station | 2.0 | 1.0 |
  | 2 | Delivery Point A | 5.0 | 3.0 |
  | 3 | Delivery Point B | 3.0 | 5.0 |
  | 4 | Return to Base | 0.0 | 0.0 |

---

### 2. `tf2_publisher`
- **File:** `tf2_publisher.py`
- **Role:** Broadcasts a **static TF2 transform** from `base_link` → `camera_frame`.
- **Transform offset:** `x=0.1, y=0.3, z=0.0`
- This simulates the physical offset of a camera mounted on the robot.

---

### 3. `tf2_listener`
- **File:** `tf2_listener.py`
- **Role:** Calls the mission planner service to get the next waypoint goal (in `camera_frame`), transforms it into `base_link` frame using TF2, and publishes it to `/goal_pose`.
- **Subscriptions:** `/goal_status` (String)
- **Publications:** `/goal_pose` (PoseStamped)
- **Service Client:** `/task` (Taskassign)

---

### 4. `robot_state_publisher`
- **File:** `robot_state_publisher.py`
- **Role:** Simulates robot motion. Moves the robot toward the received goal and publishes odometry at 20 Hz.
- **Subscriptions:** `/goal_pose` (PoseStamped)
- **Publications:** `/odom` (Odometry)
- Motion: Constant speed (`0.05 m/s`) toward goal; stops when within `0.001 m`.

---

### 5. `nav_action_server`
- **File:** `nav_action_server.py`
- **Role:** Monitors robot progress toward the goal. When the robot arrives (distance < 0.01 m), publishes `"Goal Reached"` to trigger the next waypoint.
- **Subscriptions:** `/odom` (Odometry), `/goal_pose` (PoseStamped)
- **Publications:** `/goal_status` (String)

---

## 📡 Topics & Services Summary

| Name | Type | Publisher | Subscriber |
|------|------|-----------|------------|
| `/odom` | `nav_msgs/Odometry` | robot_state_publisher | nav_action_server |
| `/goal_pose` | `geometry_msgs/PoseStamped` | tf2_listener | robot_state_publisher, nav_action_server |
| `/goal_status` | `std_msgs/String` | nav_action_server | tf2_listener |
| `/task` | `Taskassign` (srv) | — | tf2_listener (client) |

---

## 📦 Dependencies

- **ROS 2** (Humble / Iron recommended)
- `rclpy`
- `nav_msgs`
- `geometry_msgs`
- `std_msgs`
- `tf2_ros`
- `tf2_geometry_msgs`
- `my_robot_interfaces` (custom package — must include `Taskassign.srv`)

### `Taskassign.srv` definition (expected)
```
bool ask
---
float64[] goal
string message
bool success
```

---

## 🚀 Installation & Build

```bash
# Clone into your ROS 2 workspace
cd ~/ros2_ws/src
git clone <your-repo-url>

# Install dependencies
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --packages-select delivery_robot my_robot_interfaces

# Source
source install/setup.bash
```

---

## ▶️ Running the Project

### Launch all nodes at once:
```bash
ros2 launch delivery_robot delivery_robot.launch.py
```

### Or run nodes individually (5 separate terminals):
```bash
ros2 run delivery_robot mission_planner
ros2 run delivery_robot tf2_publisher
ros2 run delivery_robot tf2_listener
ros2 run delivery_robot robot_state_publisher
ros2 run delivery_robot nav_action_server
```

---

## 🔁 Execution Flow

1. **`tf2_listener`** calls `/task` service → gets waypoint goal in `camera_frame`
2. Goal is **transformed** from `camera_frame` → `base_link` using TF2
3. Transformed goal is published to `/goal_pose`
4. **`robot_state_publisher`** receives the goal and starts moving (updates `/odom`)
5. **`nav_action_server`** monitors `/odom` and detects when goal is reached
6. On arrival, it publishes `"Goal Reached"` on `/goal_status`
7. **`tf2_listener`** receives this and calls the service again for the next waypoint
8. Cycle repeats until all waypoints are visited

---

## 📝 Notes

- The robot motion is **simulated** (no physical hardware required). Replace `robot_state_publisher.py` with a hardware driver for real deployment.
- The TF2 static transform simulates a fixed camera offset. For a moving camera, replace `StaticTransformBroadcaster` with `TransformBroadcaster`.
- Goal coordinates from the mission planner are interpreted as being in `camera_frame` and automatically converted to `base_link` before navigation.

---

