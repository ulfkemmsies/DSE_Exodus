from tkinter import ttk
from tkinter import *

root = Tk()
columns = ("Parameter", "Value", "Unit")
Treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 

root.geometry("900x250")

columnwidth = Treeview.winfo_width()
print(columnwidth)

Treeview.column("Parameter", anchor='center')
Treeview.column("Value", anchor='center')
Treeview.column("Unit", anchor='center')


Treeview.heading("Parameter", text="Parameter")
Treeview.heading("Value", text="Value")
Treeview.heading("Unit", text="Unit")


Treeview.pack(side=LEFT, fill=BOTH)

names = []
vals = []
units = []
for i in range(min(len(names), len(vals))):
    Treeview.insert('', i, values=(names[i], vals[i],units[i]))


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def set_cell_value(event):
    for item in Treeview.selection():
        item_text = Treeview.item(item, "values")
        column = Treeview.identify_column(event.x)
        print(column)
        row = Treeview.identify_row(event.y)
        print(row)
    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))
    entryedit = Text(root, width=25, height=1)
    entryedit.place(x= 10 + (cn - 1) * 300, y=6 + rn * 20)

    def saveedit():
        Treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    okb.place(x=265 + (cn - 1) * 300, y=2 + rn * 20)


def newrow():
    names.append('to be named')
    vals.append('value')
    units.append('unit')
    Treeview.insert('', len(names) - 1, values=(names[len(names) - 1], vals[len(names) - 1], units[len(names)-1]))
    Treeview.update()
    newb.place(x=420, y=(len(names) - 1) * 20 + 45)
    newb.update()


Treeview.bind('<Double-1>', set_cell_value)
newb = ttk.Button(root, text='New Parameter', width=20, command=newrow)
newb.place(x=420, y=(len(names) - 1) * 20 + 45)

for col in columns:
    Treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(Treeview, _col, False))


# def print_width():
#    print("The width of Tkinter rootdow:", root.winfo_width())
#    print("The height of Tkinter window:", root.winfo_height())
# # Create a Label
# Label(root, text="Click the below Button to Print the Height and width of the Screen", font=('Helvetica 10 bold')).pack(pady=20)
# # Create a Button for print function
# Button(root, text="Click", command=print_width).pack(pady=10)

root.mainloop()