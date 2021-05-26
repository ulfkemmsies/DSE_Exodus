from tkinter import *
from tkinter import ttk
from commondata import CommonData
import tkinter.messagebox

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("H.O.M.E. Design Suite")
        self.master.geometry("1000x400")

        self.datahandler = CommonData()
        
        self.make_top_menu()

        self.create_tabs()
        self.bind_all('<<NotebookTabChanged>>', lambda e: self.focus(e))

    def create_tabs(self, new_tab=None, new_subtab=None, subtabonly=False):

        if new_tab==None and new_subtab==None and subtabonly==False:

            self.tabs = ttk.Notebook(self.master)

            self.datahandler.df_tab_organizer()

            for tab_name in self.datahandler.tab_names:
                globals()[f"{tab_name}_tab"] = ttk.Frame(self.tabs)
                self.tabs.add(globals()[f"{tab_name}_tab"], text=self.name_cleaner(tab_name))

                self.datahandler.df_subtab_creator(tab_name)

                if len(self.datahandler.subtabs) > 0:

                    globals()[f"{tab_name}_subtab_notebook"] = ttk.Notebook(globals()[f"{tab_name}_tab"])

                    for subtab_name in self.datahandler.subtabs:
                        
                        globals()[f"{subtab_name}_subtab"] = ttk.Frame(globals()[f"{tab_name}_subtab_notebook"])
                        globals()[f"{tab_name}_subtab_notebook"].add(globals()[f"{subtab_name}_subtab"], text=self.name_cleaner(subtab_name))
                        globals()[f"{tab_name}_subtab_notebook"].pack(expand=1, fill="both")

        elif new_tab != None and new_subtab != None and subtabonly==False:

            globals()[f"{new_tab}_tab"] = ttk.Frame(self.tabs)
            self.tabs.add(globals()[f"{new_tab}_tab"], text=self.name_cleaner(new_tab))

            globals()[f"{new_tab}_subtab_notebook"] = ttk.Notebook(globals()[f"{new_tab}_tab"])

            globals()[f"{new_subtab}_subtab"] = ttk.Frame(globals()[f"{new_tab}_subtab_notebook"])

            globals()[f"{new_tab}_subtab_notebook"].add(globals()[f"{new_subtab}_subtab"], text=self.name_cleaner(new_subtab))

            # print(globals()[f"{new_subtab}_subtab_notebook"] != None)
            globals()[f"{new_tab}_subtab_notebook"].pack(expand=1, fill="both")
            
            self.datahandler.df_tab_organizer()
            for tab_name in self.datahandler.tab_names:
                self.datahandler.df_subtab_creator(tab_name)
        
        elif new_tab != None and new_subtab != None and subtabonly==True:

            globals()[f"{new_subtab}_subtab"] = ttk.Frame(globals()[f"{new_tab}_subtab_notebook"])
            globals()[f"{new_tab}_subtab_notebook"].add(globals()[f"{new_subtab}_subtab"], text=self.name_cleaner(new_subtab))
            globals()[f"{new_tab}_subtab_notebook"].pack(expand=1, fill="both")

            self.datahandler.df_tab_organizer()
            for tab_name in self.datahandler.tab_names:
                self.datahandler.df_subtab_creator(tab_name)


        self.tabs.pack(expand=1, fill="both")

    def destroy_tabs(self):
        
        # self.datahandler.df_tab_organizer()
        for tab_name in self.datahandler.tab_names:
            
            self.datahandler.df_subtab_creator(tab_name)

            for subtab_name in self.datahandler.subtabs:
                del(globals()[f"{subtab_name}_subtab"])

            del(globals()[f"{tab_name}_subtab_notebook"])
            globals()[f"{tab_name}_tab"].destroy()

        self.tabs.destroy()        


    def create_param_table(self, tab_name, subtab_name):
        self.current_df = self.datahandler.param_getter(tab_name, subtab_name)
        self.current_params = list(self.current_df.param.values)
        self.current_units = list(self.current_df.units.values)
        self.current_values = list(self.current_df.value.values)
        self.current_table_tab = tab_name
        self.current_table_subtab = subtab_name

        self.table_frame = globals()[f"{subtab_name}_subtab"]

        columns = ("Parameter", "Value", "Unit")

        self.current_Treeview = ttk.Treeview(self.table_frame, height=18, show="headings", columns=columns)  # 
        self.current_Treeview.bind('<Double-1>', self.set_cell_value)

        self.current_Treeview.column("Parameter", anchor='center', stretch=True)
        self.current_Treeview.column("Value", anchor='center', stretch=True)
        self.current_Treeview.column("Unit", anchor='center', stretch=True)


        self.current_Treeview.heading("Parameter", text="Parameter")
        self.current_Treeview.heading("Value", text="Value")
        self.current_Treeview.heading("Unit", text="Unit")


        self.current_Treeview.pack(side=LEFT, fill=BOTH)

        for i in range(len(self.current_params)):
            self.current_Treeview.insert('', i, values=(self.current_params[i], self.current_values[i],self.current_units[i]))


        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
                tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


        def newrow():
                        
            top= Toplevel(self)

            new_param = StringVar()
            new_val = StringVar()
            new_unit = StringVar()

            param_entry = Entry(top,  textvariable=new_param, width=25).grid(row=1,column=0, padx=5, pady=5)
            val_entry= Entry(top, textvariable=new_val, width= 25).grid(row=1,column=1, padx=(5,5), pady=5)
            unit_entry= Entry(top, textvariable=new_unit, width= 25).grid(row=1,column=2, padx=5, pady=5)
            
            param_label = Label(top, text="Parameter:").grid(row=0,column=0, padx=5, pady=5)
            var_label = Label(top, text="Value:").grid(row=0,column=1, padx=(5,5), pady=5)
            unit_label = Label(top, text="Unit:").grid(row=0,column=2, padx=5, pady=5)

            button= Button(top, text="Ok", command=lambda:close_win(top)).grid(row=2, column=1, pady=5)

            def close_win(top):
                if (not new_param.get()) or (not new_val.get()) or (not new_unit.get()):
                    tkinter.messagebox.showinfo("Warning!", "You forgot one of the inputs, you dingus.")
                elif (new_param.get()) and (new_val.get()) and (new_unit.get()):
                    self.datahandler.add_row(tab_name, subtab_name, self.datahandler.reverse_name_cleaner(new_param.get()), new_val.get(), new_unit.get())
                    top.destroy()
                    print(self.datahandler.param_getter(tab_name,subtab_name))
                    self.current_Treeview.destroy()
                    self.create_param_table(tab_name, subtab_name)

        newb = ttk.Button(self.table_frame, text='New Parameter', width=20, command=newrow)
        newb.place(x=420, y=(len(self.current_params) - 1) * 20 + 45)

    def set_cell_value(self, event):
        for item in self.current_Treeview.selection():

            self.id_column = self.current_Treeview.identify_column(event.x)
            self.id_row = self.current_Treeview.identify_row(event.y)

        self.cn = int(str(self.id_column).replace('#', ''))
        self.rn = int(str(self.id_row).replace('I', ''))

        self.pre = list(self.current_Treeview.item(self.id_row, 'values'))[0]


        
        self.entryedit = Text(self.table_frame, width=25, height=1)
        self.entryedit.place(x= 10 + (self.cn - 1) * 300, y=6 + self.rn * 20)

        def saveedit():
            self.current_Treeview.set(item, column=self.id_column, value=self.entryedit.get(0.0, "end"))

            self.entryedit.destroy()
            self.okb.destroy()

        self.okb = ttk.Button(self.table_frame, text='OK', width=4, command=saveedit)
        self.okb.place(x=265 + (self.cn - 1) * 300, y=2 + self.rn * 20)


        
        

        # for col in columns:
        #     self.current_Treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(self.current_Treeview, _col, False))

    def name_cleaner(self,entry):
        out = entry.replace("_", " ")
        out = out.capitalize()
        return out

    def focus(self, event):
        widget = self.focus_get()
        if isinstance(widget, ttk.Notebook):
            self.datahandler.df_tab_organizer()
            subtab_name = self.datahandler.reverse_name_cleaner(widget.tab(widget.select(), "text"))
            if not subtab_name in list(self.datahandler.tab_names):
                
                tab_name = self.datahandler.get_tab_from_subtab(subtab_name)

                if hasattr(self, 'current_Treeview'):
                    self.current_Treeview.destroy()

                self.create_param_table(tab_name, subtab_name)

                print(widget.tab(widget.select(), "text"), "has focus")

    def make_top_menu(self):
        self.menubar = Menu(self)
        self.master.config(menu=self.menubar)

        self.tabmenu = Menu(self.menubar)
        self.menubar.add_cascade(label='Tab Creation', menu=self.tabmenu)

        self.tabmenu.add_command(label='New Group', command=self.make_new_tab)
        self.tabmenu.add_command(label='New Object', command=self.make_new_subtab)

        self.menubar.add_command(label="Save to disk", command=self.save_to_disk)

    def make_new_tab(self):
        top= Toplevel(self)

        new_tab = StringVar()
        new_subtab = StringVar()
        new_param = StringVar()
        new_val = StringVar()
        new_unit = StringVar()

        tab_entry = Entry(top,  textvariable=new_tab, width=25).grid(row=1,column=0, padx=5, pady=5)
        subtab_entry = Entry(top,  textvariable=new_subtab, width=25).grid(row=1,column=1, padx=5, pady=5)
        param_entry = Entry(top,  textvariable=new_param, width=25).grid(row=3,column=0, padx=5, pady=5)
        val_entry= Entry(top, textvariable=new_val, width= 25).grid(row=3,column=1, padx=(5,5), pady=5)
        unit_entry= Entry(top, textvariable=new_unit, width= 25).grid(row=3,column=2, padx=5, pady=5)
        
        tab_label = Label(top, text="Group:").grid(row=0,column=0, padx=5, pady=5)
        subtab_label = Label(top, text="Object:").grid(row=0,column=1, padx=5, pady=5)
        param_label = Label(top, text="Parameter:").grid(row=2,column=0, padx=5, pady=5)
        var_label = Label(top, text="Value:").grid(row=2,column=1, padx=(5,5), pady=5)
        unit_label = Label(top, text="Unit:").grid(row=2,column=2, padx=5, pady=5)

        button= Button(top, text="Ok", command=lambda:close_win(top)).grid(row=4, column=1, pady=5)

        def close_win(top):
                if (not new_param.get()) or (not new_val.get()) or (not new_unit.get()):
                    tkinter.messagebox.showinfo("Warning!", "You forgot one of the inputs, you dingus.")
                elif (new_param.get()) and (new_val.get()) and (new_unit.get()):
                    self.datahandler.add_row(self.datahandler.reverse_name_cleaner(new_tab.get()), self.datahandler.reverse_name_cleaner(new_subtab.get()), self.datahandler.reverse_name_cleaner(new_param.get()), new_val.get(), new_unit.get())
                    print(self.datahandler.param_getter(self.datahandler.reverse_name_cleaner(new_tab.get()),self.datahandler.reverse_name_cleaner(new_subtab.get())))
                    # self.destroy_tabs()
                    top.destroy()
                    self.create_tabs(new_tab=self.datahandler.reverse_name_cleaner(new_tab.get()), new_subtab=self.datahandler.reverse_name_cleaner(new_subtab.get()))

    def make_new_subtab(self):
        top= Toplevel(self)

        self.datahandler.df_tab_organizer()
        dropdown_choices = [self.name_cleaner(i) for i in self.datahandler.tab_names]

        new_tab = StringVar()
        new_tab.set(dropdown_choices[0])

        new_subtab = StringVar()
        new_param = StringVar()
        new_val = StringVar()
        new_unit = StringVar()

        tab_entry = OptionMenu( top , new_tab , *dropdown_choices ).grid(row=1,column=0, padx=5, pady=5)
        subtab_entry = Entry(top,  textvariable=new_subtab, width=25).grid(row=1,column=1, padx=5, pady=5)
        param_entry = Entry(top,  textvariable=new_param, width=25).grid(row=3,column=0, padx=5, pady=5)
        val_entry= Entry(top, textvariable=new_val, width= 25).grid(row=3,column=1, padx=(5,5), pady=5)
        unit_entry= Entry(top, textvariable=new_unit, width= 25).grid(row=3,column=2, padx=5, pady=5)
        
        tab_label = Label(top, text="Group (choose one):").grid(row=0,column=0, padx=5, pady=5)
        subtab_label = Label(top, text="Object:").grid(row=0,column=1, padx=5, pady=5)
        param_label = Label(top, text="Parameter:").grid(row=2,column=0, padx=5, pady=5)
        var_label = Label(top, text="Value:").grid(row=2,column=1, padx=(5,5), pady=5)
        unit_label = Label(top, text="Unit:").grid(row=2,column=2, padx=5, pady=5)

        button= Button(top, text="Ok", command=lambda:close_win(top)).grid(row=4, column=1, pady=5)

        def close_win(top):
                if (not new_param.get()) or (not new_val.get()) or (not new_unit.get()) or (not new_subtab.get()):
                    tkinter.messagebox.showinfo("Warning!", "You forgot one of the inputs, you dingus.")
                elif (new_param.get()) and (new_val.get()) and (new_unit.get()) and (new_subtab.get()):
                    self.datahandler.add_row(self.datahandler.reverse_name_cleaner(new_tab.get()), self.datahandler.reverse_name_cleaner(new_subtab.get()), self.datahandler.reverse_name_cleaner(new_param.get()), new_val.get(), new_unit.get())
                    print(self.datahandler.param_getter(self.datahandler.reverse_name_cleaner(new_tab.get()),self.datahandler.reverse_name_cleaner(new_subtab.get())))
                    # self.destroy_tabs()
                    top.destroy()
                    self.create_tabs(new_tab=self.datahandler.reverse_name_cleaner(new_tab.get()), new_subtab=self.datahandler.reverse_name_cleaner(new_subtab.get()), subtabonly=True)

    def save_to_disk(self):
        res = tkinter.messagebox.askquestion('Save to disk', 'Do you really want to commit all changes to disk?')

        if res == 'yes' :
            self.datahandler.df_to_csv('data.csv')
            tkinter.messagebox.showinfo('Success', "Successfully saved changes to disk!\nLet's hope you didn't screw up...")
            
        else :
            tkinter.messagebox.showinfo('Return', 'Returning to main application\n(why waste my time like this?)')
#________________________________________
root = Tk()
app = Application(master=root)
app.mainloop()
