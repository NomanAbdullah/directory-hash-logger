# Author: Abdullah Al Noman
# Date: March 14, 2023
# Description: This python script gets hashes of direcotry files and sends to a remote syslog server.

import os
import hashlib
import socket
from datetime import datetime

# get fully qualified domain name
fqdn = socket.getfqdn()

def get_file_hash(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def write_hashes_to_file(start_path, output_file):
    with open(output_file, 'w') as f:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                file_hash = get_file_hash(full_path)
                f.write(f"{fqdn} hashlogger: path: {full_path} md5_hash: {file_hash}\n")

#Example usage: compute MD5 hashes of all files in the current directory and its subdirectories
write_hashes_to_file('./tmp/', 'file_hashes.txt')

# UDP syslog server address and port
server_address = ('REMOTE_SYSLOG_IP', 514)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open the file for reading
with open('file_hashes.txt', 'r') as file:
    # Read the file line by line
    for line in file:
        # Send the file content to the syslog server
        sock.sendto(line.encode('utf-8'), server_address)

# Close the socket
sock.close()
