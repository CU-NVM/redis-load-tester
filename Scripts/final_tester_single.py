#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a script to Get and Set key in Redis Server for load testing.
This script will use locust as framework.

Author:- OpsTree Solutions
"""

import json
import time
from locust import Locust, events, constant
from locust.core import TaskSet, task
import redis
import gevent.monkey
gevent.monkey.patch_all()
import random


def load_config(filepath):
    """For loading the connection details of Redis"""
    with open(filepath) as property_file:
        configs = json.load(property_file)
    return configs


filename = "redis_single.json"

configs = load_config(filename)


class RedisClient(object):
    def __init__(self, host=configs["redis_host"], port=configs["redis_port"]):
        self.rc = redis.StrictRedis(host=host, port=port)

    def query(self, key, command='GET'):
        """Function to Test GET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result = self.rc.get(key)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, exception=e, response_length=0)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(result)
            events.request_success.fire(request_type=command, name=key, response_time=total_time,
                                        response_length=length)
        return result

    def write(self, key, value, command='SET'):
        """Function to Test SET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result = self.rc.set(key, value)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, exception=e, response_length=0)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = 1
            events.request_success.fire(request_type=command, name=key, response_time=total_time,
                                        response_length=length)
        return result


class RedisLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()
        self.keys =[]


class RedisLua(RedisLocust):
    wait_time = constant(0)

    class task_set(TaskSet):
        @task(1)
        def get_time(self):
            while True:
                getKey = random.choice(self.keys)
                self.client.query(getKey)

        @task(1)
        def write(self):
            while True:
                setKey = random.randrange(1, 2**20)
                self.keys.append(setKey)
                self.client.write(setKey, setKey)
