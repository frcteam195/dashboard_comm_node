#!/usr/bin/env python3

import tf2_ros
import rospy
import socket
import json
import random

UDP_IP = "127.0.0.1"
UDP_PORT = 41234
BUFFER_SIZE  = 1024
clients = [];

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket( socket.AF_INET,
                      socket.SOCK_DGRAM )

sock.setblocking(0)
sock.bind( (UDP_IP, UDP_PORT) )

def send(msg):
    for c in clients:
        sock.sendto( json.dumps(msg).encode("utf-8"), c )

def got_veh_state():
    testValue = random.randint(0, 3000)
    send( {"value": testValue} )

def ros_main(node_name):
    rospy.init_node(node_name)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        try:
            bytesAddressPair = sock.recvfrom(BUFFER_SIZE)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            if address not in clients:
                print("New Client: " + str(address))
                clients.append(address);
        except:
            pass

        got_veh_state();

        rate.sleep()
