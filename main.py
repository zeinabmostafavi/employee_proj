import sys
import os

from PySide6.QtGui import QIcon
from Database import Database
import datetime
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtCore import QFile, QSize
from PySide6.QtUiTools import QUiLoader
from functools import partial
import cv2
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
my_video = cv2.VideoCapture(0)


class employee(QWidget):
    def __init__(self):
        super(employee, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.cameraui = loader.load("camera.ui")
        self.ui.show()
        self.ui.btn_insert.clicked.connect(self.show_insertui)
        self.ui.btn_edit.clicked.connect(self.edit_employee)
        
        self.show_employee()

    def show_employee(self):
        showemps = Database.select()
        for i, showemp in enumerate(showemps):
            label = QLabel()
            label.setText(showemp[1] + " " + showemp[2] + "  " +
                          showemp[3]+"  " + showemp[4] + "  ")
            self.ui.gl_emp.addWidget(label, i, 1)
            label.setStyleSheet('font-family: B YEKAN, Helvetica, sans-serif')

            btn = QPushButton()
            btn.setIcon(QIcon(showemp[5]))
            btn.setIconSize(QSize(100, 100))
            btn.setShortcut('Ctrl+d')
            btn.setStyleSheet(
                'max-width: 40px; min-height: 40px; color: white; border: 0px; border-radius: 5px;')
            #btn.clicked.connect(partial(self.delete, showemps[0], btn, label))
            self.ui.gl_emp.addWidget(btn, i, 0)

    def show_insertui(self):
        self.ui.close()
        insert = insert_ui()
        insert()

    def edit_employee(self):
        pass

# ________________________insert_____________________


class insert_ui(QWidget):
    def __init__(self):
        super(insert_ui, self).__init__()

        loader = QUiLoader()
        self.insertui = loader.load("form_insert.ui")
        self.insertui.show()
        self.insertui.btn_add.clicked.connect(self.add_employee)
        self.insertui.btn_camera.clicked.connect(self.open_camera)

    def open_camera(self):
        camera_ui = camera_show()
        camera_ui.camera()

    def add_employee(self):
        name = self.insertui.ln_name.text()
        familly = self.insertui.ln_familly.text()
        code = self.insertui.ln_code.text()
        birthday = self.insertui.ln_birthday.text()
        img = self.insertui.ln_img.text()
        emp = employee()

        showemps = Database.select()

        if name != "" and familly != "" and code != "" and birthday != "" and img != "":
            response = Database.insert(name, familly, code, birthday, img)
            if response:
                label = QLabel()
                label.setText(name + "  " + familly + "  " +
                              code + "  " + birthday + "  ")
                emp.ui.gl_emp.addWidget(label, len(showemps)+1, 1)
                btn = QPushButton()
                btn.setIcon(QIcon(img))
                btn.setIconSize(QSize(100, 100))
                btn.setShortcut('Ctrl+n')
                btn.setStyleSheet(
                    'max-width: 40px; min-height: 40px; color: white; border: 0px; border-radius: 5px;')
                emp.ui.gl_emp.addWidget(btn, len(showemps)+1, 0)
                insert_ui.clos()
                emp.close()
                emp.show_employee()

                msg_box = QMessageBox()
                msg_box.setText("Your message sent successfully!")

                # self.ui.txt_name.setText("")
                # self.ui.txt_message.setText("")

            else:
                msg_box = QMessageBox()
                msg_box.setText("Database error!")
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Error: feilds are empty!")
            msg_box.exec_()


# ____________________camera_ui_________________________________
class camera_show(QWidget):
    def __init__(self):
        super(camera_show, self).__init__()

        loader = QUiLoader()
        self.cameraui = loader.load("camera.ui")
        self.cameraui.show()
        # self.ui.btn_insert.clicked.connect(self.show_insertui)
        # self.ui.btn_edit.clicked.connect(self.edit_employee)
        # _______________filter_________________________________________

    def camera(self):
        self.cameraui.show()
        while True:
            valdation, frame = my_video.read()
            if valdation is not True:
                break
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(frame_gray, 1.3)
            for i, face in enumerate(faces):
                x, y, w, h = face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
            image_frame = cv2.resize(frame, (h // 3, w // 3))
            cv2.imshow('output', frame)
            # self.cameraui.filter1.setIcon(QIcon('5.jpg'))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    app = QApplication([])
    window = employee()
    sys.exit(app.exec())
