from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *
import tkinter.ttk as ttk
import pandas as pd
from PIL import ImageTk,Image
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
try:   
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import FigureCanvas2Tk as FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from numpy import *
from sympy import symbols, solve, Eq, lambdify
from sympy.abc import x as rpx,y as rpy
from sympy.parsing.sympy_parser import parse_expr,standard_transformations as st,implicit_multiplication_application as ima
from sympy.core import numbers as num
from mpmath import *
import sys
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------------------------------------

def file_dialogue_pie():
	filename = filedialog.askopenfilename(initialdir = "/", title = "Select a file")
	# print(filename)
	if filename.endswith('.csv') == False:
		showerror("OOPS!", "Please upload csv file only.")
	else:
		data = pd.read_csv(filename)
		print(data)
		head = data.columns.tolist()
		m = data[head[0]].tolist()
		n = data[head[1]].tolist()

		plt.pie(n, labels = m, autopct = '%0.2f%%', shadow = True, colors = ['blue', 'pink', 'orange', 'yellow', 'green'])
		# explode = [0, 0, 0.2, 0,0]
	
		plt.title(head[2])
		plt.show()

# ---------------------------------------------------------------------------------------------------------

def file_dialogue_line():
	filename = filedialog.askopenfilename(initialdir = "/", title = "Select a file")
	# print(filename)
	if filename.endswith('.csv') == False:
		showerror("OOPS!", "Please upload csv file only.")
	else:
		data = pd.read_csv(filename)
		header = data.columns.tolist()
		
		r = data[header[0]].tolist()
		y1 = data[header[1]].tolist()
		y2 = data[header[2]].tolist()
		y3 = data[header[3]].tolist()

		plt.plot(r, y1, marker = 'o',linewidth = 3, markersize = 10, label = header[1])
		plt.plot(r, y2, marker = 'o', linewidth = 3, markersize = 10, label = header[2])
		plt.plot(r, y3, marker = 'o', linewidth = 3, markersize = 10, label = header[3])
		
		plt.xlabel(header[0])
		plt.ylabel(header[4])
		plt.title(filename)
		
		# for i, v in enumerate(y1):
		# 	plt.text(i, v+2000, "%d" %v, ha="center")

		# for i, v in enumerate(y2):
		# 	plt.text(i, v+2000, "%d" %v, ha="center")

		# for i, v in enumerate(y3):
		# 	plt.text(i, v+2000, "%d" %v, ha="center")

		plt.legend()
		plt.grid()
		plt.show()

# -------------------------------------------------------------------------------------------------------------

def file_dialogue_bar():
	filename = filedialog.askopenfilename(initialdir = "/", title = "Select a file")
	# print(filename)
	if filename.endswith('.csv') == False:
		showerror("OOPS!", "Please upload csv file only.")
	else:
		data = pd.read_csv(filename)
		head = data.columns.tolist()

		x=(data[head[0]]).tolist()	
		y=(data[head[1]]).tolist()
		
		plt.bar(x, y, color = ['red', 'cyan', 'green', 'blue', 'orange', 'yellow', 'purple', 'magenta'])
		plt.xlabel(head[0])
		plt.ylabel(head[1])
		xlocs, xlabs = plt.xticks()
		xlocs=[i+1 for i in range(0,10)]

		for i, v in enumerate(y):
		    plt.text(xlocs[i] - 1.13, v + 0.3, str(v))
		plt.show()

# -------------------------------------------------------------------------------------------------

csc = lambda t: 1/np.sin(t)
csc_func = np.vectorize(csc)
sec = lambda t: 1/np.cos(t)
sec_func = np.vectorize(sec)
cot = lambda t: 1/np.tan(t)
cot_func = np.vectorize(cot)

