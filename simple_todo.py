import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel

from button import Button
from todo import Todo


class MyApp():
    todos = []

    file_path = f"{os.getcwd()}\\tkinter\\simple_todo\\todos.json"

    def __init__(self):
        self.load_todos()

        self.app = tk.Tk()
        self.app.title(f"{os.getlogin()}'s Todos")
        self.app.geometry("500x500+800+400")
        self.app.resizable(width=False, height=False)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.configure(background='#b19f00')

        self.create_gui_elements()
        self.position_gui_elements()

        self.app.mainloop()

    def create_gui_elements(self):
        self.create_user_input_elements()
        self.create_buttons()
        self.create_treeview()

    def position_gui_elements(self):
        self.position_user_input_elements()
        self.position_buttons()
        self.position_treeview()

    def create_user_input_elements(self):
        self.label_todo = tk.Label(self.app, text="Todo:", font=(
            "Arial", 12, 'bold'), pady=10, background='#b19f00', foreground='#fff')
        self.entry_todo = tk.Entry(self.app)

    def position_user_input_elements(self):
        self.label_todo.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_todo.grid(
            row=0, column=1, columnspan=2, padx=10, sticky="ew")

    def create_buttons(self):
        self.clear_btn = Button(
            self.app, command=self.clear, text="Clear", font=("Arial", 11, "bold"),
            padx=5, pady=3, border=0, bg="#006eff", fg="#fff", activebackground="#005fdb", activeforeground="#fff"
        )
        self.submit_btn = Button(
            self.app, command=self.submit, text="Submit", font=("Arial", 11, "bold"),
            padx=5, pady=3, border=0, bg="#11ff00", fg="#fff", activebackground="#2ddb21", activeforeground="#fff"
        )

    def position_buttons(self):
        self.clear_btn.grid(
            row=1, column=0, columnspan=1, padx=10, sticky="ew")
        self.submit_btn.grid(
            row=1, column=1, columnspan=1, padx=10, sticky="ew")

    def create_treeview(self):
        columns = ('author', 'todo', 'created_at')
        self.tree = ttk.Treeview(self.app, columns=columns, show='headings')

        self.tree.heading('author', text='Author')
        self.tree.heading('todo', text='Todo')
        self.tree.heading('created_at', text='Created at')

        self.tree.column('author', width=75)
        self.tree.column('todo', width=150)
        self.tree.column('created_at', width=150)

        self.tree.bind('<<TreeviewSelect>>', self.delete_selected)

        self.update_treeview()

    def delete_selected(self, e):
        selected_items = self.tree.selection()

        for selected_item in selected_items:
            item_info = self.tree.item(selected_item, 'values')
            if item_info:
                author, text, created_at = item_info
                matching_todo = None
                for todo in self.todos:
                    if todo.author == author and todo.text == text and todo.created_at == created_at:
                        matching_todo = todo
                        break
                if matching_todo:
                    if askokcancel(title='Delete Todo', message="Are you sure?"):
                        self.todos.remove(matching_todo)
                        self.tree.delete(selected_item)
                        self.save_file()

    def position_treeview(self):
        self.tree.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    def update_treeview(self):
        self.clear_tree()
        for todo in self.todos:
            self.tree.insert('', tk.END, values=(
                todo.author, todo.text, todo.created_at))

    def clear_tree(self):
        for todo in self.tree.get_children():
            self.tree.delete(todo)

    def submit(self):
        todo = Todo(len(self.todos) + 1, self.entry_todo.get(), os.getlogin())
        self.todos.append(todo)
        self.update_treeview()
        self.entry_todo.delete(0, tk.END)
        self.save_file()

    def clear(self):
        if askokcancel(title="Clear all", message="Do you want delete all todos"):
            self.clear_tree()
            self.todos.clear()

    def save_file(self):
        todos_json = json.dumps(
            self.todos, default=lambda o: o.__dict__, indent=4)
        with open(self.file_path, "w") as f:
            f.write(todos_json)

    def load_todos(self):
        with open(self.file_path, "r") as f:
            todos_json_ff = f.read()
            todos_from_file = json.loads(todos_json_ff)
            for t in todos_from_file:
                todo = Todo(len(self.todos), t['text'], os.getlogin())
                self.todos.append(todo)


MyApp()
