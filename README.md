<img src="docs/images/roborregos_logo.png" width="400" ><img> 

# Very Small Sized Soccer (VSSS)           

The LARC IEEE VSSS competition consists of the development of a computer vision and communication system which controls a group of autonomous robots, coordinating their movements according to a collaborative soccer strategy.

## Table of contents

- [Very Small Sized Soccer (VSSS)](#very-small-sized-soccer-(vsss))
  - [Table of contents](#table-of-contents)
  - [Project details](#project-details-[wip])
  - [Project setup](#project-setup)
    - [Running Modules](#running-modules-[wip])
      - [Path finding](#path-finding)
      - [Computer vision](#computer-vision)
      - [Exit application](#exit-application)
  - [Development team](#development-team)

## Project Details [WIP]

This project is made using [ROS2](https://docs.ros.org/en/foxy/index.html), wich runs python and c++ scripts; For vision algorithms we use [OpenCV2](https://opencv.org/).

For more information about project management and standards you can check our [wiki](https://github.com/RoBorregos/VSSS/wiki).


## Project setup

Before setting up the project, you should have installed the following development tools:

- [ROS2 FOxy Fitzroy](https://docs.ros.org/en/foxy/Installation.html)
- [OpenCV2](https://docs.opencv.org/master/d9/df8/tutorial_root.html)https://docs.opencv.org/master/d9/df8/tutorial_root.html
- [Arduino](https://www.arduino.cc/en/software)

Once you have installed the required third-party software, you can follow this steps:

1. Clone the project repository on your local machine.

   SSH:

   ```bash
   $ git clone --recurse-submodules https://github.com/RoBorregos/VSSS.git
   ```

2. Enter __/vsss_ws__ and install all dependencies using rosdep:

   ```bash
   $ rosdep install --from-paths src --ignore-src --rosdistro foxy -y --skip-keys "console_bridge fastcdr fastrtps libopensplice67 libopensplice69 rti-connext-dds-5.3.1 urdfdom_headers"
   ```

## Running modules [WIP]

To build ROS packages, first run inside the __/vsss_ws__:

```bash
$ colcon build --symlink-install
```

Source the code:

```bash
$ source install/setup.bash
```

### Path finding

```bash
$ ros2 run path_planning path_planning_main
```

### Computer vision
To get information from camera use the image_publisher package with the video port (file) as parameter:

```bash
$ ros2 run image_publisher image_publisher_node /dev/video0
```

To run vision demo:

```bash
$ ros2 run vision demo 
```

PS: You can check other cameras by running:
```bash
$ ls /dev/video*
```

### Exit application
Use `Ctrl + C` to exit the logs and turn all nodes and application down.

*TODO: General launch file for whole system*

## Development team

| Name                    | Email                                                               | Github                                                       | Role      |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------ | --------- |
| Miguel Elizondo | [pev@live.com.mx](mailto:pev@live.com.mx) | [@Miguelelizondov](https://github.com/Miguelelizondov) | PM & Strategy |
| Keven Arroyo | [dake.3601@gmail.com](mailto:dake.3601@gmail.com) | [@dake3601](https://github.com/dake3601) | Path finding |
| Aurora Tijerina | [auro.tj@gmail.com](mailto:auro.tj@gmail.com)                       | [@AuroTB](https://github.com/aurotb)                         | Integration mentor |

