from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import numpy as np
import cv2
import tkinter as tk
from PIL import ImageTk,Image
import os
import os.path
from os import path
i=0
if not path.exists("Withoutmask"):
    os.mkdir('Withoutmask')
with_mask = np.load('with_mask.npy', allow_pickle=True)
without_mask = np.load('without_mask.npy', allow_pickle=True)

with_mask = with_mask.reshape(with_mask.shape[0], 50 * 50 * 3)
without_mask = without_mask.reshape(without_mask.shape[0], 50 * 50 * 3)

X = np.r_[with_mask, without_mask]

labels = np.zeros(X.shape[0])
labels[with_mask.shape[0]:] = 1.0
names = {0: 'Mask', 1: 'No Mask'}
color = {0: (255, 255, 0), 1: (0, 255, 255)}

x_train, x_test, y_train, y_test = train_test_split(X, labels, test_size=0.25)

pca = PCA(n_components=3)
X_train = pca.fit_transform(x_train)

x_train, x_test, y_train, y_test = train_test_split(X, labels, test_size=0.25)

svm = SVC()
svm.fit(x_train, y_train)

y_pred = svm.predict(x_test)
print(accuracy_score(y_test,y_pred))
cam=0
def window1():
    mycolor2='#384ca2'
    mycolor3='#3E71DE'
    mycolor='#2c2f33'
    mycolor4='#66ba33'
    root = tk.Tk()  
    root.wm_title("Home")
    canvas = tk.Canvas(root,bg=mycolor, width = 600, height = 600)  
    canvas.pack()  
    img = ImageTk.PhotoImage(Image.open("fmask1.png"))  
    canvas.create_image(300,150,image=img) 

    tk.Label(root,text="FACE MASK DETECTION",font=("Arial",22),bg=mycolor,fg="white").place(x=120,y=300)

    tk.Label(root,text="Select Camera",font=("Arial",14),bg=mycolor,fg="white").place(x=100,y=400)

    def about():
        def windoa():
            aboutwin.destroy()
            window1()
        root.destroy()
        aboutwin=tk.Tk()
        aboutwin.wm_title("About")
        aboutwin.config(bg=mycolor)
        canvas = tk.Canvas(aboutwin, width = 750, height = 650,bg=mycolor)
        canvas.pack()
        imag = ImageTk.PhotoImage(Image.open("logopce1.png"))
        canvas.create_image(375,150,image=imag)  
        tk.Label(aboutwin,text = "Project Members",font=("Arial",22,"bold"),bg=mycolor,fg='white').place(x=250,y=280)
        tk.Label(aboutwin,text = "Member 1",font=("Arial",18),bg=mycolor,fg='white').place(x = 260,y = 350)
        tk.Label(aboutwin,text = "Member 2",font=("Arial",18),bg=mycolor,fg='white').place(x = 260,y = 380)
        tk.Label(aboutwin,text = "Member 3",font=("Arial",18),bg=mycolor,fg='white').place(x = 260,y = 410)
        tk.Label(aboutwin,text = "Member 4",font=("Arial",18),bg=mycolor,fg='white').place(x = 260,y = 440) 
        tk.Label(aboutwin,text = "Face Mask Detection",font=("Arial",18),bg=mycolor,fg='white').place(x = 150,y = 490)
        butbk1=tk.Button(aboutwin,text="BACK",command=windoa,bg=mycolor3,fg='white').place(x=360,y=560)
        aboutwin.mainloop()

    tk.Button( root , text = "About" , command = about, bg=mycolor3,fg="white").place(x=380,y=480)

    def show():
        def windo():
            window.destroy()
            window1()
        global cam
        text=clicked.get()
        if(text=="Camera1"):
            cam=0
        elif(text=="Camera2"):
            cam=1
        else:
            cam=2
        
        root.destroy()

        window = tk.Tk()  #Makes main window
        window.wm_title("Face Mask Detection")
        window.config(bg=mycolor)

        imageFrame = tk.Frame(window, width=600, height=500)
        imageFrame.grid(row=0, column=0, padx=10, pady=2)


        lmain = tk.Label(imageFrame)
        lmain.grid(row=0, column=0)

        names = {0 : 'Mask', 1 : 'No Mask'}
        haar_data = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        capture = cv2.VideoCapture(cam)
        font = cv2.FONT_HERSHEY_TRIPLEX

       
        def show_frame():
            global i
            flag, img = capture.read() 
            if flag:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = haar_data.detectMultiScale(gray,1.1,4)
                for x,y,w,h in faces:
                    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 4)
                    face = img[y:y+h, x:x+w, :]
                    face = cv2.resize(face, (50,50))
                    face=face.reshape(1,-1)
                    pred = svm.predict(face)
                    n= names[int(pred)]
                    if pred == 0:
                        cv2.putText(img, n, (x,y), font, 1, (0,128,0), 2)
                    else:
                        i+=1
                        cv2.putText(img, n, (x,y), font, 1, (0,0,128), 2)
                        if(i%10==0):
                            cv2.imwrite(f'Withoutmask\img_{i}.png',img)
                            print("Saved")
                    print(n)
                backtorgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                img1 = Image.fromarray(backtorgb)
                imgtk = ImageTk.PhotoImage(image=img1)
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
                lmain.after(10, show_frame) 

        butbk=tk.Button(window,text="BACK",command=windo,bg=mycolor2,fg='white')
        butbk.grid(row=601,column=0,padx=50,pady=10)


        show_frame()
        window.mainloop()
        capture.release()
        cv2.destroyAllWindows()


    options=[
        "Camera1",
        "Camera2",
        "Camera3"
    ]
    clicked = tk.StringVar(root)
    clicked.set( "Camera1" )
    drop = tk.OptionMenu( root , clicked , *options)
    drop.config(bg=mycolor3,fg="white")
    drop["highlightthickness"]=0
    drop["menu"].config(bg=mycolor3,fg="white")
    drop.place(x=250,y=400)

    button = tk.Button( root , text = "Open " , command = show,bg=mycolor3,fg="white" ).place(x=380,y=400)
    root.mainloop() 
window1()
