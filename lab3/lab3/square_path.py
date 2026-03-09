#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

class SquarePath(Node):
    def __init__(self):
        super().__init__('square_path')
        self.declare_parameter('side_length', 1.5)
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('angular_speed', 0.15)
        self.declare_parameter('odom_topic', '/model/vehicle_blue/odometry')

        odom_topic = self.get_parameter('odom_topic').value
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.odom_sub = self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.odom_received = False

    def odom_callback(self, msg: Odometry):
        # Зчитуємо координати
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        # Перетворюємо кватерніон у звичайний кут (радіани)
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_theta = math.atan2(siny, cosy)
        self.odom_received = True

    def wait_for_odom(self):
        self.get_logger().info("Очікування даних одометрії від симулятора...")
        while rclpy.ok() and not self.odom_received:
            rclpy.spin_once(self, timeout_sec=0.1)

    def move_forward(self, distance):
        start_x = self.current_x
        start_y = self.current_y
        speed = self.get_parameter('linear_speed').value
        cmd = TwistStamped()
        cmd.header.frame_id = 'base_link'

        self.get_logger().info(f"Їду вперед на {distance} метрів...")
        while rclpy.ok():
            # Розрахунок пройденої відстані за теоремою Піфагора
            dx = self.current_x - start_x
            dy = self.current_y - start_y
            traveled = math.sqrt(dx*dx + dy*dy)
            
            if traveled >= distance:
                break
            
            cmd.twist.linear.x = speed
            cmd.header.stamp = self.get_clock().now().to_msg() # Оновлюємо час постійно!
            self.pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.05)

        self.stop_robot()

    def turn(self, angle):
        start_theta = self.current_theta
        speed = self.get_parameter('angular_speed').value
        cmd = TwistStamped()
        cmd.header.frame_id = 'base_link'

        self.get_logger().info("Повертаю на 90 градусів...")
        while rclpy.ok():
            diff = self.current_theta - start_theta
            # Безпечна нормалізація кута (захист від стрибків 3.14 -> -3.14)
            diff = math.atan2(math.sin(diff), math.cos(diff))
            
            if abs(diff) >= angle:
                break
            
            cmd.twist.angular.z = speed
            cmd.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.05)

        self.stop_robot()

    def stop_robot(self):
        # Повна зупинка та пауза для гасіння інерції
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        cmd.twist.linear.x = 0.0
        cmd.twist.angular.z = 0.0
        self.pub.publish(cmd)
        
        # Чекаємо пів секунди, щоб робот перестав ковзати
        for _ in range(10):
            rclpy.spin_once(self, timeout_sec=0.05)

    def execute_square(self):
        self.wait_for_odom()
        side = self.get_parameter('side_length').value
        
        for i in range(4):
            self.get_logger().info(f"--- Сторона {i+1} з 4 ---")
            self.move_forward(side)
            self.turn(math.pi / 2.0)
            
        self.get_logger().info("Квадрат за одометрією успішно завершено!")

def main(args=None):
    rclpy.init(args=args)
    node = SquarePath()
    try:
        # Запускаємо логіку ззовні, а не в __init__
        node.execute_square()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()