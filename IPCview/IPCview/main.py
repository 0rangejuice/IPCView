
# -*- coding: utf-8 -*-


import sys
from setuptools import setup, find_packages
from hikvision import view

required_python_version = (2, 7, 3)
setup_requires = ['pip>=1.5', 'robotframework==2.8.5', 'requests']

if not sys.version_info >= required_python_version:
    raise Exception('Python version >= %s.%s.%s is required.' % required_python_version)
# 开启设备流
view.open(ip='http://10.1.243.220', user='admin', password='12345+Hik+')

setup(name='auto_cloud',
      version='0.1',
      description='rf interface package',
      author='',
      author_email='',
      url='tbd',
      zip_safe=False,
      packages=find_packages(),
      include_package_data=True,
      setup_requires=setup_requires,)
