#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        
        # Створюємо підписника на топік лідара
        self.subscription = self.create_subscription(
            LaserScan,
            '/lidar',
            self.lidar_callback,
            10
        )
        self.get_logger().info('Читач лідара запущено! Чекаю на перешкоди...')

    def lidar_callback(self, msg):
        # Фільтруємо коректні значення відстаней
        valid_ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        
        if valid_ranges:
            min_distance = min(valid_ranges)
            
            # Якщо до перешкоди менше 1 метра - видаємо попередження!
            if min_distance < 1.0:
                self.get_logger().warn(f'УВАГА! Перешкода дуже близько: {min_distance:.2f} м!')
            elif len(valid_ranges) % 50 == 0: # Щоб не спамити, виводимо інфо рідше
                 self.get_logger().info(f'Найближча перешкода: {min_distance:.2f} м')

def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()