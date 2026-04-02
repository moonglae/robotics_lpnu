# Lab 6: Motion Planning for Mobile Robots (Nav2)

## Overview

This repository contains the implementation and configuration of the **Nav2 (Navigation 2) stack** for a TurtleBot3 robot in a simulated environment. The goal of this lab was to tune the navigation parameters to achieve smooth motion, clear local costmap updates, and precise goal reaching.

## Key Tasks

- Integrated Map Server, AMCL localization, and Nav2 Planner/Controller.
- Optimized `nav2_params.yaml` to eliminate costmap drift and unstable robot behavior.
- Adjusted goal tolerances for high-precision parking (up to 0.05m).

## Parameter Tuning Results

| Parameter            | Section         | Value     | Effect                                          |
| :------------------- | :-------------- | :-------- | :---------------------------------------------- |
| `update_frequency`   | `local_costmap` | **5 & 3** | Fixed local map "drift" during rotations.       |
| `max_vel_x`          | `FollowPath`    | **0.2**   | Smoother acceleration and safer navigation.     |
| `xy_goal_tolerance`  | `goal_checker`  | **0.05**  | High-precision arrival at the target point.     |
| `yaw_goal_tolerance` | `goal_checker`  | **0.1**   | Accurate alignment with the target orientation. |

## How to Run

1. **Build the project:**
   ```bash
   cd /opt/ws
   colcon build --packages-select lab6
   source install/setup.bash
   Launch the simulation:
   export TURTLEBOT3_MODEL=burger
   ros2 launch lab6 nav2_room_bringup.launch.py
   In RViz:
   ```

Use 2D Pose Estimate to localize the robot.

Use Nav2 Goal to set the destination.