def plotEqn(event,a1,b):
	global line, plotted, colors
	try:
		remove()
		eqn = equation_var.get().split('=')
		if eqn[0]=='y' or eqn[1]=='y' or ('y' in eqn[0]+eqn[1] and 'x' not in eqn[0]+eqn[1]):
			ans = solve(Eq(parse_expr(eqn[0], transformations=trans),parse_expr(eqn[1],transformations=trans)),y)
			rps = rpx
		else:
			ans = solve(Eq(parse_expr(eqn[0], transformations=trans),parse_expr(eqn[1],transformations=trans)),x)
			rps = rpy

		for i in ans:
			j = i.evalf()
			if isinstance(j,(num.Integer,num.Float)):
				c = np.empty(300000)
				c.fill(j)
			else:
				f = lambdify(rps,i,["scipy", "numpy", {'csc':csc_func, 'sec':sec_func, 'cot':cot_func}])
				c = f(X)
			if eqn[0]=='x' or eqn[1]=='x':
				line.append(a.plot(c,X)[0])
			else:
				line.append(a.plot(X,c)[0])
			line[-1].set_color(colors[len(plotted)])
		canvas.draw()
	except Exception as e:
		print('callback',e)

def fill(event):
	global line
	print(Listbox1.curselection())
	if line != []:
		Listbox1.insert(END,equation_var.get())
		plotted.append([equation_var.get(),line])
		line = []
		TEntry1.delete(0,END)
        

def remove():
	global line
	if line != [] :
		for i in range(len(line)):
			line[i].remove()
		canvas.draw()
		line = []

def make_eqn(event,app):
    TEntry1.insert(TEntry1.index(INSERT),app)
    if app[-2:]=='()':
        TEntry1.icursor(TEntry1.index(INSERT)-1)

def backspace(event):
    now = equation_var.get()
    curs =TEntry1.index(INSERT)
    equation_var.set(now[:curs-1]+now[curs:])
    TEntry1.icursor(curs-1)
    print(event)

# -------------------------------------------------------------------------------------------------

def totypeselection():
	master.withdraw()
	analytical_window.deiconify()

def back2analytical():
	master.withdraw()
	ask_window_pie.withdraw()
	ask_window_line.withdraw()
	ask_window_bar.withdraw()
	analytical_window.deiconify()

def back2master():
	analytical_window.withdraw()
	master.deiconify()

def toaskpie():
	analytical_window.withdraw()
	ask_window_pie.deiconify()

def toaskline():
	analytical_window.withdraw()
	ask_window_line.deiconify()

def toaskbar():
	analytical_window.withdraw()
	ask_window_bar.deiconify()

def tomath():
	master.withdraw()
	mathematical_window.deiconify()

# -----------------------------------------------------------------------------------------------------

