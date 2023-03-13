from keras.models import load_model  
import cv2  
import numpy 
from tkinter import font
import tkinter
from tkinter import *
from tkinter.ttk import *
import PIL.Image, PIL.ImageTk
from tkinter import filedialog

numpy.set_printoptions(suppress=True)
model = load_model(".\keras_model_nuocngot.h5", compile=False)
Names = open(".\labels.txt", "r").readlines()

def giaodienNhanDien():
                              
    gd=Tk()
    gd.title("Nhận Diện Nước Ngọt")
    gd.geometry("750x550")
    gd.config(bg="white")
    button_frame= Frame(gd).pack(side=BOTTOM)   
    camera = cv2.VideoCapture(0)
    vitrianh = tkinter.Label(gd)
      
    def nhandiennuoc():
               
        while True:
            ret,image = camera.read()
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)                      
            cv2.imshow("Máy ảnh", image)
            image = numpy.asarray(image, dtype=numpy.float32).reshape(1, 224, 224, 3)
            image = (image / 127.5) - 1
            pred = model.predict(image)
            index = numpy.argmax(pred)
            class_name = Names[index]
            confidence_score = pred[0][index]                     
            kq="".join(["Loại Nước:",class_name[2:]])
            tl="".join(["Tỉ lệ chính xác:",str(numpy.round(confidence_score * 100))[:-2],"%" ])                           
            print("Loại Nước::", class_name[2:], end="")
            print("Tỉ lệ chính xác:", str(numpy.round(confidence_score * 100))[:-2], "%")            
            # Listen to the keyboard for presses.           
            Thoat = cv2.waitKey(1)            
            # 27 is the ASCII for the esc key on your keyboard.          
            if Thoat == 27:                                              
                break           
        xuatkq(kq,tl)
        cv2.destroyAllWindows()
    
    def taianhlen(file_path):
        try:     
            image = PIL.Image.open(fp=file_path,mode="r") 
            image = image.resize((224, 224)) 
            image = numpy.asarray(image, dtype=numpy.float32).reshape(1, 224, 224, 3)
            image = (image / 127.5) - 1
            pred = model.predict(image)
            index = numpy.argmax(pred)
            class_name = Names[index]
            confidence_score = pred[0][index]
            kq="".join(["Loại Nước:",class_name[2:]])
            tl="".join(["Tỉ lệ chính xác:",str(numpy.round(confidence_score * 100))[:-2],"%" ])
            input.config(fg="black")
            output.config(fg="black")                                      
            print("Loại Nước:", class_name[2:], end="")
            print("Tỉ lệ chính xác:", str(numpy.round(confidence_score * 100))[:-2], "%")
            xuatkq(kq,tl)
        except:
            kq="Lỗi file ảnh"
            tl="Ảnh sử dụng nên là .jfif hoặc là .jpg"                          
            print("Lỗi file ảnh")
            input.config(fg="red")
            output.config(fg="red")           
            xuatkq(kq,tl)
            pass
                       
    def xuatkq(kq,tl):
        input.config(text=kq)
        output.config(text=tl)
             
    def chonanh():
        try:
            file_path = filedialog.askopenfilename()
            uploaded = PIL.Image.open(fp=file_path,mode="r")           
            uploaded.thumbnail(((gd.winfo_width() / 2.25), (gd.winfo_height() / 2.25)))
            im = PIL.ImageTk.PhotoImage(uploaded)
            vitrianh.config(image=im)
            vitrianh.image_names = im
            taianhlen(file_path)
        except:
            pass
    
    a = tkinter.Label(gd,text="Chọn Camera hoặc Tải ảnh lên để bắt đầu",fg="black",bd=0,bg="white" )
    a.config(font=("",10))
    a.pack(pady=0)
    
    b = tkinter.Label(gd,text="Ấn ESC để nhận kết quả",fg="black",bd=0,bg="white" )
    b.config(font=("",10))
    b.pack(pady=0)
    
    upload = tkinter.Button(button_frame,text="Tải ảnh lên",font=(("Times New Roman "),10,'bold'),bg="Yellow",fg="black",command=chonanh )
    upload.pack(padx=10)
    upload.pack( pady=10)
    
    vitrianh.pack(side=BOTTOM,pady=10 )
    
    Camera = tkinter.Button(button_frame,text="Camera",font=(("Times New Roman"),10,'bold'),bg="yellow",fg="black",command=nhandiennuoc )
    Camera.pack(pady=10)
    
    input = tkinter.Label(gd,text="",fg="black",bd=0,bg="white")
    input.config(font=("",10))
    input.pack(pady=0,side=BOTTOM)
    input.pack(padx=0)
    
    output = tkinter.Label(gd,text="",fg="black",bd=0,bg="white")
    output.config(font=("",10))
    output.pack(pady=0,side=BOTTOM)
    output.pack(padx=0)
    
    gd.mainloop()

giaodienNhanDien()
cv2.destroyAllWindows()
