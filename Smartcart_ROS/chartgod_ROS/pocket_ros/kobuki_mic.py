# -*- coding: utf-8 -*-
import os
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from pocketsphinx import LiveSpeech, get_model_path

rospy.init_node('pocket_sphinx_controller', anonymous=True)
kobuki_velocity_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)


#a,c (x,y)pose check
def process_sphinx_result(sphinx_output):
    kobuki_twist = Twist()

    if sphinx_output == "a":
        kobuki_twist.linear.x = 0.3
        kobuki_twist.angular.z = 0.0
    elif sphinx_output == "b":
        kobuki_twist.linear.x = -0.5
        kobuki_twist.angular.z = 0.0
    elif sphinx_output == "c":
        kobuki_twist.linear.x = 0.0
        kobuki_twist.angular.z = 1.0
    else:
        kobuki_twist.linear.x = 0.0
        kobuki_twist.angular.z = 0.0

    return kobuki_twist

def get_sphinx_output():
    model_path = get_model_path()
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=44100, #16000, 2048 use O
        buffer_size=4096,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, '/home/chart/.local/lib/python3.8/site-packages/pocketsphinx/model/en-us/en-us'),
        lm=os.path.join(model_path, '/home/chart/.local/lib/python3.8/site-packages/pocketsphinx/model/en-us/en-us.lm.bin'),
        dic=os.path.join(model_path,'/home/chart/catkin_ws/src/my_dict.dict')
    )
    
    for phrase in speech:
        return str(phrase).lower().strip()
    
def callback(data):
    sphinx_output = data.data
    kobuki_twist = process_sphinx_result(sphinx_output)
    kobuki_velocity_pub.publish(kobuki_twist)

dict_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "/home/chart/catkin_ws/src/my_dict.dict")
print("사용 중인 사전 파일 경로:", dict_path)

if __name__ == '__main__':
    rate = rospy.Rate(10)  # 10Hz
    rospy.Subscriber('/recognizer/output', String, callback)
    while not rospy.is_shutdown():
        sphinx_output = get_sphinx_output()
        kobuki_twist = process_sphinx_result(sphinx_output)
        kobuki_velocity_pub.publish(kobuki_twist)
        rate.sleep()
    rospy.spin()
