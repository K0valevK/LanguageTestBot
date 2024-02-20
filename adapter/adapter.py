class Adapter:
    @staticmethod
    def transform(json_data_line, task_type, task_idx=0, ans_idx=0):
        task = []
        ans = []

        if 'complex_words' not in json_data_line:
            return [], []
        tasks = json_data_line['complex_words']
        for i in range(len(tasks)):
            task.append([task_idx, task_type, json_data_line['sentence'], tasks[i]['difficulty']])

            ans.append([ans_idx, task_idx, tasks[i]['word'], tasks[i]['index'], 'True'])
            ans_idx += 1

            for j in range(len(tasks[i]['distortions'])):
                ans.append([ans_idx, task_idx, tasks[i]['distortions'][j], tasks[i]['index'], 'False'])
                ans_idx += 1

            task_idx += 1

        return task, ans

    @staticmethod
    def transform_all(data: list, task_type):
        tasks = []
        answers = []
        for jsonl in data:
            new_task, new_ans = Adapter.transform(jsonl, task_type, len(tasks), len(answers))

            tasks += new_task
            answers += new_ans

        return tasks, answers
