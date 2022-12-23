from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import mysql.connector
from keras.utils import load_img,img_to_array
from keras.models import load_model
import matplotlib.pyplot as plt
from tkinter import messagebox
from functools import partial
import cv2
import time
import numpy as np
import os
#

# trích xuất dữ liệu quản lý Mysql
myconn = mysql.connector.connect(host="localhost", user="root",
                                 passwd="quanmanh12", database="study")
cur = myconn.cursor()

#************************************************************************************Window2_test_leaf***********************************************************************
window1 = Tk()
window1.title('Plant Disease')
window1.iconbitmap('D:\AI_project\layout\\icowd.ico')
window1.geometry('1200x700+130+60')
window1.resizable(False, False)
window1.withdraw()
canvas_wd = Canvas(window1, width=1200, height=700)
bg2 = ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\bg2.png'))
canvas_wd.create_image(0, 0, anchor=NW,image=bg2)
canvas_wd.pack()
#frame window test leaf
frame_wd=Frame(window1,width=260, height=260)
frame_wd.place(x=965,y=115)
bg_frame_wd2= ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\bgfr_wd2.png'))
label_frame_wd=Label(frame_wd,image=bg_frame_wd2,bg='green')
label_frame_wd.pack()

file=0#tạo dữ liệu chun
op=0#tạo dữ liệu chun

def openimage():
    global  bg_frame_wd2,file,solution_label,op,pldi
    filename=filedialog.askopenfilename(initialdir='D:/AI_project/test',title='Select A File',filetype=(('jpeg files','*.jpg'),('png files','.png'),('All','*.*')))
    file=str(filename)
    image = Image.open(file)
    resized = image.resize((200, 200), Image.ANTIALIAS)
    print(file)
    bg_frame_wd2=ImageTk.PhotoImage(resized)

    label_frame_wd2.configure( image=bg_frame_wd2)
    solution_label.configure(text='')
    op=1
    pldi=''
    print(pldi)
    rec_frame.place_forget()
    mtl_bt.place_forget()
    mtx_bt.place_forget()
choose_img=ImageTk.PhotoImage(Image.open('D:\\AI_project\\layout\\choose.png'))
bt_choose_wd2= ttk.Button(window1, text='Choose image',command=openimage,image=choose_img)
bt_choose_wd2.place(x=950, y=340)
# nhận diện bệnh cây apple

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model_h5_compare=load_model('D:\AI_project\layout\\compare.h5')
model_h5_leaf=load_model('D:\AI_project\layout\\leaf_apple.h5')
model_h5_fruit=load_model('D:\AI_project\layout\\fruit.h5')
pldi='bien ao'

def check_combare():
    global file
    img = load_img(file, target_size=(150, 150))
    plt.imshow(img)
    img = img_to_array(img)
    img = img.astype('float32')
    img = img / 255
    img = np.expand_dims(img, axis=0)
    result = model_h5_compare.predict(img)
    class_name = ['fruit','leaf']
    combare = int(np.argmax(result, axis=1))
    if class_name[combare]=='fruit':check_fruit()#nếu quả mô hình sẽ nhận diện bằng file h5 của quả
    if class_name[combare]=='leaf':check_leaf()#nếu quả mô hình sẽ nhận diện bằng file h5 của lá

def check_leaf():
    global file,solution_label,pldi

    img = load_img(file, target_size=(150, 150))
    plt.imshow(img)
    img = img_to_array(img)
    img = img.astype('float32')
    img = img / 255
    img = np.expand_dims(img, axis=0)
    result = model_h5_leaf.predict(img)
    class_name = ['Black Rot', 'Cedar apple rust', 'Health', 'Scab']
    result_check_leaf = int(np.argmax(result, axis=1))
    print("Đây là loại:", class_name[result_check_leaf])
    window1.after(1000,
        solution_label.configure(text='Kết quả\nKiểm tra ảnh: Lá cây táo\nĐây là bệnh: {}'.format(class_name[result_check_leaf])))
    pldi=class_name[result_check_leaf]
