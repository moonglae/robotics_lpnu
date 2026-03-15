# Lab 4: Dead Reckoning Report

## 1. Goal

The objective of this lab was to implement a dead reckoning pose estimation for a differential drive robot and compare it with the ground truth (odometry) provided by the Gazebo simulator.

## 2. Implementation details

The pose estimation was implemented in `dead_reckoning.py`. The robot's pose (x, y, theta) is updated at each time step based on the commanded linear velocity (v) and angular velocity (w) using the following motion model:

- x*new = x + v * cos(theta) \_ dt
- y*new = y + v * sin(theta) \_ dt
- theta_new = theta + w \* dt

Parameters used:

- Linear Speed: 0.4 m/s
- Angular Speed: 0.4 rad/s

## 3. Results

The robot successfully executed a circle trajectory. RViz showed two paths:

- Green Path: Ground Truth (actual position from Gazebo).
- Red Path: Dead Reckoning (estimated position from our script).

## 4. Why does dead reckoning drift?

We observed a Drift Error in the terminal (approx 1.97m). This happens because:

1. Integration Errors: Small errors in each time step accumulate. Since each new pose depends on the previous one, the error grows over time.
2. Physics vs Math: The mathematical model is ideal. It doesn't account for robot inertia, wheel slip, or friction that exists in Gazebo.
3. No Feedback: Dead reckoning is an open-loop system. Without external sensors like LiDAR or GPS to correct the position, the error cannot be reset.

## 5. How to run

### Step 1: Build the workspace

Navigate to your workspace root and build the packages:
cd /opt/ws
colcon build --packages-select lab3 lab4
source install/setup.bash
ros2 launch lab3 bringup.launch.py
Step 2: Launch the simulation
Terminal 1: Start Gazebo, RViz, and the dead reckoning node:
ros2 launch lab4 dead_reckoning_bringup.launch.py
Step 3: Run the trajectory
Terminal 2: Start the robot movement:
ros2 run lab3 circle_path
