#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import PoseStamped
from hw1_draw.srv import draw


class rdraw:

    __count = 0
    __sudden_death = False
    _min = 0
    __first_post = PoseStamped()
    __end = False
    
    def __init__(self, end_distance):
        self._min = end_distance

        rospy.init_node('artist')
        rospy.loginfo("Start node artist")
        rospy.on_shutdown(self.hook_down)
        # rospy.wait_for_message("/move_base_simple/goal",PoseStamped)
        rospy.Subscriber("/move_base_simple/goal",PoseStamped,self.draw_req)
        rospy.spin() 

    def draw_req(self,rpost):
        first = False
        end   = False
        post  = rpost

        rospy.wait_for_service('/assign/draw')
        try:
            draw_service = rospy.ServiceProxy('/assign/draw',draw)
            if self.__count == 0:
                first = True
                self.__first_post = post

            if self.__sudden_death == True:
                end = True
                post = self.__first_post
                self.__end = True

            response = draw_service(pose=post,first=first,end=end)
            distance = response.lenght
            rospy.loginfo("distance is: "+str(distance))

            _to_first = math.sqrt((self.__first_post.pose.position.x-post.pose.position.x)**2+
                                  (self.__first_post.pose.position.y-post.pose.position.y)**2+
                                  (self.__first_post.pose.position.z-post.pose.position.z)**2)

            if _to_first < self._min and self.__count > 1 :
                self.__sudden_death = True
            
            self.__count += 1

        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s"%e)

        if self.__end:
            rospy.signal_shutdown("Complete the picture")

    def hook_down(self):
        rospy.loginfo("Shutdown artist node")

if __name__ == "__main__":
    end_distance = 1.0
    rvizdrawer = rdraw(end_distance)