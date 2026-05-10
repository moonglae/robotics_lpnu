# Laboratory Work 7: RTR Manipulator, TF2 Transformations, and URDF Modeling

## Project Overview

This repository contains the source code, configuration files, and launch scripts for Laboratory Work 7. The core objective of this project is to implement and verify the forward kinematics of a 3-DOF **RTR (Revolute-Translational-Revolute)** robotic manipulator.

The package includes a comprehensive visual model built with URDF/Xacro, calculates spatial coordinate relationships using the `tf2` library, and demonstrates automated joint state tracking via the `ros2_control` framework.

---

### Step 1: Workspace Compilation

To get started, build the ROS 2 package. Using the `--symlink-install` flag is recommended, as it allows dynamic updates to Python scripts without requiring a full rebuild.

```bash
cd /opt/ws
colcon build --packages-select lab7 --symlink-install
source install/setup.bash
Step 2: Part A — Kinematics and TF2 Transforms
Validate the mathematical model by running the broadcaster and listener nodes. This step ensures that the custom analytic kinematics perfectly align with the ROS 2 internal tf2 coordinate tree.

Terminal 1 (Broadcaster):

Bash
ros2 run lab7 tf2_broadcaster_demo -- 0.2 0.5 0.35
Terminal 2 (Listener):

Bash
ros2 run lab7 tf2_listener_demo -- 0.2 0.5 0.35
Step 3: Part B — Manipulator Visualization
Load the complete 3D model of the RTR manipulator into RViz2, including its visual properties and collision geometry.

Bash
ros2 launch lab7 rtr_visualize.launch.py
Step 4: Part C — Automated ROS 2 Control
Initialize the mock hardware stack to send automated positioning commands to the robotic arm.

Terminal 1 (Launch Controllers):

Bash
ros2 launch lab7 rtr_ros2_control.launch.py
Terminal 2 (Execute Position Command):

Bash
ros2 topic pub --once /forward_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.2, 0.6, 0.4]}"
Terminal 3 (Verify Transform):
Check the precise distance and rotation between the base and the end-effector:

Bash
ros2 run tf2_ros tf2_echo base_link tool0
Troubleshooting Note: If the controller_manager fails to load due to Docker container library conflicts (e.g., FastDDS symbol lookup errors), you can bypass the forward position controller by publishing directly to the joint states:
ros2 topic pub /joint_states sensor_msgs/msg/JointState "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''}, name: ['joint_theta1', 'joint_theta2', 'joint_theta3'], position: [0.2, 0.6, 0.4]}"

Step 5: Automated Testing
Finally, run the integrated testing suite to programmatically validate the accuracy of the forward kinematics logic and the TF2 mathematical agreement.

Bash
colcon test --packages-select lab7
colcon test-result --all
```
