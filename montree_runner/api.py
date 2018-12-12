import requests

# STATES
STATE_TODO = "to_do"
STATE_COMPLETED = "completed"
STATE_WORK_IN_PROGRESS = "work_in_progress"
STATE_ARCHIVED = "archived"

def get_checks(conf):
    root_url = conf['root_url']
    cookie = conf['cookie']
    project_id = conf['project_id']

    url = '{root}/api/projects/{project_id}/steps/'.format(
        root=root_url.rstrip('/'),
        project_id=project_id,
    )

    query = requests.get(url, headers={
        'Accept': 'application/json',
        'Cookie': cookie,
    })

    if str(query.status_code)[0] != '2':
        raise Exception('Error "{}" querying "{}"'.format(query.status_code, url))

    csrf_token = query.headers['x-csrf-token']
    data = query.json()

    return {
        "data": data,
        "csrf_token": csrf_token,
    }


def set_step_in_progress(conf, step, csrf_token):
    set_step_state(conf, step, csrf_token, STATE_WORK_IN_PROGRESS)

def set_step_completed(conf, step, csrf_token):
    set_step_state(conf, step, csrf_token, STATE_COMPLETED)

def set_step_to_do(conf, step, csrf_token):
    set_step_state(conf, step, csrf_token, STATE_TODO)

def set_step_archived(conf, step, csrf_token):
    set_step_state(conf, step, csrf_token, STATE_ARCHIVED)

def set_step_state(conf, step, csrf_token, state):
    root_url = conf['root_url']
    cookie = conf['cookie']
    project_id = conf['project_id']

    url = '{root}/api/projects/{project_id}/steps/{step}'.format(
        root=root_url.rstrip('/'),
        project_id=project_id,
        step=step['id'],
    )

    query = requests.patch(url,
                          json={
                              "state": {
                                  "state": state,
                              }
                          },
                          headers={
                              'Cookie': cookie,
                              'Content-Type': 'application/json',
                              'X-CSRF-TOKEN': csrf_token,
                          })

    if str(query.status_code)[0] != '2':
        raise Exception('Error "{}" querying "{}"'.format(query.status_code, url))

    print(step['id'], state, query.json())
