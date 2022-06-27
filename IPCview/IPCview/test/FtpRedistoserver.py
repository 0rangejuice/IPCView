#coding=u8

from ftplib import FTP
import time
import datetime
import sys
import os
import json
import requests
import redis



class FTPService:
    def __init__(self, host='10.19.116.26', port=21, username='hik', password='hikvision'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = FTP(self.host)
        self.ftp.login(self.username, self.password)

    def up_load(self, src_file, dst_file):
        with open(src_file, 'rb') as f:
            self.ftp.storbinary('STOR ' + dst_file, f)

    def mkd(self, directory):
        self.ftp.mkd(directory)

    def cwd(self, directory):
        self.ftp.cwd(directory)


def regular_build(component):
    cmpt_id = {'vod': '4573',
               'mgc': '839',
               'dac': '7187',
               'dacdriver': '7095',
               'iac': '2725',
               'iacdriver': '7083',
               'vnsc': '7145',
               'videoplay': '2268',
               'tvms': '1365',
               'cloud': '51204',
               'cloud_dev': '34541'}
    service = 'http://10.19.115.25:8000/'
    url = 'get_jenkins_info'
    jenkins_url = 'http://jk.hikvision.com.cn/query/BuildHistoryGridCmd.ashx?projectId=' + \
                  cmpt_id[component] + '&favorite=0&_page=1&rowNum=10'
    body = {"jenkins_url": jenkins_url}
    response = requests.post(service + url, data=json.dumps(body))
    record = json.loads(json.loads(response.text))['_rows'][0]
    print record
    print record['buildStatus']
    # if record['buildType'] == u'次级构建' and record['buildStatus'] == 'running':
    if record['buildStatus'] == 'running':
        return True


def update_product_logs(report_file, log_path):
    try:
        with open(report_file, 'r') as file:
            org_info = file.read()
            file.close()
        after_info = org_info.replace("'<div id=\"report-or-log-link\"><a href=\"#\"></a></div>' +",
                                      "'<div><a href=\"" + log_path + "\" style=\"display: block; background: black; color: white; text-decoration: none; "
                                      "font-weight: bold; letter-spacing: 0.1em; padding: 0.3em 0; border-bottom-left-radius: 4px;\">"
                                      "Product Logs</a></div>' + '<div id=\"report-or-log-link\"><a href=\"#\"></a></div>' +")
        with open(report_file, 'w') as file:
            file.write(after_info)
            file.close()
    except:
        pass


def redis_connect():
    pool = redis.ConnectionPool(decode_response=True)
    db = redis.Redis(connection_pool=pool, host='10.19.201.89', port=6379, password='12345++')
    db.set("name", "hik.pmp")  # 添加string类型的key-value# #
    print(db.get("name"))  # 速去string类型的key
    db.lpush("names", "ezviz", "hikvision", "IPC")
    db.lrange("name", 0, -1)
    return db

if __name__ == '__main__':
    """
    传入项目名如：viop,hmap(和后端是对应的)
    local_log_folder 根据实际情况修改
    """
    component = sys.argv[1]
    local_log_folder = './case_pool'
    if regular_build(component):
        exit(0)
    db = redis_connect()
    now = datetime.datetime.now()
    if now.hour > 22:
        begin_time = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond) + datetime.timedelta(hours=22)
        # 晚上10点之后的定时构建算第二天CI
    else:
        begin_time = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond) - datetime.timedelta(hours=2)
    end_time = begin_time + datetime.timedelta(hours=24)
    sql = "select report_url from app_t_tasks where task_name = '%s' and start_time >= '%s':: timestamp and " \
          "start_time < '%s':: timestamp" % (component, begin_time.strftime('%Y_%m_%d %H:%M:%S'),
                                             end_time.strftime('%Y_%m_%d %H:%M:%S'))
    print sql
    result = db.query(sql)
    print result
    if len(result):
        url_index = result[-1][0]
        directory = '/reports/%s/%s' % (component, str(int(time.time())))
        ftp = FTPService()
        ftp.mkd(directory)
        ftp.cwd(directory)
        now_string = now.strftime('%Y%m%d_%H%M%S')
        dst_file = 'log_%s_%s.html' % (component, now_string.split('_')[1])
        local_log_path = '{}/log.html'.format(local_log_folder)
        if os.path.exists(local_log_path):
            # update_product_logs(local_log_path, 'http://10.19.115.25:8888%s' % (directory))
            ftp.up_load(local_log_path, dst_file)
        else:
            print("[ftplogtoserver] No valid logs.")
            exit(0)
        log_url = 'http://10.19.201.89:8200/%s/%s' % (directory, dst_file)
        sql = "update app_all_urls set log_url='%s' where id='%s'" % (log_url, url_index)
        db.execute(sql)
        db.close()
    else:
        pass


