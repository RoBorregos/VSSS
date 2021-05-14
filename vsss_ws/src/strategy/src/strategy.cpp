#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class Strategy : public rclcpp::Node {
    public:
        Strategy() : Node("strategy") {
          suscriber_ = this->create_subscription<example_interfaces::msg::String>("vision_output", 10, 
          std::bind(&Strategy::callbackStrategyListening, this, std::placeholders::_1));  
          RCLCPP_INFO(this->get_logger(), "Strategy Node has started to listen.");
        }
    private:
        void callbackStrategyListening(const example_interfaces::msg::String::SharedPtr msg) {
            RCLCPP_INFO(this->get_logger(), "%s", msg->data.c_str());
        }
        rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr suscriber_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Strategy >();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}