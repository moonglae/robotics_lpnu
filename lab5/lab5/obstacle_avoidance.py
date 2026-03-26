import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')

        # Ціль попереду
        self.declare_parameter('goal_x', 6.0)
        self.goal_x = self.get_parameter('goal_x').value

        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.control_loop)

        self.current_x, self.current_y, self.current_yaw = 0.0, 0.0, 0.0
        self.scan_ranges = []

        # НАЛАШТУВАННЯ ДЛЯ ОБ'ЇЗДУ
        self.k_att = 1.2        # Тяжіння вперед
        self.k_rep = 0.1        # Слабке відштовхування назад (щоб не тікав)
        self.k_side = 5.0       # СИЛЬНИЙ ТАНГЕНС (штовхає вбік)
        self.obs_dist = 0.5     # Радіус реакції (50 см)
        self.min_dist = 0.18    # Ігноруємо свій корпус

    def odom_cb(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.current_yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))

    def scan_cb(self, msg):
        self.scan_ranges = msg.ranges
        self.a_min, self.a_inc = msg.angle_min, msg.angle_increment

    def control_loop(self):
        if not self.scan_ranges: return

        # Відстань до цілі
        dist = math.hypot(self.goal_x - self.current_x, 0.0 - self.current_y)
        if dist < 0.3:
            self.get_logger().info("DONE!"); self.cmd_pub.publish(Twist()); return

        # 1. СИЛА ПРИТЯГАННЯ (Локальна)
        # Рахуємо кут на ціль відносно "носа" робота
        angle_to_goal = math.atan2(0.0 - self.current_y, self.goal_x - self.current_x) - self.current_yaw
        f_x = self.k_att * math.cos(angle_to_goal)
        f_y = self.k_att * math.sin(angle_to_goal)

        # 2. ТАНГЕНЦІАЛЬНИЙ ОБ'ЇЗД
        # Шукаємо найближчу точку
        for i, r in enumerate(self.scan_ranges):
            if self.min_dist < r < self.obs_dist:
                angle_rel = self.a_min + i * self.a_inc
                
                # Потужність впливу
                rep = (1.0/r - 1.0/self.obs_dist)
                
                # ТАНГЕНС: змушує об'їжджати, а не тікати
                f_x -= self.k_side * rep * math.sin(angle_rel)
                f_y += self.k_side * rep * math.cos(angle_rel)
                
                # Невеличке відштовхування назад для безпеки
                f_x -= self.k_rep * rep * math.cos(angle_rel)

        # 3. КЕРУВАННЯ
        target_yaw = math.atan2(f_y, f_x)
        yaw_err = math.atan2(math.sin(target_yaw - self.current_yaw), math.cos(target_yaw - self.current_yaw))

        msg = Twist()
        msg.angular.z = max(-1.2, min(1.2, 3.5 * yaw_err))
        msg.linear.x = 0.15 if abs(yaw_err) < 0.6 else 0.02
        self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args); node = ObstacleAvoidanceNode(); rclpy.spin(node); rclpy.shutdown()