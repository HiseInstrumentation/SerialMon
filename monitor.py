# Serial Monitor (monitor.py): Utility for monitoring the output from a serial port
#     Copyright (C) 2020 Hise Scientific Instrumentation, LLC. 
# 
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 1, or (at your option)
#     any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA  02110-1301 USA
# 
from serial.tools import list_ports
import serial
import re
import os
import time

selected_port = None
user_port = None
system_ports = []

# Load the existing serial ports into global list
def initialize():
	for n, (port, desc, hwid) in enumerate(sorted(list_ports.comports()), 1):
		system_ports.append(port)

# User interface for selecting port
def selectPort():
	i = 1
	print("Available Serial Ports are: ")
	print("==================================")
	for port in system_ports:
		print(str(i) + ": " + str(port))
		i += 1

	print("**********************************")
	selected_port = input("Select port to use: ")

	return int(selected_port) - 1

# Clear the terminal
def clearTerminal():
	os.system('cls' if os.name == 'nt' else 'clear')

# Show menu
def showMenu():
	clearTerminal()
	print("|= MAIN MENU =========================|")
	print("| 1. Stream to terminal               |")
	print("| 2. Stream to file                   |")
	print("| 0. Exit Program                     |")
	print("|=====================================|")
	command = input("Selection: ")
	return(command)

# Enter buad rate
def selectBaudRate():
	baud_rate = input("Enter baud rate (Defaut: 9600):")
	if(baud_rate == ""):
		baud_rate = 9600
	return baud_rate

# Main
initialize()
user_selected_port = selectPort()
user_baud_rate = selectBaudRate()
port_selection = str(system_ports[user_selected_port])
s = serial.Serial(port_selection, baudrate = user_baud_rate, timeout = 1)
time.sleep(1)

program_running = True

while program_running:
	com = showMenu()
	print(com)

	if com == "0":
		print("Exiting Utility Mode")
		program_running = False

	if com == "1":
		reading_output = True

		while reading_output:
			line = s.readline()
			print(line.decode("utf-8").replace("\n", ""))

	if com == "2":
		filename = input("Enter filename (serial_out.txt): ")
		if(filename == ""):
			filename = "serial_out.txt"

		reading_output = True

		while reading_output:
			line = s.readline()
			f = open(filename, "a")
			print(line.decode("utf-8").replace(r'\r', ''))
			f.write(line.decode("utf-8").replace(r'\r', ''))
			f.close()


s.close()
