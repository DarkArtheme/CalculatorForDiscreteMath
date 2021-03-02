import sys
import string
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot


import test_form 

def sgn(number):
    if number == 0:
        return 0
    if number > 0:
        return 1
    return -1


class ExampleApp(QtWidgets.QMainWindow, test_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()
        self.a = 0
        self.b = 0
        self.c = 0
        self.a_sgn = 1
        self.b_sgn = 1
        self.c_sgn = 1
        self.a_num_sys = 10
        self.b_num_sys = 10
        self.c_num_sys = 10
        self.digit_to_letter = "0123456789" + string.ascii_uppercase;
        self.letter_to_digit = dict()
        c = 0
        for letter in self.digit_to_letter:
            self.letter_to_digit[letter] = int(c)
            c += 1
        
    
    def initUi(self):
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_1.setText("0")
        self.lineEdit_2.setText("0")
        self.lineEdit_1.textChanged.connect(self.checkInput)
        self.lineEdit_2.textChanged.connect(self.checkInput)
        self.comboBox_1.addItems(list(map(str, (range(2, 37)))))
        self.comboBox_2.addItems(list(map(str, (range(2, 37)))))
        self.comboBox_3.addItems(list(map(str, (range(2, 37)))))
        self.comboBox_1.setCurrentIndex(8)
        self.comboBox_2.setCurrentIndex(8)
        self.comboBox_3.setCurrentIndex(8)
        self.comboBox_1.currentIndexChanged.connect(self.changeSys)
        self.comboBox_2.currentIndexChanged.connect(self.changeSys)
        self.comboBox_3.currentIndexChanged.connect(self.changeSys)
        self.radioButton_1.clicked.connect(self.changeOperation)
        self.radioButton_2.clicked.connect(self.changeOperation)
        self.radioButton_3.clicked.connect(self.changeOperation)
        self.radioButton_4.clicked.connect(self.changeOperation)
        
    
    
    def checkInput(self, num_sys):
        self.sender().setText(self.sender().text().upper())
        input_string = self.sender().text()
        input_string = input_string.upper()
        if self.sender().objectName() == "lineEdit_1":
            num_sys = self.a_num_sys
            if len(input_string) > 0 and input_string[0] == "-":
                input_string = input_string[1::]
                self.a_sgn = -1
            else:
                self.a_sgn = 1
        elif self.sender().objectName() == "lineEdit_2":
            num_sys = self.b_num_sys
            if len(input_string) > 0 and input_string[0] == "-":
                input_string = input_string[1::]
                self.b_sgn = -1
            else:
                self.b_sgn = 1
        elif self.sender().objectName() == "lineEdit_3":
            num_sys = self.c_num_sys
            if len(input_string) > 0 and input_string[0] == "-":
                input_string = input_string[1::]
                self.c_sgn = -1
            else:
                self.c_sgn = 1
        try:
            for digit in input_string:
                if digit not in self.letter_to_digit:
                    raise IOError
                if self.letter_to_digit[digit] >= num_sys:
                    raise IOError
        except Exception:
            print(f"Для данной системы счисления символ '{digit}' не доступен!")
            self.sender().setText(self.sender().text()[:-1])
            return
        if self.sender().objectName() == "lineEdit_1":
            self.a = self.convert_to_int(input_string, num_sys) * self.a_sgn
        elif self.sender().objectName() == "lineEdit_2":
            self.b = self.convert_to_int(input_string, num_sys) * self.b_sgn
        elif self.sender().objectName() == "lineEdit_3":
            self.c = self.convert_to_int(input_string, num_sys) * self.c_sgn
            
    def changeSys(self):
        if self.sender().objectName() == "comboBox_1":
            self.a_num_sys = int(self.sender().currentText())
            self.lineEdit_1.setText(self.convert_to_str(self.a, self.a_num_sys, self.a_sgn))
        elif self.sender().objectName() == "comboBox_2":
            self.b_num_sys = int(self.sender().currentText())
            self.lineEdit_2.setText(self.convert_to_str(self.b, self.b_num_sys, self.b_sgn))
        elif self.sender().objectName() == "comboBox_3":
            self.c_num_sys = int(self.sender().currentText())
            if self.lineEdit_3.text() != "":
                self.lineEdit_3.setText(self.convert_to_str(self.c, self.c_num_sys, self.c_sgn))

    def changeOperation(self):
        if self.sender().objectName() == "radioButton_1":
            self.c = abs(self.a + self.b)
            self.c_sgn = sgn(self.a + self.b)
            self.lineEdit_3.setText(self.convert_to_str(self.c, self.c_num_sys, self.c_sgn))
        elif self.sender().objectName() == "radioButton_2":
            self.c = abs(self.a - self.b)
            self.c_sgn = sgn(self.a - self.b)
            self.lineEdit_3.setText(self.convert_to_str(self.c, self.c_num_sys, self.c_sgn))
        elif self.sender().objectName() == "radioButton_3":
            self.c = abs(self.a * self.b)
            self.c_sgn = sgn(self.a * self.b)
            self.lineEdit_3.setText(self.convert_to_str(self.c, self.c_num_sys, self.c_sgn))
        elif self.sender().objectName() == "radioButton_4":
            if self.b == 0:
                self.lineEdit_3.setText("error")
                win = QMessageBox.warning(self, "Ошибка!", "Делить на 0 нельзя!")
            else:
                self.c = abs(self.a // self.b)
                self.c_sgn = sgn(self.a // self.b)
                self.lineEdit_3.setText(self.convert_to_str(self.c, self.c_num_sys, self.c_sgn))

        
    def convert_to_int(self, num, num_sys):
        res = 0
        c = 0
        for letter in num[::-1]:
            res += int(self.letter_to_digit[letter] * (num_sys ** c))
            c += 1
        
        return res

    def convert_to_str(self, num, num_sys, sign):
        res = []
        num = abs(num)
        if num == 0:
            res = ["0"]
        while num > 0:
            res.append(self.digit_to_letter[num % num_sys])
            num //= num_sys
        if sign == -1:
            res.append("-")
        res.reverse()
        return "".join(res)



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()