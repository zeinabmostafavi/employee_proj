import sys
import os

from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6 import QtGui
from Database import Database
import datetime
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtCore import QFile, QSize
from PySide6.QtUiTools import QUiLoader
from functools import partial
import cv2


def convertCVImage2QtImage(cv_img):
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    height, width, channel = cv_img.shape
    bytesPerLine = 3 * width
    qimg = QImage(cv_img.data, width, height,
                  bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)


class employee(QWidget):
    def __init__(self):
        super(employee, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.show()
        self.ui.btn_insert.clicked.connect(self.show_insertui)
        self.ui.btn_edit.clicked.connect(self.edit_employee)
        # _______________main_________________________________________
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
        edit = edit_show()
        edit()


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

    def camera(self):
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        video = cv2.VideoCapture(0)
        while True:
            validation, frame = video.read()
            if validation is not True:
                break
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            for (x, y, w, h) in faces:
                roi = frame[y:y + h, x:x + w]

            img = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(img)
            self.cameraui.filter1.setIcon(QtGui.QIcon(pix))
            self.cameraui.filter1.setIconSize(QSize(155, 155))

            img2 = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_ARGB6666_Premultiplied)
            pix2 = QtGui.QPixmap.fromImage(img2)
            self.cameraui.filter2.setIcon(QtGui.QIcon(pix2))
            self.cameraui.filter2.setIconSize(QSize(151, 151))

            img3 = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_ARGB4444_Premultiplied)
            pix3 = QtGui.QPixmap.fromImage(img3)
            self.cameraui.filter3.setIcon(QtGui.QIcon(pix3))
            self.cameraui.filter3.setIconSize(QSize(155, 155))

            img4 = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_ARGB8565_Premultiplied)
            pix4 = QtGui.QPixmap.fromImage(img4)
            self.cameraui.filter4.setIcon(QtGui.QIcon(pix4))
            self.cameraui.filter4.setIconSize(QSize(155, 155))

            img5 = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_Grayscale16)
            pix5 = QtGui.QPixmap.fromImage(img5)
            self.cameraui.filter5.setIcon(QtGui.QIcon(pix5))
            self.cameraui.filter5.setIconSize(QSize(155, 155))

            img6 = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_ARGB8555_Premultiplied)
            pix6 = QtGui.QPixmap.fromImage(img6)
            self.cameraui.filter6.setIcon(QtGui.QIcon(pix6))
            self.cameraui.filter6.setIconSize(QSize(155, 155))

            img7 = QtGui.QImage(
                frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGBA8888)
            pix7 = QtGui.QPixmap.fromImage(img7)
            self.cameraui.filter7.setIcon(QtGui.QIcon(pix7))
            self.cameraui.filter7.setIconSize(QSize(155, 155))

            cv2.waitKey(30)

   
class edit_show(QWidget):
    def __init__(self):
        super(edit_show, self).__init__()

        loader = QUiLoader()
        self.editui = loader.load("form_edit.ui")
        self.editui.show()
        # self.ui.btn_edit.clicked.connect(self.edit_employee)


if __name__ == "__main__":
    app = QApplication([])
    window = employee()
    sys.exit(app.exec())
