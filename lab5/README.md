# Lab 5: TurtleBot3 Obstacle Avoidance

This repository contains the ROS 2 package for Lab 5 (`lab5`). The goal of this project is to implement an obstacle avoidance algorithm for a TurtleBot3 robot running in a Gazebo simulation environment.

## Prerequisites

This project is configured to run inside a Docker container (`robotics_lpnu` workspace) using **ROS 2 Jazzy**.

Ensure you have the following installed in your environment:

- ROS 2 Jazzy
- TurtleBot3 Simulation Packages

If you are missing the `turtlebot3_gazebo` dependencies, you can install them using `apt`:

```bash
apt update
apt install ros-jazzy-turtlebot3-gazebo
Or use rosdep from the workspace root (/opt/ws):

Bash
rosdep update
rosdep install --from-paths src -y --ignore-src --rosdistro jazzy
Build and Setup
Navigate to your workspace:

Bash
cd /opt/ws
Build the lab5 package:

Bash
colcon build --packages-select lab5
Source the workspace:

Bash
source install/setup.bash
Usage
Before launching the simulation, you must define the TurtleBot3 model you want to use (e.g., burger, waffle, or waffle_pi).

Export the robot model:

Bash
export TURTLEBOT3_MODEL=burger
Launch the obstacle avoidance simulation:

Bash
ros2 launch lab5 obstacle_avoidance_bringup.launch.py
```
