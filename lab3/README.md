Overview
This package demonstrates the kinematic control of a differential drive robot within a ROS2 and Gazebo simulation environment. The primary objective is to command the robot to autonomously navigate specific geometric trajectories (a square and a figure-8). 

Unlike open-loop systems that rely purely on timers, this project implements **closed-loop control** utilizing real-time odometry feedback (`nav_msgs/Odometry`). This ensures high precision, as the robot actively tracks its position and orientation to adjust its movements dynamically.

---

## Step-by-Step Execution Guide

To run this project, you will need to use multiple terminal windows (tabs) to keep the simulation and the control nodes running simultaneously.

### Terminal 1: Build and Launch Simulation
First, compile the workspace and launch the Gazebo world along with the RViz2 visualizer.

```bash
# 1. Navigate to the workspace (inside your Docker container)
cd /opt/ws

# 2. Build the specific package
colcon build --packages-select lab3

# 3. Source the setup file to load the new executables
source install/setup.bash

# 4. Launch the simulation environment
ros2 launch lab3 bringup.launch.py
Important: After the windows open, press the Play button in Gazebo. In RViz2, ensure the Fixed Frame under Global Options is set to odom to visualize the path correctly.Terminal 2: Run the Square Trajectory (Task 1)Open a new terminal tab, initialize the environment, and run the square path node.Bash# 1. Navigate to the workspace and source the setup
cd /opt/ws
source install/setup.bash

# 2. Run the node
ros2 run lab3 square_path
Terminal 3: Run the Figure-8 Trajectory (Task 2)Stop the previous node (using Ctrl+C), press Reset in RViz2 to clear old lines, and run the figure-8 node.Bash# 1. Source the setup (if in a new terminal)
source install/setup.bash

# 2. Run the node
ros2 run lab3 figure_8_path
Technical Implementation DetailsBoth tasks subscribe to the /model/vehicle_blue/odometry topic to read the robot's state and publish geometry_msgs/TwistStamped messages to the /cmd_vel topic to control its chassis.1. Square Path (square_path.py)Distance Tracking: Calculates the exact Euclidean distance for linear segments using the Pythagorean theorem based on the starting and current (X, Y) coordinates.Angle Tracking: Uses quaternion-to-Euler conversion to track precise 90-degree (pi2 radians) rotations.Inertia Dampening: A "stop-and-go" logic with a 1.5-second dampening pause was implemented. The robot comes to a complete halt before turning to completely eliminate kinetic inertia and wheel drift during sharp corners.2. Figure-8 Path (figure_8_path.py)Continuous Angle Accumulation: Dynamically tracks the accumulated rotation angle to draw perfect circles.Discontinuity Handling: Mathematically normalizes the angular differences using math.atan2(math.sin(diff), math.cos(diff)) to safely handle the discontinuity jump that occurs when the orientation crosses the boundary from pi to pi radians.Execution: The robot continuously drives in a circle until exactly 2pi radians (360 degrees) are accumulated, stops briefly, and then reverses its angular velocity (angular.z) for the second loop.
Control Questions & AnswersWhat is a differential drive?A differential drive is a kinematic system for mobile robots consisting of two independent, driven wheels mounted on a common axis. The robot's linear and angular velocity is controlled entirely by varying the relative speed of these two wheels. If both wheels spin at the same speed, the robot moves straight. If they spin at different speeds (or in opposite directions), the robot turns.Why might the square drift?In a physical simulation (or real life), drift and trajectory deformation occur due to several physical factors:Kinetic Inertia & Momentum: The robot possesses mass. When a stop command is issued, the robot slides slightly forward before fully halting.Wheel Slippage & Friction: The tires may slip against the Gazebo floor, especially during rapid acceleration or turning.Sensor Accumulation Error: Odometry sensors calculate position based on wheel rotations. Over time, tiny measurement errors accumulate, causing the robot's "internal map" to diverge from its actual physical location in the world.(We mitigated these issues by implementing slow movement speeds and forced "cool-down" pauses between maneuvers).
