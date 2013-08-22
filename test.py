import tkinter
import tkinter.messagebox as tkMessageBox
import tkinter.simpledialog as tkSimpleDialog
import tkinter.filedialog as tkFileDialog
import tkinter.simpledialog as tkSimpleDialog
import os

#########################
#
#Global vars
#
#########################

labeltext = "Status"

########################
#
#Simple Dialog Class (Not used)
#
########################
class MyDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = string.atoi(self.e1.get())
        second = string.atoi(self.e2.get())
        print (first)

##########################
#
#Define Functions
#
###########################
def windowclose():
	if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()		

def tempwindow2():
	tkMessageBox.showwarning("Hi","close me")

def middlemouseclick(event):
	if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()

#####CAPTURE MOUSE MOTION AND UPDATE LABELS############
def mousemotion(event):
		sx.set(event.x)
		sy.set(event.y)

#####CAPTURE MOUSE CLICK AND UPDATE LABELS#############
def mouseclick(event):
		cx.set(event.x)
		cy.set(event.y)

########CHANGE THE BACKGROUND BASED ON SCALE VALUE######
def scaleupdate(sc):
		#print (scalevalue.get())
		if scalevalue.get() == 0:
			frame.config(bg="lightblue")
		elif scalevalue.get() == 1:
			frame.config(bg="blue")
		elif scalevalue.get() == 3:
			frame.config(bg="red")
		elif scalevalue.get() ==5:
			frame.config(bg="green")
		else:
			frame.config(bg="yellow")

########UPDATE THE LABELS IN THE STATUS BAR########
def labelupdate(newtext):
		l.set(newtext)
		if ckb.get():
			n.set(n.get()+5)
		else:
			n.set(n.get()+1)

###########INPUT DATA################
def inputdata():
	x = tkSimpleDialog.askinteger("Input","Multiplier")
	if x:
		tkMessageBox.showwarning("Yes",x)
		listbox.insert(END, x)
	else:
		tkMessageBox.showwarning("No","You did it wrong")

############SELECT FILE#################
def fileselect():
	filename = tkFileDialog.askopenfilename()
	if filename:
		tkMessageBox.showwarning("Yes", filename)
	else:
		tkMessageBox.showwarning("No", "You did it wrong")

#####################################
#
#MAIN
#
#####################################

root = Tk()

###########ROOT WINDOW PROPERTIES#####
root.resizable(False,False)
root.iconbitmap(default="")  ##input your own ico file here. this will replace the default red Tk icon
root.title("Test")
root.attributes("-alpha", 1.0)
root.protocol("WM_DELETE_WINDOW", windowclose)

###############main frame##############
frame = Frame(root,relief='raised', border=4, bg="lightblue", padx=12)
frame.bind("<a>", mousemotion)
frame.bind("<a>", middlemouseclick)
frame.grid(column =0,row=1, sticky='w')

#############CLICK HERE#################
label = Label(frame, text="Click Here", cursor="gumby")
label.bind("<Enter>", mouseclick)
label.grid(column=0,row=0)

############HELLO########################
message = Message(frame, text="Hello")
message.grid(column=1,row=0)

############SCALE##########################
scalevalue = DoubleVar()
scalevalue.set(0)
scale = Scale(frame, activebackground="blue", background="red", to="10", troughcolor="green", width="25", command= scaleupdate, variable=scalevalue )
scale.grid(column=0,row=1, columnspan=2)

###################STATUS BAR###############
l = StringVar()
l.set("Status")
status = Label(root, textvariable=l, bd=1, relief=SUNKEN, anchor='w')
status.grid(column=0, row=4, sticky='w')

n = IntVar()
n.set(0)
status2 = Label(root, textvariable=n, bd=1, relief=SUNKEN, anchor='w')
status2.grid(column=0, row=4, sticky='w', padx=40)

sx = IntVar()
sx.set(0)
statusx = Label(root, textvariable=sx, bd=1, relief=SUNKEN, anchor='w')
statusx.grid(column=0, row=4, sticky='w', padx=65)

