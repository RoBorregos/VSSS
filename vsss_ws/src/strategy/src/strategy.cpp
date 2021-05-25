#include "rclcpp/rclcpp.hpp"
#include "vsss_interfaces/msg/vision_topic.hpp"
#include "geometry_msgs/msg/pose.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "geometry_msgs/msg/point.hpp"

class Strategy : public rclcpp::Node {
    public:
        Strategy() : Node("strategy") {
          suscriber_ = this->create_subscription<vsss_interfaces::msg::VisionTopic>("vision_output", 10, 
          std::bind(&Strategy::callbackStrategyListening, this, std::placeholders::_1));  
          RCLCPP_INFO(this->get_logger(), "Strategy Node has started to listen.");
        }
    private:
        void callbackStrategyListening(const vsss_interfaces::msg::VisionTopic::SharedPtr msg) {
            for (auto robot : msg->robot_positions) {
                RCLCPP_INFO(this->get_logger(), "Receiving robot position and speed");
            } RCLCPP_INFO(this->get_logger(), "Ball position received");
        }
        rclcpp::Subscription<vsss_interfaces::msg::VisionTopic>::SharedPtr suscriber_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Strategy>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}