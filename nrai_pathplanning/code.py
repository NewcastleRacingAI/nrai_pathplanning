def process_pose(msg: object) -> object:
    print(f"I'm now at position: {msg.pose.position} with orientation: {msg.pose.orientation}")
    return msg


def process_imu(msg: object) -> object:
    print(f"IMU data - Linear Acceleration: {msg.linear_acceleration}, Angular Velocity: {msg.angular_velocity}")
    return msg
