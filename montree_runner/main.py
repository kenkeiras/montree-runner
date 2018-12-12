#!/usr/bin/env python3

from . import config
from . import api
from . import tester
import time

def first_run(conf):
    checks = api.get_checks(conf)
    graph = checks['data']['steps']
    csrf_token = checks['csrf_token']

    for step in graph:
        api.set_step_in_progress(conf, step, csrf_token)

def check(conf):
    checks = api.get_checks(conf)
    graph = checks['data']['steps']
    csrf_token = checks['csrf_token']

    for step in graph:
        if not tester.has_check(step):
            api.set_step_to_do(conf, step, csrf_token)
        elif tester.is_step_ok(step):
            api.set_step_completed(conf, step, csrf_token)
        else:
            api.set_step_archived(conf, step, csrf_token)

def run(conf):
    # first_run(conf)
    while True:
        print("-" * 10 + " 8< " + "-" * 10)
        check(conf)
        time.sleep(conf.get('sleep_time', 30))

def main():
    if not config.has_configuration():
        config.run_first_time_configuration()

    conf = config.get_configuration()
    run(conf)

if __name__ == '__main__':
    main()