def check_fruit():
    global file,solution_label,pldi

    img = load_img(file, target_size=(150, 150))
    plt.imshow(img)
    img = img_to_array(img)
    img = img.astype('float32')
    img = img / 255
    img = np.expand_dims(img, axis=0)
    result = model_h5_fruit.predict(img)
    class_name = ['Blotch', 'Cedar apple rust', 'Health', 'Scab']
    result_check_fruit = int(np.argmax(result, axis=1))
    print("Đây là loại:", class_name[result_check_fruit])
    window1.after(1000,
        solution_label.configure(text='Kết quả\nKiểm tra ảnh:Quả táo\nĐây là bệnh: {}'.format(class_name[result_check_fruit])))
    pldi=class_name[result_check_fruit]
check_img=ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\checkicon.png'))
bt_check=ttk.Button(window1,command=check_combare,image=check_img)
bt_check.place(x=1010, y=340)

#in ra ket qua tren window1
solution_label = Label(window1, text='',bg='#f4eade',
                       font=('Helvetica bold', 16,'bold'),
                       anchor=W,
                       justify=LEFT)
solution_label.place(x=90, y=120)
mtlen=True
#giải pháp xử lý bệnh
def muitenlen():
    global mtlen
    mtlen=True
    solution()
def muitenxuong():
    global mtlen
    mtlen=False
    solution()
def solution():
    global solution_label,pldi,rec_label
    if pldi=='Black Rot':
        if mtlen==True:
            txt=open('D:\AI_project\layout\solution\\blackrot.txt','r',encoding='utf-8').read()
        else:txt=open('D:\AI_project\layout\dauhieu\\blackrot.txt','r',encoding='utf-8').read()
    elif pldi=='Blotch':
        if mtlen==True:
            txt=open('D:\AI_project\layout\solution\\blotch.txt','r',encoding='utf-8').read()
        else:txt=open('D:\AI_project\layout\dauhieu\\blotch.txt','r',encoding='utf-8').read()
    elif pldi=='Cedar apple rust':
        if mtlen==True:
            txt=open('D:\AI_project\layout\solution\\cedar.txt','r',encoding='utf-8').read()
        else:txt=open('D:\AI_project\layout\dauhieu\\cedar.txt','r',encoding='utf-8').read()
    elif pldi=='Scab':
        if mtlen==True:
            txt=open('D:\AI_project\layout\solution\\scab.txt','r',encoding='utf-8').read()
        else:txt=open('D:\AI_project\layout\dauhieu\\scab.txt','r',encoding='utf-8').read()
    mtl_bt.place_configure(x=870,y=400)
    mtx_bt.place_configure(x=870,y=480)
    rec_label.configure(text=str(txt))
    rec_frame.place_configure(x=90, y=240)
    rec_frame.configure(text=pldi)
mtl_img=ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\mtlen.png'))
mtl_bt=Button(window1,image=mtl_img,command=muitenlen,bd=0)
mtl_bt.place_forget()
mtx_img=ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\mtxuong.png'))
mtx_bt=Button(window1,image=mtx_img,command=muitenxuong,bd=0)
mtx_bt.place_forget()
solution_img=ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\solutionico.png'))
solution_button=ttk.Button(window1,text='Solution',command=solution,image=solution_img)
solution_button.place(x=1070,y=340)
rec_frame=LabelFrame(window1,text='',font=('Helvetica bold', 12,'bold'),bg='#f4eade',bd=0)
rec_frame.place_forget()
rec_label = Message(rec_frame, text='',bg='#f4eade',
                  font=('Helvetica bold', 12,'bold'),
                  justify=LEFT,width=600)
rec_label.pack()
#chụp hình check
click = PhotoImage(file='D:\AI_project\layout\\bt_click.png')

