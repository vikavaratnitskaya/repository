# -*- coding: utf-8 -*-
import argparse
import paramiko
import os
import sys
import re
import hashlib

def verify_arguments(argv):
    usage = "syncer.py -pas ssh_password lpath local_path \
        - rcync_arguments --file single_file_name remote_path"
    epilog = "Remote path should be specified as root@hostname:/folder"
    parser = argparse.ArgumentParser(description = "Remote copy utility",
        usage = usage, epilog = epilog)
    parser.add_argument("lpath", action = "store",
        default = None, help = "Local path")
    parser.add_argument("-pas", action = "store",
        default = None, help = "SSH password")
    parser.add_argument("-", dest = "rsync", action = "store",
        default = None, help = "rsync options")
    parser.add_argument("-file", action = "store",
        default = None, help = "single file to copy")
    parser.add_argument("rpath", action = "store",
        default = None, help = "Remote path")
    args = parser.parse_args()
    return args

# The isolation of elements to transfer (host,port,user,path) without "password"
def splitter(args):
    string = args.rpath
    port = None
    strUsrHst = string.split("@")
    usrPrt = strUsrHst[0]
    user = strUsrHst[0]
    a = re.search(',', usrPrt)
    if a is not None:
        elts = usrPrt.split(',')
        if elts[0].isalpha():
            user = elts[0]
            port = elts[1]
        else:
            user = elts[1]
            port = elts[0]
        intPort = int(port)
        if 1 > intPort or intPort > 65535:
            print "Invalid number of port! The port will be set by default."
            port = '22'
    a = re.search(':', usrPrt)
    if a is not None:
        elts = usrPrt.split(':')
        if elts[0].isalpha():
            user = elts[0]
            port = elts[1]
        else:
            user = elts[1]
            port = elts[0]
        intPort = int(port)
        if 1 > intPort or intPort > 65535:
            print "Invalid number of port! The port will be set by default."
            port = '22'
    hstPth = strUsrHst[1].split(':')
    host = hstPth[0]
    if len(hstPth)==2:
        path_ = hstPth[1]
    else: path_ = "/home/"+user+"/"
    ids = [host, user, path_, port]
    return ids

# Function to compare the hash of local and remote lists of files and directories (return list "schedule" to copy)
# It takes lists after command like "os.system ('ls')" from local and remote machine
def md5_checker(lstLcl,lstRmt):
    schedule = []
    schedule.extend(lstLcl)
    x = 0
    while x < len(lstLcl):
        hshLcl = hashlib.md5(lstLcl[x]).hexdigest()
        y = 0
        while y < len(lstRmt):
            hshRmt = hashlib.md5(lstRmt[y]).hexdigest()
            if hshLcl == hshRmt:
                schedule.remove(lstRmt[y])
            y=y+1
        x=x+1
    return schedule

# Function to compare the hash of local and remote lists of files and directories
# Returns a list of the files are not copied)
def sccss_checker(schedule,lstRmt):
    compareList = md5_checker(schedule, lstRmt)
    if len(compareList) != 0:
        print "Attention! Files: ",compareList," not copied!"
    return compareList

def ssh_open(args, ids):
    while True:
        print "Try to connect to %s" % ids[0]
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if args.pas == None:
                client.connect(hostname=ids[0], username=ids[1])
            else:
                client.connect(hostname=ids[0], username=ids[1], password=args.pas)
            print "Connected to %s" % ids[0]
            break
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % ids[0]
            sys.exit(1)
    return client

def ssh_close(client):
    client.close()
    
def file_copy(args, ids):
    if "/" in args.rpath:
        os.system("rsync --rsync-path=/usr/bin/rsync --checksum %s -%s %s"
                   % (args.lpath, args.rsync, args.rpath))
    else:
        merge_path = args.rpath + ":" + args.lpath
        print merge_path 
        os.system("rsync --rsync-path=/usr/bin/rsync --checksum %s -%s %s"
                   % (args.lpath, args.rsync, merge_path))


def main():
    args = verify_arguments(sys.argv)
    ids = splitter(args)
    ssh = ssh_open(args, ids)
#   md5_checker()
    file_copy(args, ids)
#   sccss_checker()
    ssh_close(ssh)

if __name__ == "__main__":
    main()
