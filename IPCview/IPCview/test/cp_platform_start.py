#coding=gbk
__mtime__ = '2021/9/20'
from auto_hik import IPCData, ADMIN_TOKEN
import time
import os, sys, shutil
import xmltodict

vars = {'endpoint_url': sys.argv[1], 'endpoint_url2': sys.argv[2], 'admin_pwd': sys.argv[3]}
if len(sys.argv) >= 6:
    vars.update(dict(x.split('=') for x in sys.argv[5:]))
vars['first_run'] = 'True'
if vars.get('branch1_test', 'false') == 'True':
    vars['main_test'] = 'False'

case_pool_path = 'case_pool'


def generate_output(source_file, dest_file):
    target_dict = {
      "testsuite": {
        "@errors": "0",
        "@failures": "0",
        "@name": "auto_test",
        "@rate": "0.00%",
        "@skips": "0",
        "@tests": "0",
        "@time": "0"
      }
    }
    with open(source_file) as f:
        content = f.read()
        ret = xmltodict.parse(content)
        fail = int(ret['robot']['statistics']['total']['stat'][-1]['@fail'])
        success = int(ret['robot']['statistics']['total']['stat'][-1]['@pass'])
        target_dict['testsuite']['@failures'] = str(fail)
        target_dict['testsuite']['@tests'] = str(success+fail)
        target_dict['testsuite']['@rate'] = '{:.2f}%'.format((float(success)/(success+fail))*100)

        with open(dest_file, 'w') as f:
            f.write(xmltodict.unparse(target_dict))


api = IPCData(ip='http://10.1.243.220', user='admin', password='12345+Hik+')

job_name = 'auto_cloud_dev'

api.build_job(job_name, parameters={'global_vars.py':''}, token=ADMIN_TOKEN)
def wait_job_run(job_name):
    while 1:
        ret = api.get_running_builds()
        for item in ret:
            if item['name'] == job_name:
                number = item['number']
                return number
        time.sleep(5)

number = wait_job_run(job_name)
while 1:
    ret = api.get_build_info(job_name, number)
    print(ret)
    if not ret['building']:
        break
    time.sleep(5)


jenkins_result_path = r'D:\JK\workspace\{}'.format(job_name)

report_path = os.path.join(os.getcwd(), 'report')
if not os.path.exists(report_path):
    os.mkdir(report_path)

for file_name in [ 'log.html', 'output.xml', 'report.html']:
    # srcfile = os.path.join(jenkins_result_path, case_pool_path, file_name)
    srcfile = os.path.join(jenkins_result_path, file_name)
    if file_name == 'output.xml':
        dstfile = os.path.join(report_path, 'python_test_report.xml')
        generate_output(srcfile, dstfile)
        continue
    else:
        dstfile = os.path.join(report_path, file_name)
        
    if file_name == 'log.html':
        shutil.copyfile(srcfile,dstfile)
        dstfile = os.path.join(report_path, 'index.html')
        shutil.copyfile(srcfile,dstfile)
    else:
        shutil.copyfile(srcfile,dstfile)
