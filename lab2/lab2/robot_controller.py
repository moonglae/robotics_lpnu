#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # Створюємо видавця, який буде відправляти команди швидкості
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Таймер, який викликає функцію кожні 0.1 секунди
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0
        self.get_logger().info('Контролер запущено! Робот починає рух...')

    def timer_callback(self):
        msg = Twist()
        
        # Задаємо швидкість: 0.5 м/с вперед, і СИЛЬНИЙ хвилеподібний поворот
        msg.linear.x = 0.5  
        msg.angular.z = 1.2 * math.sin(self.counter * 0.1)  
        
        # Публікуємо повідомлення
        self.publisher.publish(msg)
        self.counter += 1
        
        if self.counter % 50 == 0:
            self.get_logger().info(f'Їду: швидкість={msg.linear.x:.2f}, поворот={msg.angular.z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()