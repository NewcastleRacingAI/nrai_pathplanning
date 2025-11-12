import rclpy
from rclpy.node import Node

class Perception(Node):

    def __init__(self):
        super().__init__("nrai_pathplanning")
        self.timer = self.create_timer(1, self._timer_callback)

    def _timer_callback(self):
        self.get_logger().info("nrai_pathplanning node is running.")

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Perception()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
