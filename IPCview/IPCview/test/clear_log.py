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
                            description="删除当前目录下所有xml文件\n".decode('u8').encode('gbk'))
    args = parser.parse_args()
    ret = os.listdir(os.getcwd())
    for name in ret:
        # if re.search('o\d+.xml', name):
        if name.endswith('.xml'):
            print name
            os.remove(name)


if __name__ == '__main__':
    handle()
