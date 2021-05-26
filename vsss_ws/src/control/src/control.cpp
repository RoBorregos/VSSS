#include "rclcpp/rclcpp.hpp"
#include "vsss_interfaces/msg/path_planning_topic.hpp"
#include "geometry_msgs/msg/pose.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "geometry_msgs/msg/point.hpp"

class Control : public rclcpp::Node {
    public:
        Control() : Node("control") {
          suscriber_ = this->create_subscription<vsss_interfaces::msg::PathPlanningTopic>("path_planning_output", 10, 
          std::bind(&Control::callbackStrategyListening, this, std::placeholders::_1));
          
          RCLCPP_INFO(this->get_logger(), "Control Node has started to listen.");
        }
    private:
        void callbackStrategyListening(const vsss_interfaces::msg::PathPlanningTopic::SharedPtr msg) {
            for (auto robot : msg->trajectories) {
                RCLCPP_INFO(this->get_logger(), "Receiving robot trajectory");
            } RCLCPP_INFO(this->get_logger(), "All robots trajectories received");
        }
        rclcpp::Subscription<vsss_interfaces::msg::PathPlanningTopic>::SharedPtr suscriber_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Control>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}