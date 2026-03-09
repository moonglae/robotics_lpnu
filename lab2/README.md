1. Project Repository
   GitHub Link: https://github.com/moonglae/robotics_lpnu/tree/master/lab2

2. Overview and Objectives
   This project demonstrates the seamless integration between the ROS2 ecosystem and the Gazebo simulation environment utilizing the ros_gz_bridge. The primary objective was to configure a custom mobile robot equipped with a LiDAR sensor and develop custom ROS2 Python nodes to control the robot's physical movement while processing its sensor telemetry in real-time.

3. Commands to Run the Simulation
   To compile the workspace and launch the simulation environment along with the custom ROS2 nodes, the following sequence of commands must be executed inside the Docker container (/opt/ws):

Building the package and updating the environment:

Bash
colcon build --packages-select lab2
source install/setup.bash
To run the full simulation, three separate terminals are required:

Terminal 1 (Initializing Gazebo, the communication bridge, and RViz2):

Bash
source install/setup.bash
ros2 launch lab2 gazebo_ros2.launch.py
(Note: Press the 'Play' button in the Gazebo GUI to start the physics engine).

Terminal 2 (Executing the Robot Controller):

Bash
source install/setup.bash
ros2 run lab2 robot_controller
Terminal 3 (Executing the LiDAR Data Subscriber):

Bash
source install/setup.bash
ros2 run lab2 lidar_subscriber 4. Simulation Process and Implementation Details
Step 1: Workspace Setup and Package Creation
The lab2 package was generated utilizing the ament_python build system. To establish a proper connection between ROS2 and the Gazebo simulator, essential dependencies (rclpy, sensor_msgs, geometry_msgs, ros_gz_bridge, and ros_gz_sim) were specified in both the package.xml and setup.py configuration files.

Configuring the Launch File
To streamline the initialization process, a dedicated gazebo_ros2.launch.py script was developed. This launch file acts as a central hub that simultaneously:

Starts the Gazebo simulator with the predefined .sdf world.

Deploys the ros_gz_bridge to seamlessly map the /cmd_vel and /lidar topics between ROS2 and Gazebo.

Opens RViz2 for spatial data and laser scan visualization.

Developing the Kinematic Controller (Publisher Node)
A custom Python Publisher node (robot_controller.py) was designed to govern the robot's physical movement. This script generates and transmits Twist messages to the /cmd_vel topic at a constant rate of 10 Hz (every 0.1s). To demonstrate complex dynamic capabilities, a sinusoidal mathematical function was applied to the angular velocity (Z-axis), forcing the robot to navigate forward following a continuous wavy trajectory.
Implementing the Sensor Reader (Subscriber Node)
Environmental awareness was achieved by creating a Subscriber node (lidar_subscriber.py). This component actively monitors the /lidar topic to intercept incoming LaserScan messages. The node filters the raw laser array, calculates the shortest distance to nearby objects, and includes a critical safety threshold: if an obstacle is detected within a 1.0-meter radius, the system instantly logs a high-priority warning to the terminal.

Conclusion
The laboratory assignment successfully demonstrated the robust integration of ROS2 with the Gazebo simulation environment using the ros_gz_bridge. The developed Python nodes proved effective in establishing programmatic control over the robot's chassis via the /cmd_vel topic, as well as enabling real-time telemetry processing from the /lidar sensor. The data was successfully processed in real-time and visualized using RViz2. The current robotic architecture is fully operational and provides a reliable foundation for implementing advanced autonomous navigation tasks.
