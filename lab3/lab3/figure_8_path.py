#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

class Figure8Odom(Node):
    def __init__(self):
        super().__init__('figure_8_path')
        
        # Налаштування швидкостей
        self.declare_parameter('linear_speed', 0.3)
        self.declare_parameter('angular_speed', 0.5)
        self.declare_parameter('odom_topic', '/model/vehicle_blue/odometry')

        odom_topic = self.get_parameter('odom_topic').value
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.odom_sub = self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)

        # Змінні для відстеження кута
        self.current_theta = 0.0
        self.previous_theta = None
        self.accumulated_angle = 0.0
        self.odom_received = False

    def odom_callback(self, msg: Odometry):
        # Зчитуємо орієнтацію (кватерніон) та перетворюємо у радіани
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        theta = math.atan2(siny, cosy)

        if self.previous_theta is None:
            self.previous_theta = theta

        # Розраховуємо різницю кута з минулого кроку
        delta_theta = theta - self.previous_theta
        
        # Нормалізуємо кут, щоб уникнути стрибка при переході від 3.14 до -3.14
        delta_theta = math.atan2(math.sin(delta_theta), math.cos(delta_theta))

        self.accumulated_angle += delta_theta
        self.previous_theta = theta
        self.odom_received = True

    def wait_for_odom(self):
        self.get_logger().info("Очікування даних одометрії...")
        while rclpy.ok() and not self.odom_received:
            rclpy.spin_once(self, timeout_sec=0.1)

    def stop_robot(self):
        # Зупинка та гасіння інерції
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        cmd.twist.linear.x = 0.0
        cmd.twist.angular.z = 0.0
        self.pub.publish(cmd)
        
        # Пауза пів секунди
        for _ in range(10):
            rclpy.spin_once(self, timeout_sec=0.05)

    def draw_circle(self, direction="left"):
        linear_speed = self.get_parameter('linear_speed').value
        angular_speed = self.get_parameter('angular_speed').value

        if direction == "right":
            angular_speed = -angular_speed

        # Скидаємо накопичений кут перед новим колом
        self.accumulated_angle = 0.0
        target_angle = 2.0 * math.pi  # 360 градусів у радіанах

        cmd = TwistStamped()
        cmd.header.frame_id = 'base_link'

        self.get_logger().info(f"Малюю коло ({direction})...")
        
        while rclpy.ok():
            # Перевіряємо, чи проїхали ми повні 360 градусів (незалежно від напрямку)
            if abs(self.accumulated_angle) >= target_angle:
                break
            
            cmd.twist.linear.x = linear_speed
            cmd.twist.angular.z = angular_speed
            cmd.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.05)

        self.stop_robot()

    def execute_figure_8(self):
        self.wait_for_odom()
        self.get_logger().info("Починаю малювати вісімку за одометрією!")
        
        # Малюємо перше коло вліво
        self.draw_circle("left")
        
        # Малюємо друге коло вправо
        self.draw_circle("right")
        
        self.get_logger().info("Вісімка успішно завершена!")

def main(args=None):
    rclpy.init(args=args)
    node = Figure8Odom()
    try:
        node.execute_figure_8()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()