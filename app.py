from tkinter import *
from PIL import Image, ImageTk 
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import simpledialog
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import sqlite3
import cv2 
import face_recognition 
from datetime import datetime, date
import mysql.connector 
import numpy as np  
import os

class CustomDialog(Toplevel):
    def __init__(self, parent, title, prompt): 
        super().__init__(parent)
        self.title(title)

        self.geometry("300x150+500+250")

        self.configure(bg='light grey')  
        Label(self, text="Enter Admin Password", font=("Proxima Nova", 10 , "bold"), fg='black', bg='Light grey').place(x=74, y=20)
        self.password_entry = Entry(self, show='●', width=26)
        self.password_entry.place(x=70, y=60)
        Button(self, text="OK", fg='black',bd=0, activebackground="grey",command=self.ok_pressed).place(x=130,y=100)
        
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def ok_pressed(self):
        admin_password = self.password_entry.get()
        self.destroy()  # Close the dialog
        if admin_password:
            if admin_password == "admin123":
                self.Course()
            else:
                messagebox.showerror("Login","Invalid admin password")
        else:
            messagebox.showinfo("Login","Login cancelled")
    def Course(self):
        self.master.destroy()
        admin_page = Tk()
        admin_page.title("Home")
        admin_bg_path = r"firstPage.png"

        admin_img = ImageTk.PhotoImage(file = admin_bg_path)
        admin_Label = Label (admin_page, image = admin_img)
        admin_Label.grid(row = 0, column = 0)
        admin_Label.image =admin_img

        face_app = Admin(admin_page)
        admin_page.mainloop()
