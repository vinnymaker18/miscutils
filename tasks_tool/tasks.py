# A personal task management tool, data being stored in a sqlite database.

# load_tasks -- db_file_path, set of labels, filtering conditions.
# add_task -- db_file_path, task_id, title, body, priority, date_opened,
# deadline,
# update_task -- db_file_path, task_object.

import sqlite3


# Check whether a task passes the given filter.
# A filter is a map of column name to a list of permitted values. e.g, if
# one of the entries is pri : ['lo', 'med'], then only lo and medium priority
# tasks pass the filter.
def _good(task, filters):
    for col, value in task.items():
        entry = filters.get(col, None)
        if entry and value not in entry:
            return False

    return True


# Convert a sqlite3.Row object into a k-v map, but only the given subset of
# columns.
def _map(db_row, lbl_set):
    lbl_set = lbl_set or db_row.keys()
    return dict((lbl, db_row[lbl]) for lbl in lbl_set)


# Load the set of tasks matching the given filters. Each task object is a map
# from column names to values.
def load_tasks(db_file_path, labels=None, filters=dict()):
    with sqlite3.connect(db_file_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks;')
        tasks = [_map(task, labels) for task in cursor.fetchall()]
        tasks = filter(lambda t: _good(t, filters), tasks)

    return tasks


# Add a new task.
def add_task(db_file_path, task_id, title,
             body, priority, date_opened,
             deadline, status='active'):
    with sqlite3.connect(db_file_path) as conn:
        sql = """INSERT INTO tasks (task_id, title, body, priority, date_opened, deadline, status) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s')"""\
              % (task_id, title, body, priority, date_opened, deadline, status)
        conn.execute(sql)
        conn.commit()


# Update an existing task.
def update_task(db_file_path, task):
    with sqlite3.connect(db_file_path) as conn:
        task_id = task["task_id"]
        sql = "UPDATE tasks SET status = '%s' WHERE task_id = %d"\
              % (task["status"], task_id)
        conn.execute(sql)
        conn.commit()
