import requests
import shlex
import socket

PREFIX = 'check:'

def get_check(step):
    if step.get('description', None) is None:
        return None

    checks = [
        line.strip()
        for line in step['description'].split('\n')
        if line.lower().strip().startswith(PREFIX)
    ]
    if len(checks) == 0:
        return None
    return checks[0]

def has_check(step):
    return get_check(step) is not None

def is_step_ok(step):
    check = get_check(step)
    assert check is not None

    return run_check(check)


def run_check(check):
    assert check.strip().lower().startswith(PREFIX)

    command = check.strip()[len(PREFIX):]
    print(command)
    chunks = command.strip().split(" ", 1)
    program = chunks[0]
    if len(chunks) > 1:
        arguments = chunks[1]
    else:
        arguments = ''

    return PROGRAMS[program](**to_dict(shlex.split(arguments)))


def to_dict(args):
    return {
        args[i].strip(':') : args[i + 1]
        for i in range(0, len(args), 2)
    }

## Programs
def _test_http_response(endpoint):
    query = requests.get(endpoint)
    return str(query.status_code)[0] == '2'

def _test_host_availability(host, **kwargs):
    tcp_port = kwargs['tcp-port']
    try:
        s = socket.socket()
        s.connect((host, int(tcp_port)))
        s.close()
        return True
    except:
        return False

def _all_dependencies_ok():
    # TODO
    return True

## Map
PROGRAMS = {
    'test-http-response': _test_http_response,
    'test-host-availability': _test_host_availability,
    'all-dependencies-ok': _all_dependencies_ok,
}
