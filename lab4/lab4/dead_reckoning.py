#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, PoseStamped 
from nav_msgs.msg import Odometry, Path

class DeadReckoningNode(Node):
    def __init__(self):
        super().__init__("dead_reckoning")

        # Оголошення параметрів
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("ground_truth_topic", "/model/vehicle_blue/odometry")
        self.declare_parameter("path_dr_topic", "/path_dr")
        self.declare_parameter("frame_id", "odom")
        self.declare_parameter("max_poses", 2000)

        cmd_topic = self.get_parameter("cmd_vel_topic").value
        gt_topic = self.get_parameter("ground_truth_topic").value
        path_topic = self.get_parameter("path_dr_topic").value
        self.frame_id = self.get_parameter("frame_id").value
        self.max_poses = int(self.get_parameter("max_poses").value)

        # Підписки та паблішер
        self.create_subscription(TwistStamped, cmd_topic, self.cmd_callback, 10)
        self.create_subscription(Odometry, gt_topic, self.gt_callback, 10)
        self.pub_path = self.create_publisher(Path, path_topic, 10)

        # Змінні стану
        self.x = None
        self.y = None
        self.theta = None
        self.last_time = None
        self.gt_x = 0.0
        self.gt_y = 0.0

        # Повідомлення шляху
        self.path_msg = Path()
        self.path_msg.header.frame_id = self.frame_id

    def gt_callback(self, msg: Odometry):
        # Оновлюємо реальні координати для розрахунку похибки
        self.gt_x = msg.pose.pose.position.x
        self.gt_y = msg.pose.pose.position.y

        # Синхронізація при першому отриманні даних
        if self.x is None:
            self.x = self.gt_x
            self.y = self.gt_y
            q = msg.pose.pose.orientation
            siny = 2.0 * (q.w * q.z + q.x * q.y)
            cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
            self.theta = math.atan2(siny, cosy)
            self.get_logger().info("Стартову позицію синхронізовано з Ground Truth.")

    def cmd_callback(self, msg: TwistStamped):
        if self.x is None:
            return

        # Розрахунок дельта t (dt)
        current_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        if self.last_time is None:
            self.last_time = current_time
            return

        dt = current_time - self.last_time
        self.last_time = current_time

        # Отримання швидкостей
        v = msg.twist.linear.x
        w = msg.twist.angular.z

        # Математичне інтегрування (Dead Reckoning)
        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt
        self.theta += w * dt
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        # Створення Pose для Path
        pose = PoseStamped()
        pose.header = msg.header
        pose.header.frame_id = self.frame_id
        pose.pose.position.x = self.x
        pose.pose.position.y = self.y
        pose.pose.orientation.w = math.cos(self.theta / 2.0)
        pose.pose.orientation.z = math.sin(self.theta / 2.0)

        self.path_msg.poses.append(pose)
        
        # Обмеження довжини шляху в RViz
        if len(self.path_msg.poses) > self.max_poses:
            self.path_msg.poses.pop(0)

        self.path_msg.header.stamp = msg.header.stamp
        self.pub_path.publish(self.path_msg)

        # Розрахунок дрейфу (похибки)
        error = math.sqrt((self.x - self.gt_x)**2 + (self.y - self.gt_y)**2)
        self.get_logger().info(f"Drift Error: {error:.4f} m")

# ТОЧКА ВХОДУ (ОБОВ'ЯЗКОВО ПОЗА КЛАСОМ)
def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()