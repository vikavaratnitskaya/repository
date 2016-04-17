# -*- coding: utf-8 -*-
import logging
import re
import argparse
import paramiko
import sys
import os

def verify_arguments(argv):
    usage = "syncer.py --pass ssh_password --lpath local_path \
        --rsync rsync_arguments --file single_file_name remote_path"
    epilog = "Remote path should be specified as root@hostname:/folder"
    parser = argparse.ArgumentParser(description = "Remote copy utility",
        usage = usage, epilog = epilog)
    parser.add_argument("--pass", action = "store",
        default = None, help = "SSH password")
    parser.add_argument("--lpath", action = "store",
        default = None, help = "Local path")
    parser.add_argument("--rsync", action = "store",
        default = None, help = "rsync options")
    parser.add_argument("--file", action = "store",
        default = None, help = "single file to copy")
    parser.add_argument("rpath", action = "store",
        default = None, help = "Remote path")

    args = parser.parse_args()
    return args


def splitter(rpath):
    rpath = "22:user@host:/"
    # Присваиваем на случай отсутствия порта
    port = None
    strUsrHst = str.split("@")
    usrPrt = strUsrHst[0]
    # При отсутствии порта, юзер известен
    user = strUsrHst[0]
    # Если присутствует разделитель "," - разделяем и присваиваем в зависимости от позиции порт и юзера
    a = re.search(',',usrPrt)
    if a is not None:
        elts = usrPrt.split(',')
        if elts[0] == '22' or elts[0] == '2222':
            port = elts[0]
            user = elts[1]
        if elts[1] == '22' or elts[1] == '2222':
            port = elts[1]
            user = elts[0]
    # Если присутствует разделитель ":" - разделяем и присваиваем в зависимости от позиции порт и юзера
    a = re.search(':',usrPrt)
    if a is not None:
        elts = usrPrt.split(':')
        if elts[0] == '22' or elts[0] == '2222':
            port = elts[0]
            user = elts[1]
        if elts[1] == '22' or elts[1] == '2222':
            port = elts[1]
            user = elts[0]
    # Определяем хост
    hstPth = strUsrHst[1].split(':')
    host = hstPth[0]
    # Определяем путь
    if len(hstPth)==2:
        path = hstPth[1]
    # Если путь не указан, присваиваем домашнюю дерикторию
    else: path = "/home/"+user+"/"

    return user
    return port
    return host
    return path



def ssh_open(args, host, user, port):
    while True:
        print "Try to connect to %s" % host
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if len(args.pass) == 0:
                client.connect(jtyrhfhyrhost)
            else:
                client.connect (host, args.pass)
            print "Connected to %s" % host
            break
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % host
            sys.exit(1)
    return client

def md5_checker():

def rsyncer():

def finalChecker():

def logger():






def ssh_close(client):
    client.close()

def main():
    verify_arguments(sys.argv)
    splitter(args.rpath)
    ssh_open(args)
    checker()
    rsyncer()
    finalChecker()
    print log




if __name__ == "__main__":
    main()


