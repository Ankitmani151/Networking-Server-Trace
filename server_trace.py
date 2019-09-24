# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 08:14:00 2019

@author: A691602
"""
from netmiko import ConnectHandler
import time
import os
import re
import getpass
Ip_Name= input ("Enter the ip/name : ")
myCmd = 'tracert -d ' + input ("Enter the IP/name: ") + '>trace.txt | type trace.txt'
output = os.system(myCmd)
print (output)
num_lines = 0
with open("trace.txt") as f:
    for line in f:
        num_lines += 1


# to print a particular line
with open("trace.txt") as f:
    lines = f.readlines()
print("Last Hop is:")
last_hop = (lines[num_lines - 4])
print(last_hop)  # or whatever you want to do with this line
last_ip = last_hop.split()
print("last IP is: " + last_ip[-1])
print (last_ip[-1])
ip1 = last_ip[-1]

#Enter credentials
username=input("Username: ")
password=getpass.getpass()

device = ConnectHandler(device_type='cisco_ios',ip= ip1, username=username,password=password)
print("connection established")
#checking Arp to find mac-address of device
output1 = device.send_command("show ip arp " + Ip_Name,delay_factor=2)
time.sleep(4)
print (output1)
#searching mac-address of device
mac_regex=re.compile(r'[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}')
match_mac=re.search(mac_regex,output1)
mac_add = match_mac[0]
#Mac Address of device
print ("Mac Address of destination device: " + mac_add)

#to check interface connected 
output2 = device.send_command("show mac address-table address " + mac_add,delay_factor=2)
time.sleep(2)
print (output2)

int_regex=re.compile(r'Fa{1}\S*\d/\S*\d{1,2}|Gi{1}\S*\d/\S*\d|Eth{1}\d/\S*\d{1,2}|Te{1}\S*\d/\S*\d|Po{1}\S*\d')
interface_connected = re.search(int_regex,output2)
interface= interface_connected[0]
print (interface)
if 'Po' in interface:
    print("Its a Port-channel")
    output3 = device.send_command("show interface "+ interface,delay_factor=2)
    time.sleep(2)
    print (output3)

#to search interface connected
    int_regex1=re.compile(r'Fa{1}\S*\d/\S*\d{1,2}|Gi{1}\S*\d/\S*\d|Eth{1}\d/\S*\d{1,2}|Te{1}\S*\d/\S*\d')
    interface_connected = re.search(int_regex1,output3)
    interface= interface_connected[0]
    print (interface)
    output4 = device.send_command("show cdp neighbors "+interface+" detail",delay_factor=2)
    time.sleep(2)
    print (output4)
    if "Invalid command" in output4:
        output4=device.send_command("show cdp neighbors interface "+interface+" detail",delay_factor=2)
        print (output4)

#to search next IP address
    ip_regex=re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
    ip_address = re.search(ip_regex,output4)
    next_login_ip = ip_address[0]
    print (next_login_ip)
	
#login into next device
    next_device= ConnectHandler(device_type='cisco_ios',ip= next_login_ip, username=username,password=password)
#checking mac_address table
    output5 = next_device.send_command("show mac address-table address " + mac_add,delay_factor=2)
    time.sleep(4)
    print (output5)

#To search directly connected interface
    int_regex=re.compile(r'Fa{1}\S*\d/\S*\d{1,2}|Gi{1}\S*\d/\S*\d|Eth{1}\d/\S*\d{1,2}|Te{1}\S*\d/\S*\d|Po{1}\S*\d')
    directly_interface_connected = re.search(int_regex,output5)
    direct_interface = directly_interface_connected[0]
    print (direct_interface)


#checking interface details
    output6 = next_device.send_command("show interface "+direct_interface,delay_factor=2)
    time.sleep(2)
    print (output6)	
    next_device.disconnect()
	
else:
    print ("its directly connected interface " + interface)
    output7 = device.send_command("show interface "+ interface,delay_factor=2)
    time.sleep(2)
    print (output7)
	
device.disconnect()

