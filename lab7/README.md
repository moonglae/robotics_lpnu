# Laboratory Work 7: Coordinate Transforms (TF2), URDF/Xacro, and RTR Manipulator

## Overview This repository contains the completed Laboratory Work 7. The project implements the forward kinematics of a 3-DOF **RTR (Revolute–Translational–Revolute)** manipulator, visualizes its URDF/Xacro model, and integrates it with `ros2_control` for dynamic joint tracking.

### Step 1: Build the Workspace
Build the package with the symlink option to allow Python file updates without rebuilding:

```bash
cd /opt/ws
colcon build --packages-select lab7 --symlink-install
source install/setup.bash
```

### Step 2: Part A — TF2 Broadcaster and Listener
Run the dynamic broadcaster and listener to verify that the internal tf2 transforms match the analytic mathematical model.

#### Terminal 1:

```bash
ros2 run lab7 tf2_broadcaster_demo -- 0.2 0.5 0.35
```

#### Terminal 2:

```bash
ros2 run lab7 tf2_listener_demo -- 0.2 0.5 0.35
```

### Step 3: Part B — URDF/Xacro Visualization
Launch the visual representation of the manipulator. The model includes full collision geometry.

```bash
ros2 launch lab7 rtr_visualize.launch.py
```
(Use the joint_state_publisher_gui to move the robot in RViz2).

### Step 4: Part C — ROS 2 Control
Launch the mock hardware control stack to send live commands to the robot.

#### Terminal 1:

```bash
ros2 launch lab7 rtr_ros2_control.launch.py
```

#### Terminal 2 (Send position command):

```bash
ros2 topic pub --once /forward_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.2, 0.6, 0.4]"
```

#### Terminal 3 (Verify transform):

```bash
ros2 run tf2_ros tf2_echo base_link tool0
```

### Step 5: Automated Tests
Run the pytest suite to validate forward kinematics and TF2 analytic agreement:

```bash
colcon test --packages-select lab7
```

