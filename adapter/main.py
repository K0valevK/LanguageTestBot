from adapter import Adapter
import configparser
import json
import requests
import os


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'configs', 'settings.ini'))
    url = config['Paronym']['url']

    resp = requests.get(url)
    d = [json.loads(jline) for jline in resp.text.splitlines()]
    tasks, answers = Adapter.transform_all(d, 'paronym')

    script_dir = os.path.dirname(__file__)
    rel_path = '../database/migrations/task_db/data/tasks.csv'
    with open(os.path.join(script_dir, rel_path), 'w') as tasks_file:
        tasks_file.write('id$type$text$difficulty')

        for task in tasks:
            tasks_file.write('\n')
            tasks_file.write('$'.join(list(map(str, task))).replace('[', '(').replace(']', ')'))

    script_dir = os.path.dirname(__file__)
    rel_path = '../database/migrations/task_db/data/answers.csv'
    with open(os.path.join(script_dir, rel_path), 'w') as ans_file:
        ans_file.write('id$task_id$text$text_pos$is_true')

        for ans in answers:
            ans_file.write('\n')
            ans_file.write('$'.join(list(map(str, ans))).replace('[', '(').replace(']', ')'))
