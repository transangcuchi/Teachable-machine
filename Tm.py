from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from tkinter import font
import tkinter
from tkinter import *
from tkinter.ttk import *
import PIL.Image, PIL.ImageTk
from tkinter import filedialog

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model(".\keras_model.h5", compile=False)

# Load the labels
class_names = open(".\labels.txt", "r").readlines()



def giaodien():
                              
    root=Tk()
    root.title("Nhận Diện")
    root.geometry("800x600")
    root.config(bg="lightcyan")
    button_frame= Frame(root).pack(side=BOTTOM)
    
     
    sign_image = tkinter.Label(root)
      
    def nhandien():
        camera = cv2.VideoCapture(0)       
        while True:
            
            # Grab the webcamera's image.
            ret, image = camera.read()
            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
                       
            # Show the image in a window
            cv2.imshow("Webcam Image", image)
            
            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score  
                      
            textvat="".join(["Vật:",class_name[2:]])
            textdtc="".join(["Độ tin cậy:",str(np.round(confidence_score * 100))[:-2],"%" ])                           
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")            
            # Listen to the keyboard for presses.           
            keyboard_input = cv2.waitKey(1)            
            # 27 is the ASCII for the esc key on your keyboard.          
            if keyboard_input == 27:                                              
                break           
        update_frame(textvat,textdtc)
        cv2.destroyAllWindows()
    
    def anh(file_path):     
        image = PIL.Image.open(fp=file_path,mode="r") 
        image = image.resize((224, 224)) 
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        textvat="".join(["Vật:",class_name[2:]])
        textdtc="".join(["Độ tin cậy:",str(np.round(confidence_score * 100))[:-2],"%" ])                           
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        update_frame(textvat,textdtc)
                       
    def update_frame(textvat,textdtc):
        vat.config(text=textvat)
        dotincay.config(text=textdtc)
             
    def upload_image():
        try:
            file_path = filedialog.askopenfilename()
            uploaded = PIL.Image.open(fp=file_path,mode="r")
            
            uploaded.thumbnail(((root.winfo_width() / 2.25), (root.winfo_height() / 2.25)))
            im = PIL.ImageTk.PhotoImage(uploaded)

            sign_image.config(image=im)
            sign_image.image_names = im
            anh(file_path)
        except:
            pass


    upload = tkinter.Button(button_frame,text="Tải ảnh lên",font=(("Arial"),10,'bold'),bg="#303030",fg="#FFFFFF",command=upload_image )
    upload.pack(padx=10)
    upload.pack(pady=0) 
    upload.pack(side=BOTTOM, pady=50)
    
    sign_image.pack(side=BOTTOM, expand=True)
    
    lable = tkinter.Label(root,text="Ấn Nhận Diện hoặc Tải ảnh lên để bắt đầu",fg="black",bd=0,bg="lightcyan" )
    lable.config(font=("",10))
    lable.pack(pady=0)
    
    lable1 = tkinter.Label(root,text="Ấn ESC để nhận kết quả",fg="black",bd=0,bg="lightcyan" )
    lable1.config(font=("",10))
    lable1.pack(pady=0)
    
    
    ND = tkinter.Button(button_frame,text="Nhận Diện",font=(("Arial"),10,'bold'),bg="#303030",fg="#FFFFFF",command=nhandien )
    ND.pack(pady=10)
    
    vat = tkinter.Label(root,text="",fg="black",bd=0,bg="lightcyan")
    vat.config(font=("",10))
    vat.pack(pady=0)
    vat.pack(padx=0)
    
    dotincay = tkinter.Label(root,text="",fg="black",bd=0,bg="lightcyan")
    dotincay.config(font=("",10))
    dotincay.pack(pady=0)
    dotincay.pack(padx=0)
    
    root.mainloop()

giaodien()
camera = cv2.VideoCapture(0)
