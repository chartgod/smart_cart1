# 실행

* 가상환경 slam 실행

    $ roscore
    $ roslaunch testbot_gazebo kobuki.launch
    $ roslaunch kobuki_slam kobuki_slam.launch
    $ rosrun rviz rviz -d `rospack find kobuki_slam`/rviz/kobuki_slam

* 실제환경 slam 실행
    * gl lidar 연결

        $ sudo chmod 777 /dev/ttyUSB1
        $ roslaunch gl_ros_driver gl_ros_driver.launch
        
    $ roslaucnh kobuki_node minimal.launch
    $ roslaunch kobuki_slam kobuki_slam.launch
    $ rosrun rviz rviz -d `rospack find kobuki_slam`/rviz/kobuki_slam