import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json

tasks = []
categories = ["Trabalho", "Pessoal", "Estudos"]

def add_task():
    task = entry.get()
    category = category_var.get()
    if task:
        tasks.append((task, category))
        listbox.insert(tk.END, f"{task} [{category}]")
        entry.delete(0, tk.END)
        save_tasks()
        update_status()
    else:
        messagebox.showwarning("Aviso", "Você deve inserir uma tarefa.")

def delete_task():
    try:
        index = listbox.curselection()[0]
        listbox.delete(index)
        tasks.pop(index)
        save_tasks()
        update_status()
    except IndexError:
        messagebox.showwarning("Aviso", "Você deve selecionar uma tarefa.")

def edit_task():
    try:
        index = listbox.curselection()[0]
        old_task, old_category = tasks[index]
        new_task = simpledialog.askstring("Editar Tarefa", "Edite a tarefa:", initialvalue=old_task)
        new_category = simpledialog.askstring("Editar Categoria", "Edite a categoria:", initialvalue=old_category)
        if new_task and new_category:
            tasks[index] = (new_task, new_category)
            listbox.delete(index)
            listbox.insert(index, f"{new_task} [{new_category}]")
            save_tasks()
            update_status()
    except IndexError:
        messagebox.showwarning("Aviso", "Você deve selecionar uma tarefa.")

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            loaded = json.load(file)
            for task, category in loaded:
                tasks.append((task, category))
                listbox.insert(tk.END, f"{task} [{category}]")
    except FileNotFoundError:
        pass

def update_status():
    status_var.set(f"{len(tasks)} tarefas")

def search_tasks():
    term = simpledialog.askstring("Pesquisar Tarefas", "Digite o termo de pesquisa:")
    if term:
        listbox.delete(0, tk.END)
        for task, category in tasks:
            if term.lower() in task.lower() or term.lower() in category.lower():
                listbox.insert(tk.END, f"{task} [{category}]")


def delete_all_tasks():
    if messagebox.askyesno("Confirmação", "Tem certeza de que deseja remover todas as tarefas?"):
        listbox.delete(0, tk.END)
        tasks.clear()
        save_tasks()
        update_status()

# Janela principal
root = tk.Tk()
root.title("📝 Gerenciador de Tarefas")
root.geometry("500x500")
root.resizable(False, False)

# Estilo
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Salvar", command=save_tasks)
file_menu.add_command(label="Carregar", command=load_tasks)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=root.quit)

# Frame superior
top_frame = ttk.Frame(root)
top_frame.pack(pady=10)

entry = ttk.Entry(top_frame, width=40)
entry.pack(side=tk.LEFT, padx=5)

category_var = tk.StringVar(value=categories[0])
category_menu = ttk.OptionMenu(top_frame, category_var, categories[0], *categories)
category_menu.pack(side=tk.LEFT, padx=5)

add_button = ttk.Button(top_frame, text="➕ Adicionar", command=add_task)
add_button.pack(side=tk.LEFT, padx=5)

# Lista de tarefas
listbox = tk.Listbox(root, width=90, height=10, font=("Segoe UI", 10))
listbox.pack(pady=10)

# Frame de botões
button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

ttk.Button(button_frame, text="🗑️ Remover", command=delete_task).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="📝 Editar", command=edit_task).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="🔍 Pesquisar", command=search_tasks).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="🧹 Remover Todas", command=delete_all_tasks).grid(row=1, column=1, padx=5, pady=5)

# Barra de status
status_var = tk.StringVar()
status_var.set("0 tarefas")
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

# Inicialização
load_tasks()
update_status()
root.mainloop()
