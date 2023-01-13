#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

rospy.init_node("haiufj")
pub = rospy.Publisher("topic",Path,queue_size=1)

print("dawda")
pose1 = PoseStamped()
pose2 = PoseStamped()

pose1.pose.position.x = 1
# pose1.header.frame_id = "map"
# pose1.header.stamp = rospy.Time.now()
# pose1.pose.position.y = 0

pose2.pose.position.y = 1
# pose2.header.frame_id = "map"
# pose2.header.stamp = rospy.Time.now()

path = Path()

path.poses = [pose1,pose2]
path.header.frame_id = "map"
# path.header.stamp = rospy.Time.now()
print(path)
rospy.sleep(5)
pub.publish(path)


rospy.spin()