class Admin:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Tabs")

        self.conn = sqlite3.connect('ADMIN')
        self.cursor = self.conn.cursor()

        # Create a style for the buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5, width=15)

        # Configure the style for the navigation frame
        style.configure("TFrame", background="#0B001A",)

        Label(self.master, text='Welcome Admin!', font=('Monteserrat', 20, 'bold'), bg='#0B001A', fg='white').place(x=550, y=50)
        # Navigation Bar
        navv_frame = ttk.Frame(self.master, style="TFrame")
        navv_frame.place(x=200, y=100) 

        dep_button = ttk.Button(navv_frame, text="Department", style="TButton",command=self.show_department_content)
        dep_button.pack(side=tk.LEFT, padx=10)

        subj_button = ttk.Button(navv_frame, text="Subjects", style="TButton", command=self.show_subject_content)
        subj_button.pack(side=tk.LEFT, padx=10)

        faculty_button = ttk.Button(navv_frame, text="Faculty",  style="TButton", command=self.show_faculty_content)
        faculty_button.pack(side=tk.LEFT, padx=10)

        asgn_button = ttk.Button(navv_frame, text="Assign Subjects",  style="TButton", command =self.show_asgnsubj_content)
        asgn_button.pack(side=tk.LEFT, padx=10)
     
        students_button = ttk.Button(navv_frame, text="Students", style="TButton", command= self.show_student_content)
        students_button.pack(side=tk.LEFT, padx=10)

        self.content_frame = ttk.Frame(self.master, style="TFrame", borderwidth=2)
        self.content_frame.place(x=100, y=200, width=900, height=1000)  
    
    def show_department_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        Label(self.content_frame, text='Departments', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=250, y=120)

        self.combobox = ttk.Combobox(self.content_frame, style="TCombobox", font=("Arial",12))
        self.combobox.place(x=450,y=122)
        self.combobox.config(width=35)
        self.combobox['values'] = ('CS & IT', 'HND', 'VCD')

        add_button = Button(self.content_frame, text="Add", command=self.add_content, bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        delete_button = Button(self.content_frame, text="Delete", bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        edit_button = Button(self.content_frame, text="Edit",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        back_button =Button(self.master,text= "Back", command= self.go_back, bg='#0B001A', height=1, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=0, fg='cornsilk4')

        add_button.place(x=450,y=180)
        delete_button.place(x=650, y=180)
        edit_button.place(x=550, y=180)
        back_button.place(x=20,y=10)
    def go_back(self):
        self.master.destroy()

        home_page = Tk()
        home_page.title("Home")
        home_bg_path = r"firstPage.png"
        home_img = ImageTk.PhotoImage(file=home_bg_path)
        home_Label = Label(home_page, image=home_img)
        home_Label.grid(row=0, column=0)
        home_Label.image = home_img

        face_app = Home(home_page)
        home_page.mainloop()
        
    def add_content(self):
        new_content = simpledialog.askstring("Add Content", "Enter department:")
        if new_content:
            current_values = self.combobox['values']
            current_values += (new_content,)
            self.combobox['values'] = current_values

    def delete_content(self):
        selected_content = self.combobox.get()

        if selected_content:
            confirmation = messagebox.askokcancel("Confirmation", f"Are you sure to delete '{selected_content}'?")

            if confirmation:
                current_values = list(self.combobox['values'])
                current_values.remove(selected_content)
                self.combobox['values'] = tuple(current_values)

    def edit_content(self):
        selected_content = self.combobox.get()
        if selected_content:
            new_content = simpledialog.askstring("Edit Content", "Enter new content:", initialvalue=selected_content)
            if new_content:
                current_values = list(self.combobox['values'])
                current_values.remove(selected_content)
                current_values.append(new_content)
                self.combobox['values'] = tuple(current_values)

    def show_subject_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add label with content
        Label(self.content_frame, text='Manage Subjects Information', font=('Arial', 20 , 'bold'), bg='#0B001A', fg='white', bd=0).place(x=350, y=0)
        Label(self.content_frame, text='Department', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=60)
        Label(self.content_frame, text='Year', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=120)
        Label(self.content_frame, text='Semester', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=180)
        Label(self.content_frame, text='Subject', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=240)

        self.department_values = ["CS & IT", "HND", "VCD", "Fashion Designing", "Fine Arts", "Sociology"]  
        self.department_combobox = Combobox(self.content_frame, values=self.department_values)
        self.department_combobox.place(x=500, y=67)

        self.year_values = ["1", "2", "3", "4"]
        self.year_combobox = ttk.Combobox(self.content_frame, values=self.year_values)
        self.year_combobox.place(x=500, y=127)
        self.year_combobox.bind("<<ComboboxSelected>>", self.update_semester_options)

        self.semester_combobox = ttk.Combobox(self.content_frame)
        self.semester_combobox.place(x=500, y=187)

        self.my_combobox=Entry(self.content_frame, width=22)
        self.my_combobox.place(x=500,y=247)

        add_button2 = Button(self.content_frame, text="Add", bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        delete_button2 = Button(self.content_frame, text="Delete",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        edit_button2 = Button(self.content_frame, text="Edit",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')

        add_button2.place(x=350,y=310)
        delete_button2.place(x=550, y=310)
        edit_button2.place(x=450, y=310)

    def update_semester_options(self, event):
        selected_year = self.year_combobox.get()

        if selected_year == "1":
            semester_values = ["1", "2"]
        elif selected_year == "2":
            semester_values = ["3", "4"]
        elif selected_year == "3":
            semester_values = ["5", "6"]
        elif selected_year == "4":
            semester_values = ["7", "8"]
        else:
            semester_values = []

        self.semester_combobox['values'] = semester_values
        self.semester_combobox.set("")  

    def show_faculty_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add label with content
        Label(self.content_frame, text='Manage Faculty Information', font=('Arial', 20 , 'bold'), bg='#0B001A', fg='white', bd=0).place(x=350, y=0)
        Label(self.content_frame, text='First Name', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=60)
        Label(self.content_frame, text='Second Name', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=120)
        Label(self.content_frame, text='Email', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=180)
        Label(self.content_frame, text='Password', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=240)

        self.firstname = Entry(self.content_frame, width =30)
        self.firstname.place(x=500, y=67)

        self.lastname = Entry(self.content_frame, width =30)
        self.lastname.place(x=500, y=127)

        self.email = Entry(self.content_frame, width =30)
        self.email.place(x=500, y=187)

        self.facultypass =Entry(self.content_frame, width =30)
        self.facultypass.place(x=500, y=247)


        add_button3 = Button(self.content_frame, text="Add", bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        delete_button3 = Button(self.content_frame, text="Delete",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        edit_button3 = Button(self.content_frame, text="Edit",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        back_button3 =Button(self.master,text= "Back", command= self.go_back, bg='#0B001A', height=1, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=0, fg='cornsilk4')

        add_button3.place(x=400,y=300)
        delete_button3.place(x=600, y=300)
        edit_button3.place(x=500, y=300)

    def show_asgnsubj_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add label with content
        Label(self.content_frame, text='Assign Subjects', font=('Arial', 20 , 'bold'), bg='#0B001A', fg='white', bd=0).place(x=350, y=0)
        Label(self.content_frame, text='Teacher', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=60)
        Label(self.content_frame, text='Year', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=120)
        Label(self.content_frame, text='Semester', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=180)
        Label(self.content_frame, text='Department', font=('Arial', 20 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=240)

        self.department_values = ["CS & IT"] 
        self.department_combobox = ttk.Combobox(self.content_frame, values=self.department_values)
        self.department_combobox.place(x=500, y=65)

        self.year_values = ["1", "2", "3", "4"]
        self.year_combobox = ttk.Combobox(self.content_frame, values=self.year_values)
        self.year_combobox.place(x=500, y=125)
        self.year_combobox.bind("<<ComboboxSelected>>", self.update_semester_options)

        self.semester_combobox = ttk.Combobox(self.content_frame)
        self.semester_combobox.place(x=500, y=185)

        self.dep_combobox = ttk.Combobox(self.content_frame)
        self.dep_combobox.place(x=500, y=245)


        add_button4 = Button(self.content_frame, text="Add", bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        delete_button4 = Button(self.content_frame, text="Delete",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        edit_button4 = Button(self.content_frame, text="Edit",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
    

        add_button4.place(x=400,y=300)
        delete_button4.place(x=600, y=300)
        edit_button4.place(x=500, y=300)

    def show_student_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        Label(self.content_frame, text="Student Details", font=('Arial', 20 ,'bold'),bg='#0B001A',fg='white', bd=0).place(x=350, y=0)
        Label(self.content_frame, text='First Name',      font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=62)
        Label(self.content_frame, text='Last Name',       font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=102)
        Label(self.content_frame, text='Email',           font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=142)
        Label(self.content_frame, text='Contact',         font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=182)
        Label(self.content_frame, text='Year ',           font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=222)
        Label(self.content_frame, text='Semester',        font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=262)
        Label(self.content_frame, text='Department',      font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=302)
        Label(self.content_frame, text='Course',          font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=300, y=342)

        Entry(self.content_frame, width=17, font=('Arial', 14 )).place(x=450, y=65)
        Entry(self.content_frame,width=17, font=('Arial', 14 )).place(x=450, y=105)
        Entry(self.content_frame, width=17, font=('Arial', 14 )).place(x=450, y=145)
        Entry(self.content_frame, width=17, font=('Arial', 14 )).place(x=450, y=185)
        Combobox(self.content_frame, width=15, font=('Arial', 14 )).place(x=450, y=225)
        Combobox(self.content_frame, width=15, font=('Arial', 14 )).place(x=450, y=265)
        Combobox(self.content_frame, width=15, font=('Arial', 14 )).place(x=450, y=305)
        Combobox(self.content_frame, width=15, font=('Arial', 14 )).place(x=450, y=345)

        add_button5 = Button(self.content_frame, text="Add", bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        delete_button5 = Button(self.content_frame, text="Delete",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')
        edit_button5 = Button(self.content_frame, text="Edit",bg='#0B001A', height=2, width=7,
                                 activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=2, fg='cornsilk4')

        add_button5.place(x=380,y=400)
        delete_button5.place(x=580, y=400)
        edit_button5.place(x=480, y=400)
class LoginPage:
    def __init__(self,master):
        self.master = master
        self.master.title("Attendify")
        self.image_path ='img.jpg'
        bg_img = ImageTk.PhotoImage(file = self.image_path)
        bg_Label = Label (self.master, image = bg_img)
        bg_Label.grid(row = 0, column = 0)
        bg_Label.image =bg_img

        # Labels
        Label(self.master, text='ATTENDIFY', font=('Monteserrat', 35, 'bold'), bg='#0B001A', fg='white').place(x=600, y=150)
        Label(self.master, text='USER LOGIN', font=('Montserrat', 20, 'bold'), bg='#0B001A', fg='white').place(x=645, y=230)
        Label(self.master, text='Username', font=('Proxima Nova', 16), bg='#0B001A', fg='light grey', bd=0).place(x=600, y=300)
        Label(self.master, text='Password', font=('Proxima Nova', 16), bg='#0B001A', fg='light grey', bd=0).place(x=600, y=372)
        Label(self.master, text="Don't have an account?", bg='#0B001A', height=1, width=20, activeforeground='#0B001A',
              bd=0, fg='cornsilk4').place(x=620, y=532)
        Label(self.master, text='Show Password', bg='#0B001A', fg='cornsilk4', bd=0).place(x=623, y=432)

        # Frames
        Frame (self.master , bg = 'Grey', width = 225, height = 1).place(x = 600 , y = 357)
        Frame (self.master , bg = 'Grey' , width = 225 , height = 1).place  (x = 600 , y = 425)
        # Buttons
        Button(self.master, bg='#0B001A', height=1, width=20, bd=0, text='Forget Password?', fg='cornsilk4',
               activebackground='#0B001A').place(x=705, y=430)
        Button(self.master, bg='#0B001A', height=1, width=8, activeforeground='#0B001A', activebackground='#0B001A',
               bd=0.5, fg='cornsilk4', text='Log In', command=self.login).place(x=690, y=480)
        Button(self.master, bg='#0B001A', height=1, width=5, activeforeground='#0B001A', activebackground='#0B001A',
               bd=0, fg='cornsilk4', text='Sign up').place(x=760, y=530)
        Checkbutton(self.master, bg='#0B001A', activebackground='#0B001A', height=1, width=0, bd=0
                    ,command=lambda:self.show(self.password_enter)).place(x=600, y=430)
        
        # User Entries
        self.username_enter = Entry(self.master, font=('San Fransisco', 13), bg='#0B001A', fg='light grey', bd=0,
                                    insertbackground='white')
        self.username_enter.place(x=600, y=334)
        self.password_enter = Entry(self.master, show='●', font=('San Fransisco', 12), bg='#0B001A', fg='light grey',
                                    bd=0, insertbackground='white')
        self.password_enter.place(x=600, y=400)

    def login(self):
        username_enter = self.username_enter.get()
        password_enter = self.password_enter.get()
        if username_enter== "1" and password_enter =="1":
            messagebox.showinfo("Login Successfull","Smart Attendance, Bright Future - Welcome to Attendify ")
            self.open_home_page()
        elif not username_enter or not password_enter:
            messagebox.showerror("Login", "Both username and password are required")
        else:
            messagebox.showerror("Login","Invalid username or password")

    def show(self,password_enter):
        if password_enter.cget ( 'show' ) == '●':
           password_enter.config (show = '')
        else:
           password_enter.config (show = '●')

    def open_home_page(self):
        self.master.destroy()
        home_page = Tk()
        home_page.title("Home")
        home_bg_path = r"firstPage.png"

        home_img = ImageTk.PhotoImage(file = home_bg_path)
        home_Label = Label (home_page, image = home_img)
        home_Label.grid(row = 0, column = 0)
        home_Label.image =home_img

        face_app = Home(home_page)
        home_page.mainloop()
class Home:
    def __init__(self,master):
        self.master = master

        Label(self.master, text='Login As', font=('Monteserrat', 45, 'bold'), bg='#0B001A', fg='white').place(x=490, y=150)
    
        tchr_img_path = r"Teacher.jpg"
        tchr_image = Image.open(tchr_img_path)
        tchr_size = (160, 160)
        resized_tchr_image = tchr_image.resize(tchr_size)
        self.tchr_photo = ImageTk.PhotoImage(resized_tchr_image)

        admin_img_path = r"Admin.jpg"
        Admin_image = Image.open(admin_img_path)
        admin_size = (160, 160)
        resized_admin_image = Admin_image.resize(admin_size)
        self.admin_photo = ImageTk.PhotoImage(resized_admin_image)

        student_img_path = r"Stuudent.jpg"
        student_image = Image.open(student_img_path)
        student_size = (160, 160)
        resized_student_image = student_image.resize(student_size)
        self.student_photo = ImageTk.PhotoImage(resized_student_image)

        Label(self.master, image=self.admin_photo).place(x=270, y=320)
        Label(self.master, image=self.tchr_photo).place(x=570, y=320)
        Label(self.master, image=self.student_photo).place(x=870, y=320)
        Button(self.master, bd=0, fg='cornsilk4', activebackground="#04D9FF", 
               activeforeground="grey",image=self.admin_photo, compound="top",  command=self.admin_login,
               width=self.admin_photo.width(), height=self.admin_photo.height(), bg="#0B001A").place(x=270, y=320)
        Button(self.master, bd=0, fg='cornsilk4',activebackground="#04D9FF", 
               activeforeground="grey",image=self.tchr_photo, compound="top",command= self.markk, width=self.tchr_photo.width(), 
               height=self.tchr_photo.height(), bg="#0B001A").place(x=570, y=320)
        Button(self.master, bd=0, fg='cornsilk4', activebackground="#04D9FF", 
               activeforeground="grey",image=self.student_photo, compound="top",
               width=self.student_photo.width(), height=self.student_photo.height(), bg="#0B001A").place(x=870, y=320)
        
        Label(self.master, text='Admin', font=('Proxima Nova', 16 , "bold"), bg='#0B001A', fg='light grey', bd=0).place(x=310, y=485)
        Label(self.master, text='Teacher', font=('Proxima Nova', 16, "bold"), bg='#0B001A', fg='light grey', bd=0).place(x=600, y=485)
        Label(self.master, text='Student', font=('Proxima Nova', 16, "bold"), bg='#0B001A', fg='light grey', bd=0).place(x=900, y=485)

    def admin_login(self):
        CustomDialog(self.master, "Admin Login", "Enter Admin password:")

    def markk(self):
        self.master.destroy() 
        markk_page = Tk()
        markk_page.title("Capture Moment, Mark Presence")
        markk_page.resizable(False, False) 

        face_app = Markk(markk_page)
        markk_page.mainloop()
class NotificationPanel(tk.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        # self.title("Notification")
        self.geometry("300x50+500+500") 

        # Configure the style for an elegant design
        style = ttk.Style()
        style.configure("Notification.TFrame", background="white", borderwidth=0 , relief="solid")

        # Create a frame with the configured style
        frame = ttk.Frame(self, style="Notification.TFrame")
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Display the notification message
        label = ttk.Label(frame, text=message, font=("Arial", 12), background="white",foreground="black")
        label.pack(expand=True, fill="both")

        # Set a timeout to close the notification after a few seconds
        self.after(5000, self.destroy)
db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234My_sql#',
        database='ATTENDANCEDATA'
    )
cursor = db.cursor()
class Markk:
    
    def __init__(self, master):
        
        self.master = master
        self.master.title("Roll Calls")
        markk_bg_path = r"firstPage.png"

        markk_img = ImageTk.PhotoImage(file=markk_bg_path)
        markk_Label = tk.Label(self.master, image=markk_img)
        markk_Label.grid(row=0, column=0)
        markk_Label.image = markk_img

        tk.Label(self.master, text='Smart Check-Ins', font=('Monteserrat', 35, 'bold'), bg='#0B001A', fg='white').place(x=400, y=10)
        tk.Label(self.master, text="Capture Moment, Mark Presence", font=('Monteserrat', 18), bg='#0B001A', fg='white').place(x=400, y=70)

        # Create a style for the buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5, width=15)

        # Configure the style for the navigation frame
        style.configure("TFrame", background="#0B001A")

        # Navigation Bar
        nav_frame = ttk.Frame(self.master, style="TFrame")
        nav_frame.place(x=330, y=150) 
        # Home button
        home_button = ttk.Button(nav_frame, text="Home", command=self.home_command, style="TButton")
        home_button.pack(side=tk.LEFT, padx=10)


        # view attendence
        markatt_button = ttk.Button(nav_frame, text="View Attendance", command=self.markkatt_image, style="TButton")
        markatt_button.pack(side=tk.LEFT, padx=10)

        # Exit button
        back_button = ttk.Button(nav_frame, text="Exit", command=self.exit_function, style="TButton")
        back_button.pack(side=tk.LEFT, padx=10)

        self.content_frame = ttk.Frame(self.master, style="TFrame", borderwidth=2)
        self.content_frame.place(x=450, y=300, width=900, height=1000)

        Robot_img_path = r"OKY.png"
        Robot_image = Image.open(Robot_img_path)

        # Resize the image
        Robot_size = (399, 411)
        resized_Robot_image = Robot_image.resize(Robot_size)
        self.Robot_photo = ImageTk.PhotoImage(resized_Robot_image)

        # Create a label and add the image to it
        tk.Label(self.master, image=self.Robot_photo, bd=0).place(x=3, y=350)
        self.establish_database()

    def home_command(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        Label(self.content_frame, text="Course", font=('Arial', 16 ),bg='#0B001A',fg='white', bd=0).place(x=0, y=3)
        Label(self.content_frame, text='Semester',      font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=0, y=48)
        Label(self.content_frame, text='Subject',       font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=0, y=93)
        Label(self.content_frame, text='Total Lectures', font=('Arial', 16 ), bg='#0B001A', fg='light grey', bd=0).place(x=0, y=138)

      
        Combobox(self.content_frame, width=10, font=('Arial', 12 )).place(x=150, y=3)
        Combobox(self.content_frame, width=10, font=('Arial', 12 )).place(x=150, y=48)
        Combobox(self.content_frame, width=10, font=('Arial', 12 )).place(x=150, y=93)
        Combobox(self.content_frame, width=10, font=('Arial', 12 )).place(x=150, y=138)
     
        Button(self.content_frame,text= "Mark Attendance", command= self.get_group_photo_path, bg='white', fg= 'black', height=2, width=20,activeforeground='#0B001A', activebackground='#0B001A',
                                 bd=0,).place(x=97, y=183)

    def exit_function(self):
        self.master.destroy()

        home_page = Tk()
        home_page.title("Home")
        home_bg_path = r"firstPage.png"
        home_img = ImageTk.PhotoImage(file=home_bg_path)
        home_Label = Label(home_page, image=home_img)
        home_Label.grid(row=0, column=0)
        home_Label.image = home_img

        face_app = Home(home_page)
        home_page.mainloop()
    def establish_database(self):
        cursor.execute("CREATE DATABASE IF NOT EXISTS ATTENDANCEDATA")
        cursor.execute("USE ATTENDANCEDATA")
        cursor.execute("CREATE TABLE IF NOT EXISTS attendance_table (id INT AUTO_INCREMENT PRIMARY KEY, "
                   "student_name VARCHAR(255), date DATE, time TIME, attendance_status VARCHAR(10))")

    def read_images_and_class_names(path):
        images = []
        class_names = []
        myList = os.listdir(path)
        for cl in myList:
            current_img = cv2.imread(f'{path}/{cl}')
            images.append(current_img)
            class_names.append(os.path.splitext(cl)[0])

        return images, class_names

    path = 'Trained Pictures'
    images, classNames = read_images_and_class_names(path)

    def find_encodings(images):
        encodings_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodings_list.append(encode)
        return encodings_list

    encodings_known = find_encodings(images)
    print("Encoding Complete")

    def match_faces_with_dataset(self,group_image_path, known_encodings, class_names):
    # Load the group photo
        group_image = cv2.imread(group_image_path)
        rgb_group_image = cv2.cvtColor(group_image, cv2.COLOR_BGR2RGB)

        # Find face locations in the group photo
        face_locations = face_recognition.face_locations(rgb_group_image)
        face_encodings = face_recognition.face_encodings(rgb_group_image, face_locations)

        recognized_names = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding with known encodings
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            # Find the index with the minimum face distance (maximum similarity)
            best_match_index = int(np.argmin(face_distances))

            # Use the name from the training dataset
            name = class_names[best_match_index]
            recognized_names.append(name)

            # Draw rectangle and display the name on the group photo
            cv2.rectangle(group_image, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            cv2.putText(group_image, name, (left + 5, bottom + 15), font, 0.5, (255, 255, 255), 1)

    # Display the group photo with rectangles and names
        cv2.imshow('Matched Faces in Group Photo', group_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return recognized_names
    
    def mark_attendance(self,recognized_names):

    # Get today's date and current time
        today_date = date.today()
        current_time = datetime.now().strftime("%H:%M:%S")

    # Mark attendance in the database for recognized faces (excluding "Unknown") with timestamp
        for name in recognized_names:
            if name != "Unknown":
                attendance_status = "Present"
                # Insert attendance record into the database with timestamp
                sql = "INSERT INTO attendance_table (student_name, date, time, attendance_status) VALUES (%s, %s, %s, %s)"
                val = (name, today_date, current_time, attendance_status)
                cursor.execute(sql, val)
    # Commit the changes and close the database connection
        db.commit()

    def get_group_photo_path(self):
        file_path = filedialog.askopenfilename(title="Select Group Photo", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        if file_path:
        # Call the function to match faces in the group photo with the trained dataset
           recognized_faces = self.match_faces_with_dataset(file_path, self.encodings_known, self.classNames)

        # Mark attendance for recognized faces with timestamp
           self.mark_attendance(recognized_faces)
           self.show_notification("Attendance Marked")
        else:
           self.show_notification("Attendance not Marked")
  
    def dummy_function(self): 
        for widget in self.content_frame.winfo_children():
            widget.destroy()  
        self.show_notification("This is a dummy function.")

    def markkatt_image(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.show_notification("This is a dummy function.")

    def show_notification(self, message):
        NotificationPanel(self.master, message)
def main():
    root = Tk()
    loginApp = LoginPage(root)
    root.mainloop()
if __name__ == "__main__":
    main()