import os
import netifaces
import socket
import subprocess

from os import listdir
from os.path import isfile, join
from time import sleep


class Helper:

    def __init__(self):
        pass

    def infos(self):
        infos = []
        infos.append('hostname ' + str(socket.gethostname()))
        infos.append('PID ' + str(os.getpid()))
        ifaces = self.interfaces_self()
        for iface in ifaces:
            infos.append('Interface' + str(iface))
        return infos

    def interfaces_first(self):
        ips = self.interfaces_self()
        # remove ipv6 from results
        for ip in ips:
            if ':' not in ip:
                return ip
        return '127.0.0.1'

    def interfaces_self(self):
        ifaces = []
        for interface in netifaces.interfaces():
            if interface != 'lo':
                if 2 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[2][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
                if 17 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[17][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
                if 18 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[18][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
        return ifaces

    def files_in_path(self, file_path):
        files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
        return files

    def not_local(self, ip):
        if ip != '127.0.0.1':
            return True
        return False

    def shutdown(self, time):
        _down = int(time)
        print('fpvcar down in ' + str(_down))
        sleep(_down)
        print('os shudown in 10')
        subprocess.call(['sleep 10s; shutdown -h now'], shell=True)
        return
