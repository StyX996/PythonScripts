#!/usr/bin/env python
from argparse import ArgumentParser
import sys, os, glob, ipaddress, re

parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="directory", help="Select log DIR")
parser.add_argument("-c", "--cidr", dest="cidr", help="CIDR to be searched for")
parser.add_argument("-cf", "--cidr_file", dest="cidr_file", help="Specify a file which contains CIDR's")
parser.add_argument("-sf", "--show_filenames", dest="show_filenames", action="store_true", help="Display filenames")
args = parser.parse_args()

### CHECK ARGS
if args.directory == None:
    print("You have to specify a log dir")
    exit()
if args.cidr == None and args.cidr_file == None:
    print("You have to specify a cidr or cidr file")
    exit()
if args.cidr != None and args.cidr_file != None:
    print("Only specify cidr or cidr file!")
    exit()



### Magic
os.chdir(args.directory)
m = 0
v = 0
output = []

def print_progress():
    global m, v
    # Prints the actual progress
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*int(v/m*20), int(v/m*100)))
    sys.stdout.flush()


def search(cidr):
    global v, output
    for file in glob.glob("*.py"):
        v += 1
        print_progress()
        for ip in ipaddress.IPv4Network(cidr):
            fop = open(file,"r")
            for line in fop:
                if re.search(str(ip), line):
                    if args.show_filenames:
                        output += file
                        output += ': '
                    output += line 
            fop.close


if len(glob.glob("*.py")) == 0:
    print("Logdir dont contain any logfiles")
    exit()
else:
    log_file_count = len(glob.glob("*.py"))
    print("Loaded %d logiles..." % log_file_count)


if args.cidr != None:
    # Single CIDR
    print("Loaded 1 cidr...")
    m=log_file_count
    search(args.cidr)
else:
    # CIDR File
    with open(args.cidr_file) as f:
        cidr_file_contents = f.read().splitlines()
    cidr_count = len(cidr_file_contents)
    print("Loaded %d cidr's..." % cidr_count)
    m=cidr_count*log_file_count
    for cidr in cidr_file_contents:
        search(cidr)
        
print("\r\n---- OUTPUT ----")
print(''.join(output))


