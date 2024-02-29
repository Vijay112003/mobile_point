import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS mobiles(
            id Integer Primary Key,
            name text UNIQUE,
            intime time(8) NOT NULL
        )
        """
        self.cur.execute(sql)
        self.con.commit()

        sql="""
        CREATE TABLE IF NOT EXISTS TOKENS(
            tok integer Primary Key
        )
        """
        self.cur.execute(sql)
        self.con.commit()
        #self.cur.execute("SELECT * from TOKENS")
        #rows = self.cur.fetchall()
        #print(rows)
        

    # Insert Function
    def insert(self, tok, name):
        nowt = datetime.now()
        #inhour=nowt.hour
        #inmin=nowt.minute
        #insec=nowt.second
        intim=str(nowt.hour-12 if nowt.hour>12 else nowt.hour)+":"+str("0"+str(nowt.minute) if nowt.minute<10 else nowt.minute)+":"+str("0"+str(nowt.second) if nowt.second<10 else nowt.second)
        self.cur.execute("insert into mobiles (id,name,intime) values (?,?,?)",
                         (tok,name,intim))
        self.con.commit()

    # Insert into token table
    def inserttok(self, tok):
        self.cur.execute("insert into TOKENS (tok) values (?)",(tok,))
        self.con.commit()

    # Fetch All Data from DB
    def fetch(self):
        self.cur.execute("SELECT * from mobiles")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    #during adding
    def fetchtok(self):
        self.cur.execute("SELECT tok from TOKENS LIMIT 1")
        rows=self.cur.fetchall()
        row=rows[0]
        return row[0]

    #delete token
    def deletetok(self,tok):
        self.cur.execute("delete from TOKENS where tok=?",(tok,))
        self.con.commit()

    def tokcount(self):
        self.cur.execute("SELECT COUNT(tok) from TOKENS")
        counts=self.cur.fetchall()
        count=counts[0]
        return count[0]
        

    #during deletion
    def fetchone(self,roll):
        self.cur.execute("SELECT id,intime from mobiles where name=?", (roll,))
        rows=self.cur.fetchall()
        row=rows[0]
        return row

    # Delete a Record in DB
    def remove(self, id):
        self.cur.execute("delete from mobiles where id=?", (id,))
        self.con.commit()
    

    

db = Database("studmobile.db")
root = Tk()
root.title("MOBILE POINT")
root.geometry("1280x720+0+0")
root.config(bg="#2c3e50")
#root.iconbitmap("favicon.ico")
root.state("zoomed")

for i in range(1,1001):
    db.inserttok(i)


name = StringVar()
tok = StringVar()
mob = StringVar()
roll=StringVar()
token=StringVar()
rolldel=StringVar()
tokendel=StringVar()

# Entries Frame
entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="MOBILE POINT", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, column=0, padx=10, pady=20, sticky="w")

lbltokens = Label(entries_frame, text="Total tokens:", font=("Calibri", 16), bg="#535c68", fg="white")
lbltokens.grid(row=0, column=2, padx=10, pady=10, sticky="w")
lbltokens = Label(entries_frame, text="1000", font=("Calibri", 16), bg="#535c68", fg="cyan")
lbltokens.grid(row=0, column=3, padx=10, pady=10, sticky="w")

lbltokens = Label(entries_frame, text="Balance tokens:", font=("Calibri", 16), bg="#535c68", fg="white")
lbltokens.grid(row=0, column=4, padx=10, pady=10, sticky="w")
lbltokens = Label(entries_frame, textvariable=tok, font=("Calibri", 16), bg="#535c68", fg="yellow")
lbltokens.grid(row=0, column=5, padx=10, pady=10, sticky="w")

lbltokens = Label(entries_frame, text="Mobiles:", font=("Calibri", 16), bg="#535c68", fg="white")
lbltokens.grid(row=0, column=6, padx=10, pady=10, sticky="w")
lbltokens = Label(entries_frame, textvariable=mob, font=("Calibri", 16), bg="#535c68", fg="red")
lbltokens.grid(row=0, column=7, padx=10, pady=10, sticky="w")

lblName = Label(entries_frame, text="Roll Number", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtName = Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=30)
txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lblroll = Label(entries_frame, textvariable=roll, font=("Calibri", 16), bg="#535c68", fg="cyan")
lblroll.grid(row=1, column=4, padx=10, pady=10, sticky="w")
lblto = Label(entries_frame, textvariable=token, font=("Calibri", 16), bg="#535c68", fg="cyan")
lblto.grid(row=1, column=5, padx=10, pady=10, sticky="w")

lblrolldel = Label(entries_frame, textvariable=rolldel, font=("Calibri", 16), bg="#535c68", fg="red")
lblrolldel.grid(row=1, column=7, padx=10, pady=10, sticky="w")
lbltodel = Label(entries_frame, textvariable=tokendel, font=("Calibri", 16), bg="#535c68", fg="red")
lbltodel.grid(row=1, column=8, padx=10, pady=10, sticky="w")







def getData(event):
    try:
        selected_row = tv.focus()
        data = tv.item(selected_row)
        global row
        row = data["values"]
        #print(row)
        name.set(row[1])
    except:
        messagebox.showinfo("Mobile point", "Please fill the Roll number or select any Roll number")
    
def displaytok(t):
    token.set(t)
    roll.set(txtName.get()+" :")
def displaytokdel(t):
    tokendel.set(t)
    rolldel.set(txtName.get()+" :")
def balanceTokens():
    count=db.tokcount()
    tok.set(count)
    mob.set(1000-count)
def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)
    balanceTokens()


def add_employee():
    if txtName.get() == "" :
        messagebox.showerror("Mobile point", "TextField is empty, please fill the roll number")
    else:
        try:
            token=db.fetchtok()
            db.deletetok(token)
            db.insert(token,txtName.get())
            messagebox.showinfo("Mobile point", token)
            displaytok(token)
        except:
            db.inserttok(token)
            messagebox.showinfo("Mobile point", "Already tokened")
        clearAll()
    displayAll()






def delete_employee():
    try:
        tok=db.fetchone(txtName.get())
        db.remove(tok[0])
        db.inserttok(tok[0])
        nowt = datetime.now()
        outtim=str(nowt.hour-12 if nowt.hour>12 else nowt.hour)+":"+str("0"+str(nowt.minute) if nowt.minute<10 else nowt.minute)+":"+str("0"+str(nowt.second) if nowt.second<10 else nowt.second)
        displ="Token no:"+str(tok[0])+"\nOUT TIME:"+str(outtim)
        messagebox.showinfo("Mobile point", displ)
        displaytokdel(tok[0])
        clearAll()
    except:
        if txtName.get()=="":
            messagebox.showinfo("Mobile point", "Fill the textField or select any row")
        else:
            messagebox.showinfo("Mobile point", "Not Entered")
            clearAll()
    displayAll()
        


def clearAll():
    if txtName.get()=="":
        messagebox.showinfo("Mobile point", "TextField is already empty")
    else:
        name.set("")
    displayAll()
    
btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")

btnAdd = Button(btn_frame, command=add_employee, text="Allocate slot", width=15, font=("Calibri", 16, "bold"), fg="white",
                bg="#16a085", bd=0).grid(row=0, column=0, padx=10)

btnDelete = Button(btn_frame, command=delete_employee, text="Deallocate slot", width=15, font=("Calibri", 16, "bold"),
                   fg="white", bg="#c0392b",
                   bd=0).grid(row=0, column=1, padx=10)
btnClear = Button(btn_frame, command=clearAll, text="Clear Entry", width=15, font=("Calibri", 16, "bold"), fg="white",
                  bg="#f39c12",
                  bd=0).grid(row=0, column=2, padx=10)

# Table Frame
tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=180, width=1980, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18),rowheight=100)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3), style="mystyle.Treeview")
tv.heading("1", text="Token Number")
tv.column("1", anchor=CENTER, stretch=NO, width=200)
tv.heading("2", text="Roll Number")
tv.column("2", anchor=CENTER, stretch=NO, width=200)
tv.heading("3", text="Intime")
tv.column("3", anchor=CENTER, stretch=NO, width=200)
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

#displayAll()
root.mainloop()
