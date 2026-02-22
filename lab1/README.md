Project: Building a Robot in Gazebo

To ensure a successful simulation and data verification, please follow these steps using three separate terminal windows.

Terminal 1: Environment Initialization & GUI
This terminal starts the Docker container and launches the Gazebo simulation environment.
Navigate to the project directory:
cd ~/robotics_lpnu
Start the Docker container:
./scripts/cmd run
Launch the Gazebo world:
gz sim src/code/lab1/worlds/robot.sdf
Note: Once the Gazebo window appears, you must click the orange Play button in the bottom-left corner to start the physics engine and enable the sensors.
Terminal 2: Motion Control (Teleoperation)
This terminal is used to send velocity commands to the robot's differential drive system.

Enter the active container:
cd ~/robotics_lpnu
./scripts/cmd bash
Publish a movement command:
gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 1.0}, angular: {z: 0.5}"
Linear x: 1.0: Sets the forward velocity to 1 m/s.Angular z: 0.5: Commands the robot to turn left, creating a curved trajectory towards the obstacles.
Terminal 3: Sensor Data Verification
This terminal confirms that the LiDAR sensor is actively scanning the environment and publishing data.

Enter the active container:
cd ~/robotics_lpnu
./scripts/cmd bash
Monitor the LiDAR topic:
gz topic -e -t /lidar
You will see a live stream of the ranges array.

As the robot approaches the red_box or gray_wall, the numerical values in the ranges list will decrease, reflecting the real-time distance to the objects.
Troubleshooting & Tips
Command Not Found: If the gz command is not recognized, ensure you have entered the Docker shell using ./scripts/cmd bash.

Stationary Robot: If the robot does not move after sending a command, check if the Play button in the Gazebo GUI has been pressed.

LiDAR Visualization: To see the laser rays in the 3D view, enable the Visualize Lidar plugin from the right-hand plugins menu in Gazebo.
