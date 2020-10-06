import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq

root = tk.Tk()
root.title('To-Do List')
root.geometry("400x250+500+300")

conn = sq.connect('todo.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')
#cur.execute('create table if not exists state (title text)')
task =  []
state = []
taskPlace=60

# ------------------------------- Functions--------------------------------
def addTask():
    global taskPlace
    global state
    word = e1.get()
    if len(word) == 0:
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:

        task.append(word)
        state.append(tk.IntVar())
        cur.execute('insert into tasks values (?)', (word,))
        #cur.execute('insert into state values (?)', (tk.IntVar().get(),))
        #listUpdate()
        #t.insert(cb)
        cb = tk.Checkbutton(root, text=word, variable=state[task.index(word)])
        cb.place(x=230, y=taskPlace)
        taskPlace=taskPlace+20
        e1.delete(0, 'end')


#def listUpdate():
 #   clearList()
   # for i in task:
   #     t.insert('end', i)


def updateList():
    global state
    print(state)
    print(task)

    for i in state:
        if i.get():
           cur.execute('delete from tasks where title = ?', (task[state.index(i)],))
           del task[state.index(i)]
           state.remove(i)
    update_checkbox()


def deleteAll():
    mb = messagebox.askyesno('Delete All', 'Are you sure?')
    if mb == True:
        while (len(task) != 0):
            task.pop()
        cur.execute('delete from tasks')
        update_checkbox()


#def clearList():
  #  t.delete(0, 'end')


def bye():
    updateList()
    root.destroy()


def retrieveDB():
    while (len(task) != 0):
        task.pop()
    for row in cur.execute('select title from tasks'):
        task.append(row[0])
        state.append(tk.IntVar())

def update_checkbox():
    global taskPlace
    global state
    for widget in root.winfo_children():
        if type(widget) == tk.Checkbutton:
           widget.destroy()
    taskPlace=60

    for i in task:
        cb=tk.Checkbutton(root, text=i, variable=state[task.index(i)])
        cb.place(x=230, y=taskPlace)
        taskPlace = taskPlace + 20

# ------------------------------- Functions--------------------------------


l1 = ttk.Label(root, text='To-Do List',font = ('Sans','20','bold'))
l2 = ttk.Label(root, text='Enter task title: ')
e1 = ttk.Entry(root, width=21)
#t = tk.Listbox(root, height=11, selectmode='SINGLE')
b1 = ttk.Button(root, text='Add task', width=20, command=addTask)
b3 = ttk.Button(root, text='update list', width=20, command=updateList)
b4 = ttk.Button(root, text='Exit', width=20, command=bye)
b5= ttk.Button(root, text='Delete All', width=20, command=deleteAll)

retrieveDB()
#listUpdate()
update_checkbox()
# Place geometry
l2.place(x=50, y=50)
e1.place(x=50, y=80)
b1.place(x=50, y=110)
b3.place(x=50, y=170)
b4.place(x=50, y=200)
b5.place(x=50, y=230)
l1.place(x=200, y=10)
#t.place(x=220, y=50)
root.mainloop()

conn.commit()
cur.close()