#!/usr/bin/env python3

from frc_robot_utilities_py_node.RobotStatusHelperPy import RobotStatusHelperPy, Alliance, RobotMode
from frc_robot_utilities_py_node.frc_robot_utilities_py import *
from threading import Thread
import tf2_ros
import rospy
import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 41234
BUFFER_SIZE = 1024
clients = []

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))


def send(msg):
    for c in clients:
        sock.sendto(json.dumps(msg).encode("utf-8"), c)


def send_dashboard_packet():
    global hmi_updates
    global robot_status

    robot_status_data = ""
    if robot_status is not None:
        robot_status_data = robot_status.get_message()

    send({  "robot_status": robot_status_data, 
            "starting_position":["one", "two", "three"],
            "autonomous":["one_disk", "two_disk", "three_disk"]})


def loop():
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        try:
            message, address = sock.recvfrom(BUFFER_SIZE)

            if address not in clients:
                print("New Client: " + str(address))
                clients.append(address)
        except:
            pass

        send_dashboard_packet()

        rate.sleep()


def ros_main(node_name):
    rospy.init_node(node_name)
    register_for_robot_updates()

    t1 = Thread(target=loop)
    t1.start()

    rospy.spin()

    t1.join(5)
