#coding=u8
import time
import datetime
import sys
import os
import json
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import xmltodict

def handle():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description="检查rf运行结果是否成功\n"
                                        "如果成功 返回0\n"
                                        "如果失败用例比例大于预期，返回254\n".decode('u8').encode('gbk'))
    parser.add_argument('-f', '--files', help='rf执行结果文件集合'.decode('u8').encode('gbk'), type=str, required=True)
    parser.add_argument('-c', '--count', help='失败用例个数，大于等于则返回254'.decode('u8').encode('gbk'), type=int, default=1)
    args = parser.parse_args()
    fail_count = 0
    for name in args.files.split('  '):
        with open(name) as f:
            ret = xmltodict.parse(f.read())
            fail_count += int(ret['robot']['statistics']['total']['stat'][-1]['@fail'])
    if fail_count >= args.count:
        print(254)
    else:
        print(0)


if __name__ == '__main__':
    handle()
