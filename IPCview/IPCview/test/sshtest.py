# -*- coding: utf-8 -*-
"""
__mktime__ = '2022/06/29'
__author__ = 'zwh'
__filename__ =
"""

import paramiko


def sshclient_execmd(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command(execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.

    print
    stdout.read()
    s.close()


def main():
    hostname = '10.33.137.210'
    port = 55555
    username = 'root'
    password = '1234566@A'
    execmd = "ls"

    sshclient_execmd(hostname, port, username, password, execmd)


if __name__ == "__main__":
    main()


# 产品质量部测试
'''
密码统一：1234566@A
ssh root@10.33.139.35 -p 55555
ssh root@10.33.140.46 -p 55555
ssh root@10.33.137.210 -p 55555
'''