def camera():
    global label_frame_wd2,op
    rec_frame.place_forget()
    solution_label.configure(text='')
    try:
        cap = cv2.VideoCapture(0)
        print(op)
        op=0

        def video_stream():
            global op
            _, frame = cap.read()
            resize = cv2.resize(frame, (200, 200))
            cv2image = cv2.cvtColor(resize, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label_frame_wd2.imgtk = imgtk
            label_frame_wd2.configure(image=imgtk)
            label_frame_wd2.after(1, video_stream)


            if op == 1:
                cap.release()
                label_frame_wd2.configure(image=bg_frame_wd2)
                op = 0
                button.place_forget()



        video_stream()
        def open_image_cam():
            global bg_frame_wd2, file, solution_label, op

            file = str('D:\\AI_project\\test\\AI_project_0.jpg')
            print(file)
            bg_frame_wd2 = ImageTk.PhotoImage(Image.open(file))

            label_frame_wd2.configure(image=bg_frame_wd2)
            solution_label.configure(text='')
            op = 1


        def click_img():
            global img_counter,label_frame_wd2,solution_label
            path = 'D:/AI_project/test'
            _, frame = cap.read()
            resize = cv2.resize(frame, (200, 200))
            cv2.imwrite(path +'\AI_project_0.jpg', resize)
            filename=path +'\AI_project_0.jpg'
            file=ImageTk.PhotoImage(Image.open(filename))
            label_frame_wd2.configure(image=file)
            solution_label.configure(text='')
            print("image written!")
            msg = messagebox.askyesno('Thông Báo', 'Bạn có muốn chọn ảnh làm ảnh check?')
            if msg==True:
                open_image_cam()
            else:pass
        mtl_bt.place_forget()
        mtx_bt.place_forget()
        button = Button(window1,bd=0, image=click, command=click_img)
        button.place(x=850, y=200)

    except:
        pass
camera_img=ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\cameraicon.png'))
button_camera = ttk.Button(window1, text='camera', command=camera,image=camera_img).place(x=1130, y=340)




#**************************************************************************************************man hinh dang nhap***********************************************************
window2=Toplevel(window1)
window2.title('Plant Disease')
window2.iconbitmap('D:\AI_project\layout\\icowd.ico')
window2.geometry('500x400+540+260')
window2.iconbitmap('D:\AI_project\layout\\icowd.ico')
window2.resizable(False,False)
canvas_wd4 = Canvas(window2, width=500, height=400)
bg_wd4 = ImageTk.PhotoImage(Image.open('D:\AI_project\layout\\bg1.png'))
canvas_wd4.create_image(0, 0, anchor=NW, image=bg_wd4)
canvas_wd4.place(x=0,y=0)
name = Label(window2, text='Tên',bg='#f9f9c5')
name.place(x=90, y=70)
password = Label(window2, text='Mật Khẩu',bg='#f9f9c5')
password.place(x=90, y=110)

txt1 = StringVar()
txt1_entry=Entry(window2,textvariable=txt1,bg='#f9f9c5')
txt1_entry.place(x=193, y=70)
txt2 = StringVar()
txt2_entry=Entry(window2,show='*',textvariable=txt2,bg='#f9f9c5')
txt2_entry.place(x=193, y=110)
STT_fake=0
def log_in(user,passs,event=None):
    global op
    try:
        sql = "SELECT TEN,MATKHAU FROM login"
        cur.execute(sql)
        result_cur = cur.fetchall()
    except:
        myconn.rollback()
    if user.get() == '' or passs.get() == '': messagebox.showinfo('Thông báo', 'Chưa nhập tên hoặc mật khẩu')
    elif (user.get(), passs.get()) not in result_cur:
        messagebox.showwarning('Cảnh báo', 'Sai tên hoặc mật khẩu')
    elif (user.get(), passs.get()) in result_cur:
        op=op+1
        window2.withdraw()
        time.sleep(1)
        window1.deiconify()

value_nm_ps = partial(log_in,txt1,txt2)# nếu dùng lgi(txt1,txt2)thì lệnh lgi sẽ ghi nhận liền của txt1  txt2 và xuất ra 'sai mật khẩu',dùng partial() để tạo ra 1 hàm mới có chức năng của lgi và nhân giá txt nhập vào
#txt bây giờ là cố định ,ban đầu txt là trống ,thay đổi txt thì ra 1 hàm mới dựa vào txt mới điền
Log_in = Button(window2, text='Đăng nhập', bg='#FFFBBF',command=value_nm_ps)
Log_in.place(x=350, y=110)



Log_in.bind('<Return>',value_nm_ps)
window1.mainloop()

