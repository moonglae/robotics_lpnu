import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    # Шляхи до пакетів
    turtlebot3_gazebo_share = get_package_share_directory("turtlebot3_gazebo")
    ros_gz_sim_share = get_package_share_directory("ros_gz_sim")
    lab5_share = get_package_share_directory("lab5")

    # Шлях до нашого світу
    world_file = "/opt/ws/src/code/lab3/turtlebot3/worlds/room.sdf"

    # 1. Запуск Gazebo (Сервер + Клієнт одним викликом)
    # Аргументи: -r (автозапуск), -v 4 (детальні логи), і шлях до світу
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": f"-r -v 4 {world_file}"
        }.items(),
    )

    # 2. Robot State Publisher (щоб RViz бачив робота)
    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_share, "launch", "robot_state_publisher.launch.py")
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    # 3. Спавн робота TurtleBot3
    spawn_turtlebot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_share, "launch", "spawn_turtlebot3.launch.py")
        ),
        launch_arguments={"x_pose": "0.0", "y_pose": "0.0"}.items(),
    )

    # 4. МІСТОК (Bridge) — БЕЗ НЬОГО РОБОТ НЕ ПОЇДЕ
    # Передає /cmd_vel, /scan та /odom між ROS та Gazebo
    # Оновлений місток: додаємо /tf та /joint_states
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        parameters=[{'qos_overrides./tf.publisher.reliability': 'reliable'}],
        output='screen'
    )

    # Додаємо вузол, який з'єднує частини робота (якщо його немає)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    # 5. RViz (візуалізація лідара)
    rviz_config = os.path.join(lab5_share, "rviz", "obstacle_avoidance.rviz")
    rviz = ExecuteProcess(
        cmd=["rviz2", "-d", rviz_config],
        output="screen"
    )

    return LaunchDescription([
        # Встановлюємо модель робота
        SetEnvironmentVariable(name="TURTLEBOT3_MODEL", value="burger"),
        # Допомагаємо Gazebo знайти моделі TurtleBot
        SetEnvironmentVariable(
            name="GZ_SIM_RESOURCE_PATH", 
            value=os.path.join(turtlebot3_gazebo_share, "models")
        ),
        
        gz_sim,
        robot_state_publisher,
        spawn_turtlebot,
        bridge,
        rviz
    ])