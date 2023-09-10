from tkinter import *
from tkinter import messagebox
from tkmacosx import Button
from tkinter.font import Font
from random import randint
from time import time

def Final_score(x):
    global max_score_value
    if x > max_score_value:
        max_score_value = x

def Fill():
    global buttons, frame
    for i in range(len(buttons)):
        while len(buttons[i]) < 10:
            text = randint(1,9)
            pos = (i, len(buttons[i]))
            buttons[i].append(Button(frame, text=text,width=35, height=35, activebackground="white",
                       font=Font(size=25), command=lambda x=text,pos=pos:Click(x,pos)))
            buttons[i][pos[1]].grid(row=i, column=pos[1])

def Restart():
    msg_box = messagebox.askyesno("Nowa gra", "Zrestartować?")

    if msg_box:
        root.destroy()
        main()

def counter():
    global start, score
    playtime = 60
    current = playtime - (time() - start)
    timer.config(text=f"{round(current, 1)} s")
    if current < 0:
        Final_score(score.get())
        msg_box = messagebox.askyesno("Koniec", "Koniec czasu\n"
                                      f"Twój wynik: {score.get()}\n"
                                      f"Najlepszy wynik: {max_score_value}\n"
                                      f"Jeszcze raz?")
        if msg_box:
            root.destroy()
            main()
        else:
            root.destroy()

    root.after(100, counter)

def Empty_row():
    global buttons
    for i in (range(len(buttons))):
        if len(buttons[i]) == 0:
            del buttons[i]
            return None


def Re_grid(pos):
    global buttons
    for i in range(pos[1], len(buttons[pos[0]])):
        buttons[pos[0]][i].grid(row=pos[0], column=i)


def Update():
    global buttons
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            posn = (i, j)
            x = int(buttons[i][j].cget("text"))
            buttons[i][j].config(command=lambda x=x, posn=posn:Click(x,posn))

def Set():
    global first, second, firstpos, secondpos
    first = second = firstpos = secondpos = None

def Wrong(pos1, pos2, color):
    global buttons
    try:
        buttons[pos1[0]][pos1[1]].config(bg=color)
        buttons[pos2[0]][pos2[1]].config(bg=color)
        root.after(1500, lambda :Wrong(pos1,pos2, "white"))
    except IndexError:
        return None



def Check(x,y):
    if x == y or x+y == 10:
        return True
    return False




def Correct(x,y):
    global buttons
    if abs(x[0] - y[0]) == 1 and (x[1] == 0 or y[1] == 0) \
               and ((x[1] == len(buttons[x[0]])-1) or (y[1] == len(buttons[y[0]])-1)):
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
        if Correct(firstpos, secondpos) and Check(first, second):
            score.set(score.get() + 1)
            if firstpos[0] == secondpos[0] and firstpos[1] < secondpos[1]:
                buttons[firstpos[0]][firstpos[1]].grid_remove()
                del buttons[firstpos[0]][firstpos[1]]

                buttons[secondpos[0]][secondpos[1]-1].grid_remove()
                del buttons[secondpos[0]][secondpos[1]-1]

                Re_grid(firstpos)

            elif firstpos[0] == secondpos[0] and firstpos[1] > secondpos[1]:
                buttons[firstpos[0]][firstpos[1]-1].grid_remove()
                del buttons[firstpos[0]][firstpos[1]-1]

                buttons[secondpos[0]][secondpos[1]].grid_remove()
                del buttons[secondpos[0]][secondpos[1]]

                Re_grid(secondpos)

            else:

                buttons[firstpos[0]][firstpos[1]].grid_remove()
                del buttons[firstpos[0]][firstpos[1]]
                Re_grid(firstpos)
                Empty_row()

                buttons[secondpos[0]][secondpos[1]].grid_remove()
                del buttons[secondpos[0]][secondpos[1]]
                Re_grid(secondpos)
            Empty_row()
            Update()
            Set()
            return None
        else:
            Wrong(firstpos, secondpos, "red")
            Set()
            return None

def main():
    global first, second, firstpos, secondpos, root, timer, start, score,\
    buttons, frame, max_score_value

    lista = [[randint(1,9) for i in range(10)] for j in range(3)]
    first = second = firstpos = secondpos = None


    root = Tk()
    #root.geometry("300x300")

    score = IntVar(value=0)
    max_score_var = IntVar(value=max_score_value)

    upper_frame = Frame(root)
    time_text = Label(upper_frame, text="Pozostały czas:")
    timer = Label(upper_frame, width=5, height=2)
    message = Label(upper_frame, text="Zdobądź jak najwięcej punktów", height=2)

    lower_frame = Frame(root)
    current_score = Label(lower_frame, text="Twój wynik to:")
    score_label = Label(lower_frame, textvariable=score)
    max_score_label = Label(lower_frame, text="Najlepszy wynik:")
    max_score = Label(lower_frame, textvariable=max_score_var)

    rulesbutton = Button(lower_frame, text="Zasady",
                         command=lambda :messagebox.showinfo("Zasady",
                                                             "+1 - 2 sąsiadujące identyczne\n"
                                                             "+1 - 2 sąsiadujące z sumą 10\n"
                                                             "+1 - pierwszy plus ostatni z sąsiednich rzędów\n identyczne lub z sumą 10"
                                                                                         ))
    newgame = Button(lower_frame, text="Nowa gra", command=Restart)
    fill = Button(lower_frame, text="Uzupełnij", command=Fill)

    frame = Frame(root, bg="black")

    time_text.grid(row=0, column=0)
    timer.grid(row=0, column=0, sticky=E)
    message.grid(row=1, column=0)

    upper_frame.pack()
    frame.pack(fill="both", expand=True)
    lower_frame.pack(fill=X)

    current_score.grid(row=0, column=1, padx=7, sticky=W)
    score_label.grid(row=0, column=1, padx=5, sticky=E)
    max_score_label.grid(row=1, column=1, padx=5, sticky=E)
    max_score.grid(row=1, column=2, sticky=W)
    rulesbutton.grid(row=2, column=0, ipadx=5, padx=5)
    newgame.grid(row=2, column=1, ipadx=5, padx=5)
    fill.grid(row=2, column=2, ipadx=5, padx=5)



    buttons = [[] for _ in lista]
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            current_score = lista[i][j]
            pos = (i, j)
            b = Button(frame, text=current_score, width=35, height=35, activebackground="white",
                       font=Font(size=25), command=lambda x=current_score, pos=pos:Click(x, pos))
            b.grid(row=i, column=j)
            buttons[i].append(b)

    start = time()
    counter()


    root.mainloop()

if __name__ == "__main__":
    max_score_value = 0
    main()
