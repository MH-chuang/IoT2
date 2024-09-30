import tkinter as tk
import speech_recognition as sr
import random
from PIL import Image, ImageTk


def w2():
    frame1.destroy()
    frame2.place(relheight=1, relwidth=1)

def convert():
    speech = sr.Recognizer()
    with sr.Microphone() as source:
        audioData = speech.listen(source)
        try:
            text = speech.recognize_google(audioData, language='zh-tw')
            return text
        except:
            return "try again!!"

def listen(items =[]):
    print("剪刀 石頭 布:")
    b = True
    while b:
        temp = convert()
        print(temp)
        for item in items:
            if temp == item:
                b = False
                return item
                break
        print("say again!!")


def image(canvas, temp):
    canvas.delete("all")
    if temp == "剪刀":
        canvas.create_image(50,50,image = photo1)
    elif temp == "石頭":
        canvas.create_image(50,50,image = photo2)
    else:
        canvas.create_image(50,50,image = photo3)

def setScore(Ai, player, turn, stemp):
    score1.set(Ai)
    score2.set(player)
    t.set(turn)
    string.set(stemp)


def play():
    AIscore = score1.get()
    playerscore = score2.get()
    turn = t.get()
    print("第"+str(turn)+"回合")
    print("分數(AI:"+str(AIscore) +" player:"+str(playerscore)+")")
    AI = random.choice(["剪刀","石頭","布"])
    temp = listen(["剪刀","石頭","布","不","步步","瀑布"])
    image(canvas1, AI)
    image(canvas2, temp)
    if temp in ["剪刀","石頭"]:
        print("Player: " + temp)
    else:
        print("Player: 布")
    print("AI : " + AI)
    stemp =""
    if temp == "剪刀":
        if AI == "剪刀":
            print("平手")
            stemp ="平手"
        elif AI == "石頭":
            print("lose")
            stemp ="輸了"
            AIscore +=1
        else:
            print("win")
            stemp ="贏了"
            playerscore +=1
    elif temp == "石頭":
        if AI == "剪刀":
            print("win")
            stemp ="贏了"
            playerscore +=1
        elif AI == "石頭":
            print("平手")
            stemp ="平手"
        else:
            print("lose")
            stemp ="輸了"
            AIscore +=1
    else:
        if AI == "剪刀":
            print("lose")
            stemp ="輸了"
            AIscore +=1
        elif AI == "石頭":
            print("win")
            stemp ="贏了"
            playerscore +=1
        else:
            print("平手")
            stemp ="平手"
    turn +=1
    setScore(AIscore, playerscore, turn, stemp)

window = tk.Tk()
window.title("game")
window.minsize(width=500, height=500)#畫面大小
window.resizable(width=True, height=True)#畫面可否放大縮小

img1 = Image.open("scissors1.png")
img2 = Image.open("rocks.png")
img3 = Image.open("toilet-paper.png")
img4 = Image.open("question-mark.png")
photo1 = ImageTk.PhotoImage(img1)
photo2 = ImageTk.PhotoImage(img2)
photo3 = ImageTk.PhotoImage(img3)
photo4 = ImageTk.PhotoImage(img4)

frame1 = tk.Frame(window, pady= 200)
frame1.place(relheight=1, relwidth=1)
tk.Label(frame1, text="剪刀石頭布").pack()
exit_button1 = tk.Button(frame1, text="離開", command=window.destroy)
exit_button1.pack(side=tk.BOTTOM)
bUtton1 = tk.Button(frame1, text="開始", command = w2)
bUtton1.pack(side= tk.BOTTOM)


frame2 = tk.Frame(window)
tk.Label(frame2, text="AI").place(relx=0.25, rely=0.2)
tk.Label(frame2, text="Player").place(relx=0.65, rely=0.2)
canvas1 = tk.Canvas(frame2, width = 100, height=100)
canvas1.place(relx= 0.18, rely=0.3)
canvas1.create_image(50,50,image = photo4)
canvas2 = tk.Canvas(frame2, width = 100, height=100,)
canvas2.place(relx= 0.59, rely=0.3)
canvas2.create_image(50,50,image = photo4)

score1 = tk.IntVar()
score2 = tk.IntVar()
t = tk.IntVar()
string = tk.StringVar()   
score1.set(0)
score2.set(0)
t.set(1)
string.set("")
tk.Label(frame2, text="分數").place(relx=0.23, rely=0.05)
tk.Label(frame2, text="回合").place(relx=0.45, rely=0.05)
tk.Label(frame2, text="分數").place(relx=0.66, rely=0.05)   
tk.Label(frame2, textvariable = score1).place(relx=0.25, rely=0.1)
tk.Label(frame2, textvariable = t).place(relx=0.47, rely=0.1)
tk.Label(frame2, textvariable = score2).place(relx=0.68, rely=0.1)
tk.Label(frame2, textvariable = string).place(relx=0.46, rely=0.7)    
bUtton2 = tk.Button(frame2, text="開始", command= play)
bUtton2.place(relx=0.45, rely=0.8)
exit_button2 = tk.Button(frame2, text="離開", command=window.destroy)
exit_button2.place(relx=0.45, rely=0.9)


window.mainloop()

