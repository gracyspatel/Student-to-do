import kivy
kivy.require('1.9.0') 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivymd.uix.button import MDRaisedButton,MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem,ThreeLineListItem,IRightBodyTouch, ThreeLineAvatarIconListItem
import mysql.connector
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDTimePicker,MDDatePicker
from kivy.properties import StringProperty
from kivymd.icon_definitions import md_icons
kvlang = '''
<ScreenManagement>:
    LoginScreen:
    TaskScreen:

<LoginScreen>:
    name:'Loginsrc'
    id:mdsrc
    MDIconButton:
        id:icon
        icon:"account-circle"
        pos_hint:{"center_x":.5,"center_y":.8}
        user_font_size:"60sp"
        theme_text_color:"Custom"
        text_color:0,0,0,1
    MDTextField:
        width:300
        id:username
        hint_text:"Enter Your Email"
        size_hint_x:.8
        pos_hint:{"center_x":.5,"center_y":.46}
        current_hint_text_color:0,0,0,1
        color_mode:"custom"
        line_color_focus:0,0,0,1
    MDTextField:
        width:300
        id:password
        hint_text:"Enter Your Password"
        size_hint_x:.8
        pos_hint:{"center_x":.5,"center_y":.34}
        password: True
        current_hint_text_color:0,0,0,1
        color_mode:"custom"
        line_color_focus:0,0,0,1
        icon_right: 'key-variant'
    MDRaisedButton:
        id:login_btn
        text:"Login"
        pos_hint: {"center_x":0.5,"center_y":.2}
        size_hint_x:.5
        md_bg_color:0,0,0,1
        on_press: root.showdata()
    MDLabel:
        id:label
        text: f"[font=Arial]Taskiva Admin Login[/font]"
        markup: True
        pos_hint:{"center_y":.7}
        halign:"center"
        theme_text_color:"Custom"
        text_color:0,0,0,1
        font_style:"H5"
<AssignedTaskScreen>:
    name:"assignedscr"
    id:screen4
    MDLabel:
        text: "Assigned Tasks"
        halign:"center"
        font_style:'H5'
        pos_hint: {"top":1.43}
<CompletedTaskScreen>:
    name:"assignedscr"
    id:screen4
    MDLabel:
        text: "Completed Tasks"
        halign:"center"
        font_style:'H5'
        pos_hint: {"top":1.43}
<AddScreen>:
    name:"assignedscr"
    id:screen4
    MDLabel:
        text: "Add Tasks"
        halign:"center"
        font_style:'H5'
        pos_hint: {"top":1.43}
    BoxLayout:
        padding: "40dp"
        MDProgressBar:
            pos_hint: {"top":1.45}
            value: 100
    MDLabel:
        text: f"[font=Arial][b]  Task Name[/b][/font]"
        markup: True
        font_style:'Subtitle1'
        pos_hint: {"top":1.30,"center_x":.57}
    MDLabel:
        text: f"[font=Arial][b]  Task Description[/b][/font]"
        markup: True
        font_style:'Subtitle1'
        pos_hint: {"top":1.10,"center_x":.57}
    MDTextField:
        width:300
        id:taskname
        hint_text:"Enter Assignment Name...."
        size_hint_x:.8
        pos_hint:{"center_x":.5,"center_y":.70}
        current_hint_text_color:0,0,0,1
        color_mode:"custom"
    MDTextField:
        width:300
        id:taskdes
        hint_text:"Enter Details...."
        size_hint_x:.8
        pos_hint:{"center_x":.5,"center_y":.50}
        current_hint_text_color:0,0,0,1
        color_mode:"custom"
    MDRaisedButton:
        text: "Select Time"
        pos_hint: {'center_x': .56, 'center_y': .35}
        on_press: root.show_time_picker()
    MDRaisedButton:
        text: "Select Date"
        pos_hint: {'center_x': .16, 'center_y': .35}
        on_press: root.show_date_picker()
    MDRaisedButton:
        text: "SUBMIT"
        pos_hint: {'center_x': .16, 'center_y': .15}
        on_press: root.submitbtn()
<TaskScreen>:
    name: 'TaskScreen'
    id: screen6
    BoxLayout:
        orientation:'vertical'

        MDToolbar:
            title:"Taskiva Admin"
            elevation: 10
            pos_hint:{"top":1}
            md_bg_color: .2, .2, .2, 1
            specific_text_color: 1, 1, 1, 1

        MDBottomNavigation:
            panel_color: .2, .2, .2, 1

            MDBottomNavigationItem:
                name: 'ass_task'
                text: 'Tasks'
                on_tab_press: root.assignedlist()
                ScrollView:
                    pos_hint:{"top":0.9}
                    MDList:
                        id: assigned
                AssignedTaskScreen:

            MDBottomNavigationItem:
                name: 'comp_task'
                text: 'Completed Tasks'
                on_tab_press: root.completedlist()
                ScrollView:
                    pos_hint:{"top":0.9}
                    MDList:
                        id: completed
                CompletedTaskScreen:

            MDBottomNavigationItem:
                name: 'add_task'
                text: 'Add Task'
                AddScreen:
    MDRaisedButton:
        text: "Logout"
        md_bg_color: 0, 0, 1, 1
        on_press: app.root.current = 'Loginsrc'
        pos_hint: {"center_x": .9, "center_y": .94}
<ListItemWithCheckbox>:
    IconLeftWidget:
        icon: root.icon
    RightCheckbox:
        on_press:root.deletetask()
'''
def login_s():
    db_login = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1234",
        database = 'S_assign'
        )
    c_conn = db_login.cursor()
    c_conn.execute("SELECT * from login_data")
    S_id = c_conn.fetchall()
    return S_id
