#include <cmath>
#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <visualization_msgs/MarkerArray.h>
#include <visualization_msgs/Marker.h>
#include <rviz_visual_tools/rviz_visual_tools.h>
#include <hw1_draw/draw.h>

class drawing_service
{
    private:
        // std var
        int counter = 0;
        float distance;
        bool end = false;

        // ros var
        ros::NodeHandle nh;
        ros::ServiceServer drawing_server;
        // tools var
        rviz_visual_tools::RvizVisualToolsPtr visual_tools_;
        // msg
        geometry_msgs::Pose newP;
        geometry_msgs::Pose oldP;
        std::vector<geometry_msgs::Pose> path;
        // visualization_msgs::Marker marker;
        // visualization_msgs::MarkerArray allmarker;
        // std::vector<visualization_msgs::Marker> vecmarker;
    
    public:
        drawing_service():nh("~")
        {
            visual_tools_.reset(new rviz_visual_tools::RvizVisualTools("map","/rviz_visual_markers"));
            drawing_server = nh.advertiseService("/assign/draw",&drawing_service::drawing,this);
            while(ros::ok()){
                if(end == true){
                    break;
                }
            }
        }

        bool drawing(hw1_draw::draw::Request &req, hw1_draw::draw::Response &res)
        {
            newP = req.pose.pose;
            path.push_back(newP);
            // marker.header.frame_id = "map";
            // marker.header.stamp = ros::Time::now();
            // marker.type = visualization_msgs::Marker::SPHERE;
            // marker.pose = newP;
            // marker.color.a = 1.0;
            // marker.color.b = 1.0;
            // marker.color.g = 0.0;
            // marker.color.r = 0.0;
            // marker.action = visualization_msgs::Marker::ADD;
            // vecmarker.push_back(marker);
            // allmarker.markers = vecmarker;
            

            visual_tools_->publishPath(path,rviz_visual_tools::colors::GREEN,rviz_visual_tools::scales::XXLARGE);
            // visual_tools_->publishMarkers(allmarker);
            visual_tools_->trigger();

            if (req.first==true){
                res.lenght = 0;
            }
            else{
                distance = sqrt(pow(newP.position.x-oldP.position.x,2)+
                                pow(newP.position.y-oldP.position.y,2)+
                                pow(newP.position.z-oldP.position.z,2));
                res.lenght = distance;

                if (req.end==true){
                    end = true;
                }
            }
            oldP = req.pose.pose;

            return true;
        }

};


int main(int argc, char **argv)
{
    ros::init(argc, argv, "drawing");
    ros::AsyncSpinner spinner(0);

    spinner.start();
    ROS_INFO_STREAM("Start drawing node");
    drawing_service service;
    

    ROS_INFO_STREAM("Ending drawing node");
    
    return 1;
}