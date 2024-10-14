#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class ControlNode(Node):
    def __init__(self) -> None:
        # Initialize base class
        super().__init__("control_node")
        
        # Create a publisher for the /cmd_vel topic with Twist message type
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        
        # Create a timer that calls the control_callback every 0.2 seconds
        self.control_timer = self.create_timer(0.2, self.control_callback)
        
        # Create a subscription for the /kill topic
        self.kill_sub = self.create_subscription(Bool, "/kill", self.kill_callback, 10)

    def control_callback(self) -> None:
        """
        Callback function that publishes a constant Twist message
        """
        # Create and initialize a Twist message
        msg = Twist()
        msg.linear.x = 1.0  # Set linear velocity (m/s)
        msg.angular.z = 0.5  # Set angular velocity (rad/s)

        # Publish the Twist message
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info("Publishing Twist message: linear.x = %.2f, angular.z = %.2f" % (msg.linear.x, msg.angular.z))

    def kill_callback(self, msg: Bool) -> None:
        """
        Callback function that stops the control when a kill signal is received
        """
        if msg.data:
            self.get_logger().info("Received kill signal. Stopping control.")
            self.control_timer.cancel()  # Stop the timer

            # Publish a zero control message to /cmd_vel
            stop_msg = Twist()
            stop_msg.linear.x = 0.0  # Zero linear velocity
            stop_msg.angular.z = 0.0  # Zero angular velocity
            self.cmd_vel_pub.publish(stop_msg)

            self.get_logger().info("Publishing stop message: linear.x = %.2f, angular.z = %.2f" % (stop_msg.linear.x, stop_msg.angular.z))

if __name__ == "__main__":
    rclpy.init()        # Initialize ROS2 context
    node = ControlNode()  # Instantiate the control node
    rclpy.spin(node)    # Use ROS2 built-in scheduler for executing the node
    rclpy.shutdown()    # Cleanly shutdown ROS2 context