def addcompTask(ttname,tdes,tdate,ttime):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="s_assign"
        )
    mycursor = mydb.cursor()
    sql = "INSERT INTO ca_tasks (ca_name, ca_des,ca_date,cat_time) VALUES (%s, %s,%s,%s)"
    val = (ttname,tdes,tdate,ttime)
    mycursor.execute(sql, val)
    mydb.commit()
    print("added")
class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")
    def deletetask(self):
        print(self.text[4:])
        #print(len(self.text[4:]))
        #if(self.text[4:]=='Task 4'):
        #print(True)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="s_assign"
        )
        mycursor = mydb.cursor()
        #mycursor.execute("DELETE FROM s_tasks WHERE s_name='task1'")
        sql= "SELECT * FROM a_tasks WHERE t_name=%s"
        adr=(self.text[4:],)
        mycursor.execute(sql,adr)
        myresult = mycursor.fetchall()
        for x in myresult:
            ttname=x[0]
            tdes=x[1]
            tdate=x[2]
            ttime=x[3]
        #print(ttname,tdes,tdate,ttime)
        addcompTask(ttname,tdes,tdate,ttime)
        sql= "DELETE FROM a_tasks WHERE t_name=%s"
        adr=(self.text[4:],)
        mycursor.execute(sql,adr)
        mydb.commit()
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
class ScreenManagement(ScreenManager):
    pass

class ContentNavigationDrawer(BoxLayout):
    pass

class LoginScreen(Screen):
    def switch(self):
        #here you can insert any python logic you like 
        self.parent.current = 'TaskScreen'
    def closedialog(self,obj):
        self.dia.dismiss()
    def showdata(self):
        S_data=login_s()
        for x in S_data:
            s_id=x[0]
            s_pass=x[1]
        t=""
        a=0
        print(self.ids.password.text)
        if(self.ids.username.text=="" and self.ids.password.text==""):
            t = "Username and Password required"
            a=1
        elif(self.ids.username.text==""):
            t = "Username required"
            a=1
        elif(self.ids.password.text==""):
            t = "Password required"
            a=1
        if(a==1):
            bt = MDRectangleFlatButton(text="x",on_release=self.closedialog)
            self.dia=MDDialog(text=t,size_hint=(0.5,1),buttons=[bt])
            self.dia.open()	
        else:
            #pass check
            if(self.ids.username.text==s_id and self.ids.password.text==s_pass):
                self.parent.current = 'TaskScreen'
                return
            elif(self.ids.username.text!=s_id):
                self.d=MDDialog(text="Incorrect Username",size_hint=(0.5,1))
                self.d.open()
            else:
                self.d=MDDialog(text="Incorrect Password",size_hint=(0.5,1))
                self.d.open()
save=[]
save2=[]
class TaskScreen(Screen):
    def assignedlist(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="s_assign"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM a_tasks")
        myresult = mycursor.fetchall()
        c=1
        icons = list(md_icons.keys())
        for x in myresult:
            if(x[0] not in save):
                save.append(x[0])
                self.ids.assigned.add_widget(
                    ListItemWithCheckbox(text=f"{c} : {x[0]}",secondary_text=f"Assigned Task",tertiary_text=f"Deadline :{x[2]}",icon=icons[47],on_release=MDDialog(text=f"Task Name :{x[0]} /n Task Descreption :{x[1]}/n Deadline Date:{x[2]} /n Deadline Time: {x[3]}").open)
                    )
                c=c+1

    def completedlist(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="s_assign"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM ca_tasks")
        myresult = mycursor.fetchall()
        c=1
        for i in myresult:
            if(i[0] not in save2):
                save2.append(i[0])
                self.ids.completed.add_widget(
                    ThreeLineListItem(text=f"{c} : {i[0]}",secondary_text=f"Completed Task",tertiary_text=f"{i[1]}")
                    )
                c+=1

class CompletedTaskScreen(Screen):
    pass
class AssignedTaskScreen(Screen):
    pass
class AddScreen(Screen):
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    def get_time(self, instance1, time):
        global t
        print(time)
        t=time
    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.got_date)
        date_dialog.open()
    def got_date(self,the_date):
        global dd
        global mm
        global yy
        print(the_date.day)
        dd=the_date.day
        print(the_date.month)
        mm=the_date.month
        print(the_date.year)
        yy=the_date.year
    def submitbtn(self):
        print("Submited")
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1234",
        database = 'S_assign'
        )
        mycursor = mydb.cursor()
        staskval=self.ids.taskname.text
        stdesval=self.ids.taskdes.text
        print(staskval)
        print(stdesval)
        print(dd)
        print(mm)
        print(yy)
        stdateval=str(yy)+'-'+str(mm)+'-'+str(dd)
        print(stdateval)
        print(t)
        sttimeval=t
        sql = "INSERT INTO a_tasks (t_name, t_des,t_date,t_time) VALUES (%s, %s,%s,%s)"
        val = (staskval, stdesval,stdateval,sttimeval)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

class MyApp(MDApp):
    def build(self):
        Builder.load_string(kvlang)
        return ScreenManagement()

if __name__ == '__main__':
    MyApp().run()