master = Tk()
master.title("Graph Generator")
master.geometry("{0}x{0}+-7+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

# image1 = PhotoImage(file = r"assets/g1.gif")
# label1 = Label(master, image = image1)
# label1.place(x = 0, y = 0)

img = ImageTk.PhotoImage(Image.open("assets/g1.jpg"))  
l=Label(master, image=img)
l.place(x = 0, y = 0)

analytical_button = Button(master, text = "Analytical Graph", width = 18, 
	borderwidth = 9, fg = "dark green", font = ('Arial', 20, 'bold'), command = totypeselection)
analytical_button.place(x = 480, y = 230)

mathematical_button = Button(master, text = "Mathematical Graph", width = 18,
	borderwidth = 9, fg = "dark green", font = ('Arial', 20, 'bold'), command = tomath)
mathematical_button.place(x = 480, y = 310)

def quit():
	if askokcancel("Quit", "Do you want to quit?"):
		master.destroy()	

master.protocol("WM_DELETE_WINDOW", quit)

# ------------------------------------------------------------------------------------------------------------

ask_window_pie = Toplevel(master)
ask_window_pie.title("Upload csv for Pie Chart")
ask_window_pie.geometry("{0}x{0}+-7+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

l=Label(ask_window_pie, image=img)
l.place(x = 0, y = 0)

upload_button = Button(ask_window_pie, text = "Upload a file", width = 12,
 	borderwidth = 7, fg = "dark green",  font = ('Arial', 20, 'bold'), command = file_dialogue_pie)
upload_button.place(x = 510, y = 250)

back_button = Button(ask_window_pie, text = "Back", width = 12, 
	borderwidth = 7, fg = "dark green", font = ('Arial', 20, 'bold'), command = back2analytical)
back_button.place(x = 510, y = 330)

ask_window_pie.withdraw()

# ------------------------------------------------------------------------------------------------------------

ask_window_line = Toplevel(master)
ask_window_line.title("Upload csv for Line Graph")
ask_window_line.geometry("{0}x{0}+-7+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

l=Label(ask_window_line, image=img)
l.place(x = 0, y = 0)

upload_button = Button(ask_window_line, text = "Upload a file", width = 12,
 	borderwidth = 7, fg = "dark green",  font = ('Arial', 20, 'bold'), command = file_dialogue_line)
upload_button.place(x = 510, y = 250)

back_button = Button(ask_window_line, text = "Back", width = 12,
	borderwidth = 7, fg = "dark green",  font = ('Arial', 20, 'bold'), command = back2analytical)
back_button.place(x = 510, y = 330)

ask_window_line.withdraw()

# --------------------------------------------------------------------------------------------------

ask_window_bar = Toplevel(master)
ask_window_bar.title("Upload csv for bar Graph")
ask_window_bar.geometry("{0}x{0}+-7+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

l=Label(ask_window_bar, image=img)
l.place(x = 0, y = 0)

upload_button = Button(ask_window_bar, text = "Upload a file", width = 12,
	borderwidth = 7, fg = "dark green",  font = ('Arial', 20, 'bold'), command = file_dialogue_bar)
upload_button.place(x = 510, y = 250)

back_button = Button(ask_window_bar, text = "Back", width = 12,
 	borderwidth = 7, fg = "dark green",  font = ('Arial', 20, 'bold'), command = back2analytical)
back_button.place(x = 510, y = 330)

ask_window_bar.withdraw()

# -------------------------------------------------------------------------------------------------

analytical_window = Toplevel(master)
analytical_window.title("Type Selection")
analytical_window.geometry("{0}x{0}+-7+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

l=Label(analytical_window, image=img)
l.place(x = 0, y = 0)

pie_button = Button(analytical_window, text = "Pie Chart", borderwidth = 7, 
	fg = "dark green", width = 12, font = ('Arial', 20, 'bold'), command = toaskpie)
pie_button.place(x = 510, y = 190)

line_button = Button(analytical_window, text = "Line Graph", borderwidth = 7,
	fg = "dark green", width = 12, font = ('Arial', 20, 'bold'), command = toaskline)
line_button.place(x = 510, y = 270)

bar_button = Button(analytical_window, text = "Bar Graph", borderwidth = 7,
	fg = "dark green", width = 12, font = ('Arial', 20, 'bold'), command = toaskbar)
bar_button.place(x = 510, y = 350)

back_button = Button(analytical_window, text = "Back", borderwidth = 7,
	fg = "dark green", width = 12, font = ('Arial', 20, 'bold'), command = back2master)
back_button.place(x = 510, y = 430)

analytical_window.withdraw()

# -------------------------------------------------------------------------------------------------

fig = Figure( dpi=100)
fig.set_tight_layout(True)
a = fig.add_subplot(111)
trans = (st+(ima,))
t = arange(-314, 314, 0.01)
major_loc = matplotlib.ticker.MaxNLocator(10)
major_loc1 = matplotlib.ticker.MaxNLocator(6)
minor_loc = matplotlib.ticker.AutoMinorLocator(5)
minor_loc1 = matplotlib.ticker.AutoMinorLocator(5)
a.xaxis.set_major_locator(major_loc)
a.yaxis.set_major_locator(major_loc1)
a.yaxis.set_minor_locator(minor_loc)
a.xaxis.set_minor_locator(minor_loc1)
a.set_ylim(-13,13,1)
y,x = symbols('y x')
a.set_xlim(-23,23,1)
a.set_aspect('equal',anchor='C')
a.spines['left'].set_position('zero')
a.spines['bottom'].set_position('zero')
a.xaxis.set_ticks_position('bottom')
a.yaxis.set_ticks_position('left')
a.grid(which='major',alpha=0.9,linestyle=':',color='k')
a.grid(which='minor',alpha=0.5,linestyle=':',color='k')
plt.ion()

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_compcolor = '#d9d9d9'
_ana1color = '#d9d9d9'
_ana2color = '#d9d9d9'
font10 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
    "roman -underline 0 -overstrike 0"
font9 = "-family {Segoe UI} -size 10 -weight normal -slant "  \
    "roman -underline 0 -overstrike 0"
style = ttk.Style()
if sys.platform == "win32":
    style.theme_use('winnative')
style.configure('.',background=_bgcolor)
style.configure('.',foreground=_fgcolor)
style.configure('.',font=font9)
style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])

mathematical_window = Toplevel(master)
mathematical_window.geometry("{0}x{0}+-7+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
mathematical_window.title("Graphing Calculator")
mathematical_window.configure(background="#d9d9d9")
mathematical_window.configure(highlightbackground="#d9d9d9")
mathematical_window.configure(highlightcolor="black")

global X
X = np.linspace(-250.0, 250.0, 300000)
line = []
plotted =[]
colors =['b', 'g', 'r', 'c', 'm', 'y','#1f77b4','#ff7f0e','#17becf','#9467bd']
equation_var = StringVar()
equation_var.trace('w', plotEqn)
TEntry1 = ttk.Entry(mathematical_window, textvariable=equation_var)
TEntry1.place(relx=0.01, rely=0.45, relheight=0.04, relwidth=0.17)
TEntry1.configure(width=236)
TEntry1.configure(background = "#d9d9d9")
TEntry1.configure(takefocus = "")
TEntry1.configure(cursor = "ibeam")

pi = ttk.Button(mathematical_window)
pi.place(relx=0.0, rely=0.52, height=35, width=26)
pi.configure(takefocus = "")
pi.configure(text = '''π''')
pi.bind('<Button-1>', lambda event: make_eqn(event,'3.142'))

exp = ttk.Button(mathematical_window)
exp.place(relx=0.02, rely=0.52, height=35, width=26)
exp.configure(takefocus="")
exp.configure(text='''e''')
exp.bind('<Button-1>',lambda event:make_eqn(event,'2.718'))

Listbox1 = Listbox(mathematical_window)
Listbox1.place(relx=0.01, rely=0.01, relheight=0.43, relwidth=0.17)
Listbox1.configure(background="white")
Listbox1.configure(disabledforeground="#a3a3a3")
Listbox1.configure(font="TkFixedFont")
Listbox1.configure(foreground="#000000")
Listbox1.configure(highlightbackground="#d9d9d9")
Listbox1.configure(highlightcolor="black")
Listbox1.configure(selectbackground="#c4c4c4")
Listbox1.configure(selectforeground="black")
Listbox1.configure(selectmode=SINGLE)
Listbox1.configure(width=236)

sin = ttk.Button(mathematical_window)
sin.place(relx=0.0, rely=0.57, height=35, width=56)
sin.configure(takefocus="")
sin.configure(text='''sin''')
sin.bind('<Button-1>',lambda event:make_eqn(event,'sin()'))

cos = ttk.Button(mathematical_window)
cos.place(relx=0.0, rely=0.62, height=35, width=56)
cos.configure(takefocus="")
cos.configure(text='''cos''')
cos.bind('<Button-1>',lambda event:make_eqn(event,'cos()'))

tan = ttk.Button(mathematical_window)
tan.place(relx=0.0, rely=0.67, height=35, width=56)
tan.configure(takefocus="")
tan.configure(text='''tan''')
tan.bind('<Button-1>',lambda event:make_eqn(event,'tan()'))

Canvas1 = Canvas(mathematical_window)
Canvas1.place(relx=0.19, rely=0.01, relheight=0.95, relwidth=0.8)
Canvas1.configure(background="#d9d9d9")
Canvas1.configure(borderwidth="2")
Canvas1.configure(insertbackground="black")
Canvas1.configure(relief=RIDGE)
Canvas1.configure(selectbackground="#c4c4c4")
Canvas1.configure(selectforeground="black")
Canvas1.configure(width=1092)

canvas = FigureCanvasTkAgg(fig, master=Canvas1)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas.get_tk_widget().configure(width=1093)

toolbar = NavigationToolbar2TkAgg(canvas,Canvas1)
toolbar.update()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

csc = ttk.Button(mathematical_window)
csc.place(relx=0.0, rely=0.72, height=35, width=56)
csc.configure(takefocus="")
csc.configure(text='''csc''')
csc.bind('<Button-1>',lambda event:make_eqn(event,'csc()'))

sec = ttk.Button(mathematical_window)
sec.place(relx=0.0, rely=0.77, height=35, width=56)
sec.configure(takefocus="")
sec.configure(text='''sec''')
sec.bind('<Button-1>',lambda event:make_eqn(event,'sec()'))

cot = ttk.Button(mathematical_window)
cot.place(relx=0.0, rely=0.82, height=35, width=56)
cot.configure(takefocus="")
cot.configure(text='''cot''')
cot.bind('<Button-1>',lambda event:make_eqn(event,'cot()'))


no_1 = ttk.Button(mathematical_window)
no_1.place(relx=0.05, rely=0.57, height=35, width=26)
no_1.configure(takefocus="")
no_1.configure(text='''1''')
no_1.bind('<Button-1>',lambda event:make_eqn(event,'1'))

no_2 = ttk.Button(mathematical_window)
no_2.place(relx=0.07, rely=0.57, height=35, width=26)
no_2.configure(takefocus="")
no_2.configure(text='''2''')
no_2.bind('<Button-1>',lambda event:make_eqn(event,'2'))

no_3 = ttk.Button(mathematical_window)
no_3.place(relx=0.09, rely=0.57, height=35, width=26)
no_3.configure(takefocus="")
no_3.configure(text='''3''')
no_3.bind('<Button-1>',lambda event:make_eqn(event,'3'))


add = ttk.Button(mathematical_window)
add.place(relx=0.11, rely=0.57, height=35, width=26)
add.configure(takefocus="")
add.configure(text='''+''')
add.bind('<Button-1>',lambda event:make_eqn(event,'+'))

no_4 = ttk.Button(mathematical_window)
no_4.place(relx=0.05, rely=0.62, height=35
        , width=26)
no_4.configure(takefocus="")
no_4.configure(text='''4''')
no_4.bind('<Button-1>',lambda event:make_eqn(event,'4'))

no_5 = ttk.Button(mathematical_window)
no_5.place(relx=0.07, rely=0.62, height=35
        , width=26)
no_5.configure(takefocus="")
no_5.configure(text='''5''')
no_5.bind('<Button-1>',lambda event:make_eqn(event,'5'))

no_6 = ttk.Button(mathematical_window)
no_6.place(relx=0.09, rely=0.62, height=35
        , width=26)
no_6.configure(takefocus="")
no_6.configure(text='''6''')
no_6.bind('<Button-1>',lambda event:make_eqn(event,''))

min_button = ttk.Button(mathematical_window)
min_button.place(relx=0.11, rely=0.62, height=35
        , width=26)
min_button.configure(takefocus="")
min_button.configure(text='''-''')
min_button.bind('<Button-1>',lambda event:make_eqn(event,'-'))

no_7 = ttk.Button(mathematical_window)
no_7.place(relx=0.05, rely=0.67, height=35
        , width=26)
no_7.configure(takefocus="")
no_7.configure(text='''7''')
no_7.bind('<Button-1>',lambda event:make_eqn(event,'7'))

no_8 = ttk.Button(mathematical_window)
no_8.place(relx=0.07, rely=0.67, height=35
        , width=26)
no_8.configure(takefocus="")
no_8.configure(text='''8''')
no_8.bind('<Button-1>',lambda event:make_eqn(event,'8'))

no_9 = ttk.Button(mathematical_window)
no_9.place(relx=0.09, rely=0.67
        , height=35, width=26)
no_9.configure(takefocus="")
no_9.configure(text='''9''')
no_9.bind('<Button-1>',lambda event:make_eqn(event,'9'))

mul = ttk.Button(mathematical_window)
mul.place(relx=0.11, rely=0.67
        , height=35, width=26)
mul.configure(takefocus="")
mul.configure(text='''*''')
mul.bind('<Button-1>',lambda event:make_eqn(event,'*'))

l_brac = ttk.Button(mathematical_window)
l_brac.place(relx=0.05, rely=0.72
        , height=35, width=26)
l_brac.configure(takefocus="")
l_brac.configure(text='''(''')
l_brac.bind('<Button-1>',lambda event:make_eqn(event,'('))

no_0 = ttk.Button(mathematical_window)
no_0.place(relx=0.07, rely=0.72
        , height=35, width=26)
no_0.configure(takefocus="")
no_0.configure(text='''0''')
no_0.bind('<Button-1>',lambda event:make_eqn(event,'0'))

r_brac = ttk.Button(mathematical_window)
r_brac.place(relx=0.09, rely=0.72
        , height=35, width=26)
r_brac.configure(takefocus="")
r_brac.configure(text=''')''')
r_brac.bind('<Button-1>',lambda event:make_eqn(event,')'))

div = ttk.Button(mathematical_window)
div.place(relx=0.11
        , rely=0.72, height=35, width=26)
div.configure(takefocus="")
div.configure(text='''/''')
div.bind('<Button-1>',lambda event:make_eqn(event,'/'))

mod = ttk.Button(mathematical_window)
mod.place(relx=0.05
        , rely=0.77, height=35, width=26)
mod.configure(takefocus="")
mod.configure(text='''|x|''')
mod.bind('<Button-1>',lambda event:make_eqn(event,'abs()'))

pow_button = ttk.Button(mathematical_window)
pow_button.place(relx=0.07
        , rely=0.77, height=35, width=26)
pow_button.configure(takefocus="")
pow_button.configure(text='xⁿ')
pow_button.bind('<Button-1>',lambda event:make_eqn(event,'**'))

sqr = ttk.Button(mathematical_window)
sqr.place(relx=0.09
        , rely=0.77, height=35, width=26)
sqr.configure(takefocus="")
sqr.configure(text='''√''')
sqr.bind('<Button-1>',lambda event:make_eqn(event,'sqrt()'))

log = ttk.Button(mathematical_window)
log.place(relx=0.11
        , rely=0.77, height=35, width=26)
log.configure(takefocus="")
log.configure(text='''ln''')
log.bind('<Button-1>',lambda event:make_eqn(event,'log()'))

eql = ttk.Button(mathematical_window)
eql.place(relx=0.05
        , rely=0.82, height=35, width=26)
eql.configure(takefocus="")
eql.configure(text='''=''')
eql.bind('<Button-1>',lambda event:make_eqn(event,'='))

dec = ttk.Button(mathematical_window)
dec.place(relx=0.07
        , rely=0.82, height=35, width=26)
dec.configure(takefocus="")
dec.configure(text='''.''')
dec.bind('<Button-1>',lambda event:make_eqn(event,'.'))

var_x = ttk.Button(mathematical_window)
var_x.place(relx=0.09
        , rely=0.82, height=35, width=26)
var_x.configure(takefocus="")
var_x.configure(text='''x''')
var_x.bind('<Button-1>',lambda event:make_eqn(event,'x'))

var_y = ttk.Button(mathematical_window)
var_y.place(relx=0.11
        , rely=0.82, height=35, width=26)
var_y.configure(takefocus="")
var_y.configure(text='''y''')
var_y.bind('<Button-1>',lambda event:make_eqn(event,'y'))

bckspc = ttk.Button(mathematical_window)
bckspc.place(relx=0.14
        , rely=0.57, height=75, width=46)
bckspc.configure(takefocus="")
bckspc.configure(text='''⌫''')
bckspc.configure(width=46)
bckspc.bind('<Button-1>',lambda event:backspace(event))

enter = ttk.Button(mathematical_window)
enter.place(relx=0.14, rely=0.68, height=75, width=46)
enter.configure(takefocus="")
enter.configure(text='''Enter''')
enter.configure(width=46)
enter.bind('<Button-1>',lambda event:fill(event))

mathematical_window.withdraw()

master.mainloop()
