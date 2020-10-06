import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog, messagebox
import sqlite3 as sq

root =tk.Tk()
apps=[]
# sql definitions
conn = sq.connect('todo.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')
task = []
state = []
taskPlace = 220
# -------------------------------To do List Functions--------------------------------
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
        cb = tk.Checkbutton(root, text=word, variable=state[task.index(word)],font = ('Sans','10','bold'))
        cb.place(x=900, y=taskPlace)
        taskPlace=taskPlace+30
        e1.delete(0, 'end')

def updateList():
    global state

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
    taskPlace = 220

    for i in task:
        cb=tk.Checkbutton(root, text=i, variable=state[task.index(i)],font = ('Sans','10','bold'))
        cb.place(x=900, y=taskPlace)
        taskPlace = taskPlace + 30

# -------------------------------App runner Functions--------------------------------
def addApp():
    filename=filedialog.askopenfilename(initialdir="/", title="Select File",
                                    filetypes=( ("executables","*.exe"),("all files","*")))

    apps.append(filename)

    lb.delete(0, 'end')
    for app in apps:
        app=app.split('/')[-1]
        app = app.split('.')[0]
        lb.insert('end', app)

def RemoveApp():
        try:
            name=lb.get(lb.curselection())
            fullName=""

            for app in apps :
               if name == app.split('/')[-1].split('.')[0] :
                 fullName=app

            apps.remove(fullName)


            lb.delete(0, 'end')
            for app in apps:
                app = app.split('/')[-1]
                app = app.split('.')[0]
                lb.insert('end', app)
        except:
             messagebox.showinfo('Cannot Delete', 'No app  Selected')

def runApps():
    for app in apps:
        os.startfile(app)
def bye():
    updateList()
    root.destroy()
    with open('save.txt','w') as f:
        for app in apps:
            f.write(app + ",")


############################## main program ################################
# add canvas and roots
canvas = tk.Canvas(root, height=500, width=1050)
canvas.pack()

background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

#root =tk.Canvas(root, height=350, width=470, bg='#80c1ff')
#root.place(x=50 ,y=90)

#root =tk.Canvas(root, height=350, width=400, bg='#80c1ff')
#root.place(x=620 ,y=90)

l0=ttk.Label(root, text='good morning world',font = ('Sans','20','bold'),foreground ="green")

####################### to do list object #######################


l1 = ttk.Label(root, text='My smart To-Do List:',font = ('Sans','17','bold'),foreground ="green")
l2 = ttk.Label(root, text='Enter task title: ',foreground ="blue")
l3= ttk.Label(root, text='Tasks: ',foreground ="blue")
e1 = ttk.Entry(root, width=21)
b1 = tk.Button(root, text='Add task', width=17, command=addTask, font = ('Sans','15','bold') ,foreground ="blue")
b3 = tk.Button(root, text='update list', width=17, command=updateList,font = ('Sans','15','bold'),foreground ="blue")
b4 = tk.Button(root, text='Exit', width=17, command=bye,font = ('Sans','15','bold'))
b5= tk.Button(root, text='Delete All', width=17, command=deleteAll,font = ('Sans','15','bold'),foreground ="blue")

retrieveDB()
update_checkbox()

# Place geometry
l0.place(x=360,y=30)
l1.place(x=700, y=110)
l2.place(x=640, y=155)
l3.place(x=900, y=155)
e1.place(x=640, y=190)
b1.place(x=630, y=240)
b3.place(x=630, y=290)
b5.place(x=630, y=340)
b4.place(x=400, y=430)



####################### Apps runner object #######################

#add labels and list box
l4 = tk.Label(root, text="Apps to run:",font = ('Sans','10','bold') ,foreground="blue")
l4.place(x=300,y=160)

l5 = tk.Label(root, text="Apps runner:",font = ('Sans','17','bold') ,foreground="green")
l5.place(x=170,y=110)
# transperaty
lb = tk.Listbox(root, height=11, selectmode='SINGLE',font = ('Sans','10','bold'),bg='#80c1ff')
lb.place(x=270,y=190)

# crate and place the buttons
addApp = tk.Button(root, text="Add app", font = ('Sans','15','bold'), padx=14, pady=4, command=addApp,foreground="blue")
addApp.place(x=60,y=200)

runApps= tk.Button(root,text="Run all apps",font = ('Sans','15','bold'),padx=10,pady=4,command =runApps,foreground="blue")
runApps.place(x=60,y=260)

deleteApp= tk.Button(root,text="Delet App",font = ('Sans','15','bold'),padx=10, pady=4,command=lambda: RemoveApp(),foreground="blue")
deleteApp.place(x=60,y=320)

 # read apps from file to list
if os.path.isfile('save.txt'):
    with open('save.txt','r')as f:
        tempApps=f.read()
        tempApps=tempApps.split(',')
        apps=[x for x in tempApps if x.strip()]

# updete apps from list to list box
lb.delete(0, 'end')
for app in apps:
    app=app.split('/')[-1]
    app=app.split('.')[0]
    lb.insert('end', app)


root.mainloop()

conn.commit()
cur.close()
with open('save.txt','w') as f:
    for app in apps:
        f.write(app + ",")




