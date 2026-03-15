import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import math
import time

class CirclePath(Node):
    def __init__(self):
        super().__init__('circle_path')
        
        # Параметри
        self.declare_parameter("linear_speed", 0.4)
        self.declare_parameter("angular_speed", 0.4)
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        
        v = self.get_parameter("linear_speed").value
        w = self.get_parameter("angular_speed").value
        
        # Розрахунок часу: 2*PI / кутову швидкість + запас на інерцію
        duration = (2.0 * math.pi / abs(w)) + 10.0
        
        self.get_logger().info(f"Запуск: v={v}, w={w}. Чекаю {duration:.2f} сек (Sim Time)")

        # Чекаємо, поки з'явиться час у симуляції (якщо вона на паузі)
        while self.get_clock().now().nanoseconds == 0:
            self.get_logger().info("Чекаю на запуск симуляції...")
            time.sleep(0.5)

        start_time = self.get_clock().now()
        
        msg = TwistStamped()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = float(v)
        msg.twist.angular.z = float(w)

        # Цикл керування
        while rclpy.ok():
            current_time = self.get_clock().now()
            elapsed = (current_time - start_time).nanoseconds / 1e9
            
            if elapsed >= duration:
                break
            
            msg.header.stamp = current_time.to_msg()
            self.pub.publish(msg)
            
            rclpy.spin_once(self, timeout_sec=0.05)

        # Зупинка
        stop_msg = TwistStamped()
        stop_msg.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(stop_msg)
        self.get_logger().info("Коло завершено!")

def main(args=None):
    rclpy.init(args=args)
    node = CirclePath()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()