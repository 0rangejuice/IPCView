#coding=u8
import time
import datetime
import sys
import os
import json

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import xmltodict
import re

def handle():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description="删除当前目录下global_variables.txt和cookie.txt\n".decode('u8').encode('gbk'))
    args = parser.parse_args()
    cwd = os.getcwd()
    ret1 = os.listdir(cwd)
    print(ret1)
    for name in ret1:
        if name == 'global_variables.txt':
            os.remove(name)
            print('delete global_variables.txt')
        if name == 'cookie.txt':
            os.remove(name)
            print('cookie.txt')

    cwd2 = cwd + '\case_pool'
    ret2 = os.listdir(cwd2)
    print(ret2)
    for name in ret2:
        if name == 'global_variables.txt':
            os.remove(os.path.join(cwd2, name))
            print('delete global_variables.txt success')
        if name == 'cookie.txt':
            os.remove(os.path.join(cwd2, name))
            print('delete cookie.txt success')


if __name__ == '__main__':
    handle()
