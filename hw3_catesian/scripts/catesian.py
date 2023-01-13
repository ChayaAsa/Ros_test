#!/usr/bin/env python3

import rospy
import moveit_commander
from geometry_msgs.msg import PoseStamped,Pose
from nav_msgs.msg import Path

class catesian_go:

    waypoints = []
    point_list = []


    def __init__(self,group_name):
        rospy.init_node("catesian_go")
        rospy.on_shutdown(self.hook_down)
        rospy.Subscriber("/goal",PoseStamped,self.pose_reciever)
        self.pathpub = rospy.Publisher("/pathpub",Path,queue_size=1)
        self.move_group = moveit_commander.MoveGroupCommander(group_name)

        rospy.logout("\033[1;36mUse 2D Nav Goal to make path then enter if you are finish ")

        while not rospy.is_shutdown():
            go = input()
            if go == '':
                rospy.loginfo("\033[1;36mcompute catesian path")
                self.catesian()
            elif go == 'q':
                rospy.logout("\033[1;36mExit command,restart node")
                rospy.signal_shutdown("exit command")
            else:
                rospy.logwarn("Press enter to compute or 'q' to exit")
        

        rospy.spin()

    def pose_reciever(self,pose_data:PoseStamped):
        pose_data.pose.position.z = 0.5
        self.point_list.append(pose_data)

        path = Path()
        path.header.frame_id = "panda_link0"
        path.header.stamp = rospy.Time.now()
        path.poses = self.point_list

        pose = Pose()
        pose = pose_data.pose
        self.waypoints.append(pose)
        self.pathpub.publish(path)
        rospy.loginfo("If you finish making path,\n     you can press enter to compute or 'q' + enter to quit")

    def catesian(self):
        waypoints = self.waypoints
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)
        self.move_group.execute(plan, wait=True)

        rospy.logout("\033[1;36mComplete task, restarting node")
        rospy.signal_shutdown("Complete all task")
    
    def hook_down(self):
        rospy.logout("\033[1;32mEnding catesian node")

if __name__ == "__main__":
    catesian_go("panda_arm")