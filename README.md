# Networking-Server-Trace
Cisco IP trace
This Python script will take allow you to enter a single IP and trace the associated MAC address(es) from a core Cisco router/switch to the edge switch port.
It will output the target IP address, MAC address, edge switch name, port name, port description, interface mode (access or trunk), VLAN(s) allowed on port, and the number of MAC addresses currently learned on the edge port.
By default, the script will output this information to the console.
Please note that this script is only designed to run on Cisco IOS devices.

Usage:
Open a command prompt/terminal and run python cisco_ip_trace.py. The script has two options to run it: interactive prompts or parameters.

Requirements
-Python3.7
-Python modules 'netmiko', 'time',’os’,’getpass’ and 're'
-SSH access to all Cisco devices from the computer running the script; 
-Cisco Discovery Protocol (CDP) enabled on all Cisco switches
-The credentials provided must work on all devices discovered via CDP

