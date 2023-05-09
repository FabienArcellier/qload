#!/usr/bin/env python
#
# To enable this hook, rename this file to hook_started.py.
#
# It's a way to check if the environment is ready for the test.
#  * check if a port is listening before executing the test
#  * check if a database in postgresql is up and mounted
#

import boto3
import fixtup.helper

fixtup.helper.wait_port(9090, timeout=5000)

s3 = boto3.client('s3', endpoint_url='http://localhost:9090')
s3.upload_file('file.json', 'bucket', 'file.json')

