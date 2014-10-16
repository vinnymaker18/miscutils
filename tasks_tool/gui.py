# A gui for tasks tool.

import Tkinter
import tasks


class TaskWidget(Tkinter.Frame):
    def __init__(self, root=None, db_file_path='/home/evinay/.tasks.db'):
        Tkinter.Frame.__init__(self, root)
        self.grid()
        self.db_file_path = db_file_path
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        self.all_tasks = tasks.load_tasks(self.db_file_path)
        self.tableheight = 1 + len(self.all_tasks)
        label_widths = {'task_id': 4, 'title': 20, 'body': 30,
                        'priority': 5,
                        'date_opened': 10, 'deadline': 10, 'status': 10}
        column_labels = ['task_id', 'title', 'body', 'priority',
                         'date_opened', 'deadline', 'status']
        self.tablewidth = len(column_labels)

        # Index of the cell in entries array given it's grid position.
        def _idx(r, c):
            return r * self.tablewidth + c

        # The top row containing the labels.
        for col, lbl in enumerate(column_labels):
            wid = label_widths[lbl]
            self.entries[_idx(0, col)] = Tkinter.Entry(self, width=wid)
            self.entries[_idx(0, col)].insert(0, lbl)
            self.entries[_idx(0, col)].grid(row=1, column=col)

        # Populate all the task rows.
        for (row, t) in enumerate(self.all_tasks):
            for col, lbl in enumerate(column_labels):
                wid = label_widths[lbl]
                idx = _idx(row + 1, col)
                cur_entry = self.entries[idx] = Tkinter.Entry(self, width=wid)
                cur_entry.insert(1, t[lbl])
                cur_entry.grid(row=row + 2, column=col)


def main():
    task_w = TaskWidget(None, 'tasks.db')
    task_w.master.title('Tasks tool')
    task_w.mainloop()


if __name__ == '__main__':
    main()
