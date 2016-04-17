import argparse
import paramiko
import os
import sys
import re
import logging
import socket


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
    parser.add_argument("-loglevel", dest='loglevel', action = "store",
                        default = 'DEBUG',
                        choices={'DEBUG', 'INFO', 'WARN', 'ERROR'},
                        help = "Set logging level")
    parser.add_argument("-logpath", dest='logpath', action = "store",
        default = '/tmp/tears.log', help = "Define logging file path")
    args = parser.parse_args()
    return args

def splitter(args, log):
    string = args.rpath
    strUsrHst = string.split("@")
    usrPrt = strUsrHst[0]

    user = strUsrHst[0]

    a = re.search(',',usrPrt)
    if a is not None:
        elts = usrPrt.split(',')
        if elts[0] == '22' or elts[0] == '2222':
            port = elts[0]
            user = elts[1]
        if elts[1] == '22' or elts[1] == '2222':
            port = elts[1]
            user = elts[0]

    a = re.search(':',usrPrt)
    if a is not None:
        elts = usrPrt.split(':')
        if elts[0] == '22' or elts[0] == '2222':
            port = elts[0]
            user = elts[1]
        if elts[1] == '22' or elts[1] == '2222':
            port = elts[1]
            user = elts[0]

    hstPth = strUsrHst[1].split(':')

    source_ip = socket.gethostbyname(socket.gethostname())

    host = hstPth[0]
    log.info("%s to %s" % (source_ip, host))
    if len(hstPth)==2:
        path_ = hstPth[1]
    else: path_ = "/home/"+user+"/"
    ids = [host, user, path_]
    return ids


def ssh_open(args, ids):
    while True:
        print "Try to connect to %s" % ids[0]
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if args.pas is None:
                client.connect(hostname=ids[0], username=ids[1])
            else:
                client.connect(hostname=ids[0], username=ids[1], password=args.pas)
            print "Connected to %s" % ids[0]
            break
        except paramiko.AuthenticationException:
            log.error("Authentication failed when "
                      "connecting to %s" % ids[0])
            raise
    return client

def ssh_close(client):
    client.close()
    
def file_copy(args, ids):
    if "/" in args.rpath:
        code = os.system("rsync --rsync-path=/usr/bin/rsync"
                         " --checksum %s -%s %s"
                         % (args.lpath, args.rsync, args.rpath))
    else:
        merge_path = args.rpath + ":" + args.lpath
        print merge_path 
        code = os.system("rsync --rsync-path=/usr/bin/rsync"
                         " --checksum %s -%s %s"
                         % (args.lpath, args.rsync, merge_path))
    if code > 0:
        log.error("rsync fails with error code %s" % code)
        sys.exit(1)


def main():
    args = verify_arguments(sys.argv)

    logging.basicConfig(
        filename=args.logpath,
        level=getattr(logging, args.loglevel),
        format='%(levelname)s:%(asctime)s:%(message)s')

    print 
    log = logging.getLogger(__name__)
    log.debug("Hello Vika!")


    ids = splitter(args, log)
    print ids

    ssh = ssh_open(args, ids)
    file_copy(args, ids)
    ssh_close(ssh)

    
if __name__ == "__main__":
    main()
