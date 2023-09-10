from tkinter import *
from tkmacosx import Button
from tkinter.font import Font
from random import randint

lista = [[randint(0,9) for i in range(10)] for j in range(3)]
first = second = firstpos = secondpos = None


def Set():
    global first, second, firstpos, secondpos
    first = second = firstpos = secondpos = None

def Wrong(pos1, pos2, color):
    global buttons
    buttons[pos1[0]][pos1[1]].config(bg=color)
    buttons[pos2[0]][pos2[1]].config(bg=color)
    root.after(1500, lambda :Wrong(pos1,pos2, "white"))



def Check(x,y):
    if x == y or x+y == 10:
        return True
    return False




def Correct(x,y):
    if abs(x[0] - y[0]) == 1 and abs(x[1] - y[1]) == 9:
        return True
    if abs(x[0] - y[0]) > 1 or abs(x[1] - y[1]) > 1 or (x == y):
        return False
    return True


def Click(x, pos):
    global first, second, firstpos, secondpos, buttons, score
    if first is None:
        first = x
        firstpos = pos
        return None
    else:
        second = x
        secondpos = pos
        if Correct(firstpos, secondpos):
            if Check(first, second):
                score.set(score.get()+1)

                buttons[firstpos[0]][firstpos[1]].config(state=DISABLED)
              #  del buttons[firstpos[0]][firstpos[1]]

                buttons[secondpos[0]][secondpos[1]].config(state=DISABLED)
              #  del buttons[secondpos[0]][secondpos[1]]

                Set()
                return None
            else:
                Wrong(firstpos, secondpos, "red")
                Set()
                return None
        else:
            Wrong(firstpos, secondpos, "red")
            Set()
            return None


root = Tk()
#root.geometry("300x300")
score = IntVar(value=0)
rules = Label(root, text="+1 - 2 sąsiadujące identyczne\n"
                         "+1 - 2 sąsiadujące z sumą 10\n"
                         "+1 - pierwszy plus ostatni z sąsiednich rzędów\n identyczne lub z sumą 10")
lower_frame = Frame(root)
text = Label(lower_frame, text="Twój wynik to:")
score_label = Label(lower_frame, textvariable=score)
frame = Frame(root, bg="grey")
rules.pack()
frame.pack(fill="both", expand=True)
lower_frame.pack()
text.grid(row=0, column=0)
score_label.grid(row=0, column=1)
buttons = [[] for _ in lista]
for i in range(len(lista)):
    for j in range(len(lista[i])):
        text = lista[i][j]
        pos = (i, j)
        b = Button(frame, text=text,width=35, height=35, activebackground="white",
                   font=Font(size=25), command=lambda x=text,pos=pos:Click(x,pos))
        b.grid(row=i, column=j)
        buttons[i].append(b)
root.mainloop()