sy = IntVar()
sy.set(0)
statusy = Label(root, textvariable=sy, bd=1, relief=SUNKEN, anchor='w')
statusy.grid(column=0, row=4, sticky='w', padx=95)

cx = IntVar()
cx.set(0)
statuscx = Label(root, textvariable=cx, bd=1, relief=SUNKEN, anchor='w')
statuscx.grid(column=0, row=4, sticky='w', padx=125)

cy = IntVar()
cy.set(0)
statuscy = Label(root, textvariable=cy, bd=1, relief=SUNKEN, anchor='w')
statuscy.grid(column=0,row=4,sticky='w', padx=140)

####################RADIO BUTTONS###########
v = IntVar()
radbutton = Radiobutton(frame, text = "Option 1", variable=v, value=1)
radbutton.grid(column = 2, row = 0, sticky = NW)

radbutton2 = Radiobutton(frame, text = "Option 2", variable=v, value=2)
radbutton2.grid(column = 2, row = 1, sticky = NW)

#################CHECK BUTTONS##############
ckb = IntVar()
ckbbutton = Checkbutton(frame, text = "Add 5", variable=ckb)
ckbbutton.grid(column = 2, row= 2, sticky=NW)

#################LIST BOX#####################

listbox = Listbox(frame, selectmode=MULTIPLE)
listbox.grid(column=2, row=3, sticky=NW)

listbox.insert(END, "zero")
listbox.insert(END, "one")
listbox.insert(END, "two")

###################IMAGES IN BASE64 ############
img00 = PhotoImage(format='gif', data="R0lGODlhKwAQAJEAACWgA/3bYYNOGgAAACwAAAAAKwAQAAACfIyPqcsrD2M0oAJqa8h29yAkITiG3HWmKWiUrdtpseZdtcfmJSyjvf2Z5Q671u0wA9I+RtLjZcwgfxglTTchjqS34JUrCUMQySOzih07Tb62eeneqSfU8vsmf65xZa8S/zI3dlLD5deRl1dlxdT4MYIA2TBJuSZ2iZkZVgAAOw==")
img01 = PhotoImage(format='gif', data="R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw==")
cat = PhotoImage(file="") ##place your own .gif file here
open = PhotoImage(format='gif', data="R0lGODlhEAAQAIcAADFKY0L/QplnAZpoApxqBJ5sBqBuCKJwCqNxC6RyDKVzDad1D6x6FLB+GLOBG7WCHbeEH7qHIr2KJcaaGcaaGsKPKsiVMMmWMcuYM8yZNMmgIc+iJte4QNq/bOKzQ+LBUP3VcP/bdfDkev/kf5SlvZylvbe3t5ytxqW11qm92r3GxrnK5P/XhP/rhP/viffwif/4k///mf//nP//pcTExMXFxc3NzdHR0cbW69jh8efv9+vz//r7/P///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAMAAAEALAAAAAAQABAAAAiZAAMIHEiwoMGDBzNkwHDBAkKBGXpI5MGjAsKIMjJm7CEhAoQHDhoIxNBDo0mJEhncCHChB4yXMGPKWFBjgs2bOG1+aIGAxoQYJk3G6DCBhQGfQGPClPFiAogCNAL8dEG1KtUZGjwQiPpTxoivYEfM4LBhQFSpMUKoXatWBAUBNQROUECXboIDBgoQGGDCxkAbNAILHuz34cGAADs=")

imglabel = Label(frame, image=cat)
imglabel.grid(column=3, row=0, rowspan=4)

############TOOLBAR#####################
toolbar = Frame(root)
b = Button(toolbar, image=open, width=20, command=tempwindow2)
b.grid(column=0, row=0, sticky='w')
b2 = Button(toolbar, image=img00, width=50, command=lambda: labelupdate("status"))
b2.grid(column=1, row=0)
toolbar.grid(column=0, row=0, sticky='w')

#######################MENU#################
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=fileselect)
filemenu.add_command(label="Quit", command=windowclose)

editmenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Input", command=inputdata)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label = "About", command=tempwindow2)
#######ROOT MAIN###########################
root.mainloop()