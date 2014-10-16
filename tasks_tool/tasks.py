# A personal task management tool, data being stored in a sqlite database.

# load_tasks -- db_file_path, set of labels, filtering conditions.
# add_task -- db_file_path, task_id, title, body, priority, date_opened,
# deadline,
# update_task -- db_file_path, task_object.

# SQL statements must always be enclosed in double qoutes, or by triple "s for
# a multiline statement.
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
# from column names to values. Naively loads all the tasks into memory - this
# is a personal script for fuck's sake.
def load_tasks(db_file_path, labels=None, filters=dict()):
    with sqlite3.connect(db_file_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks;')
        tasks = [_map(task, None) for task in cursor.fetchall()]
        tasks = filter(lambda t: _good(t, filters), tasks)
        tasks = [_map(task, labels) for task in tasks]

    return tasks


# Add a new task.
def add_task(db_file_path, title,
             body, priority, date_opened,
             deadline, status='active'):
    with sqlite3.connect(db_file_path) as conn:
        sql = """INSERT INTO tasks (title, body, priority, date_opened, deadline, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"""\
              % (title, body, priority, date_opened, deadline, status)
        conn.execute(sql)
        conn.commit()


# Deletes a task from the database.
def delete_task(db_file_path, task_id):
    with sqlite3.connect(db_file_path) as conn:
        sql = "DELETE FROM tasks WHERE task_id = '%d'" % (task_id,)
        conn.execute(sql)
        conn.commit()


# Update an existing task. changes is a map of column labels to new values.
def update_task(db_file_path, task_id, changes):
    if not changes:
        # db call is unnecessary.
        return

    with sqlite3.connect(db_file_path) as conn:
        sql, args = "UPDATE tasks SET ", []
        for lbl, new_val in changes.items():
            sql += lbl + " = " + "'%s'"
            args.append(new_val)
        sql = sql + " WHERE task_id = '%d'" % (task_id,)
        sql = sql % tuple(args)
        conn.execute(sql)
        conn.commit()
