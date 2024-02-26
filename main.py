from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

from ui.main_window import Ui_MainWindow

import sys
import math
import numpy as np
from random import randint
from collections import defaultdict
from functools import reduce
from operator import mul
import shutil
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

class Cfile():
    def open(self):#открытие файла
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()","", "All Files (*);;Text Files (*.txt)")
        if check:
            self.file_open = file
            print(self.file_open)

            info = QFileInfo(self.file_open)
            name = info.fileName()
            return name

    def close(self):#закрытие файла
        file_name, check = QFileDialog.getSaveFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*);;Text Files (*.txt)")
        if check:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.text_backup)

            msg = QtWidgets.QMessageBox.information(
                self,
                'Успех',
                f'Введенные данные записаны в файл {file_name}.'
            )

    # def seek(self):#поиск

    def read(self):#чтение файла
        filename = self.file_open

        if filename[0]:
            f = open(filename, 'r')

            with f:
                data = f.read()
                self.ui.textEdit.setText(data)

    def write(self):#запись в файл
        self.text_backup = self.ui.textEdit.toPlainText()
        print(self.text_backup)

    def getPosition(self):#получить путь файла
        self.ui.label_51.setText(f"путь файла - {self.file_open}")

    def getLenght(self):#получить размер файла
        info = QFileInfo(self.file_open)
        size = info.size()

        self.ui.label_51.setText(f"размер файла - {size} байт")

class CMyDataFile(Cfile):
    def __init__(self, file_name, file_type):
        self.myData
        #self.header

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if(section == 0):
                return "x"
            elif (section == 1):
                return "ln(x+1)"
            elif (section == 2):
                return "результат сумма"
            elif (section == 3):
                return "кол-во членов суммы"
            # return super().headerData(section, orientation, role)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

class mywindow(QtWidgets.QMainWindow):

    fire_count = 0

    def set_header_lab_4(self, model):
        model.setHeaderData(1, QtCore.Qt.Horizontal, "Фамилия И.О.")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "должность")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "год поступления")
        model.setHeaderData(4, QtCore.Qt.Horizontal, "зарплата")

    def connect(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("workers.sqlite")
        self.con.open()

        query = QSqlQuery(self.con)
        query.exec("create table if not exists soldat (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, fio varchar(255), post varchar(255), year INTEGER, salary INTEGER)")

        self.soldat_model = QSqlQueryModel()
        self.soldat_model.setQuery("select * from soldat")

        self.set_header_lab_4(self.soldat_model)

        self.ui.tableView_2.setModel(self.soldat_model)
        self.ui.tableView_2.setColumnHidden(0, True)

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect()
        self.lab_10_classs = CMyDataFile

        self.ui.label_6.setPixmap(QtGui.QPixmap("ui/z1_z2.jpg"))
        self.ui.label_14.setPixmap(QtGui.QPixmap("ui/l_2_2.jpg"))

        self.ui.pushButton.clicked.connect(self.lab_1)
        self.ui.pushButton_2.clicked.connect(self.lab_2_1)
        self.ui.pushButton_3.clicked.connect(self.lab_2_2)
        self.ui.pushButton_4.clicked.connect(self.lab_3_1)
        self.ui.pushButton_5.clicked.connect(self.lab_3_2)
        self.ui.pushButton_6.clicked.connect(self.lab_3_3)
        self.ui.pushButton_7.clicked.connect(self.lab_4)
        self.ui.pushButton_13.clicked.connect(self.lab_5)

        self.ui.pushButton_8.clicked.connect(self.lab_6_insert)
        self.ui.pushButton_9.clicked.connect(self.lab_6_delete)
        self.ui.pushButton_10.clicked.connect(self.lab_6_update)

        self.ui.pushButton_11.clicked.connect(self.lab_6_find)

        self.ui.radioButton.toggled.connect(self.lab_6_order)
        self.ui.radioButton_2.toggled.connect(self.lab_6_order)
        self.ui.radioButton_3.toggled.connect(self.lab_6_order)

        self.ui.pushButton_12.clicked.connect(self.lab_6_save_copy)

        self.ui.pushButton_14.clicked.connect(self.lab_7)
        self.ui.pushButton_15.clicked.connect(self.lab_10_open)
        self.ui.pushButton_20.clicked.connect(self.lab_10_path)
        self.ui.pushButton_21.clicked.connect(self.lab_10_size)
        self.ui.pushButton_17.clicked.connect(self.lab_10_read)
        self.ui.pushButton_16.clicked.connect(self.lab_10_write)
        self.ui.pushButton_18.clicked.connect(self.lab_10_close)


    def lab_1(self):
        a = float(self.ui.lineEdit.text())  # тестовое значение 5
        z1 = (math.sin(2 * a) + math.sin(5 * a) - math.sin(3 * a)) / (math.cos(a) - math.cos(3 * a) + math.cos(5 * a))  # -0.652065
        z2 = math.sin(3*a)/math.cos(3*a)  # -0.855993
        self.ui.label_3.setText(str(z1))
        self.ui.label_5.setText(str(z2))

    def lab_2_1(self):
        radius = int(self.ui.lineEdit_3.text())
        x = float(self.ui.lineEdit_2.text())

        self.ui.graphWidget.clear()
        self.ui.graphWidget.showGrid(x=True, y=True)

        x_list = list()
        y_list = list()

        for i in np.arange(-10, 2*radius+0.001, 0.001):
            if (i >= -10) & (i <= 0):
                x_list.append(i)
                y_list.append(-radius * ((i + 6) / 6))
            elif (i > 0) & (i < radius):
                x_list.append(i)
                y_list.append(-math.sqrt(radius ** 2 - i ** 2))
            elif (i >= radius) & (i <= 2 * radius):
                x_list.append(i)
                y_list.append(math.sqrt(radius ** 2 - (i - 2 * radius) ** 2))
        self.ui.graphWidget.plot(x_list, y_list)

        if (x > 2 * radius) | (x < -10):
            self.ui.label_9.setText("ошибка! выход за рамки диапазона")
        elif (x >= -10) & (x <= 0):
            self.ui.label_9.setText("прямая; при x = " + str(x) + " y = " + str(-radius * ((x + 6) / 6)))
        elif (x > 0) & (x < radius):
            self.ui.label_9.setText("первый радиус; при x = " + str(x) + " y = " + str(-math.sqrt(radius ** 2 - x ** 2)))
        elif (x >= radius) & (x <= 2 * radius):
            self.ui.label_9.setText("второй радиус; при x = " + str(x) + " y = "+ str(math.sqrt(radius ** 2 - (x - 2 * radius) ** 2)))

    def lab_2_2(self):
        radius = int(self.ui.lineEdit_6.text())
        x = float(self.ui.lineEdit_4.text())
        y = float(self.ui.lineEdit_5.text())

        if (x > 0) & (y > 0):
            if (x ** 2 + y ** 2 <= radius ** 2):
                self.ui.label_13.setText("точка попала в область")
            else:
                self.ui.label_13.setText("точка не попала в круг")
        elif (x < 0):
            if (x ** 2 + y ** 2 >= radius ** 2) & (y > 0):
                self.ui.label_13.setText("точка попала в область за кругом")
            elif (x > -radius) & (y > -radius) & (y >= x) & (x < 0) & (y < 0):
                self.ui.label_13.setText("точка попала в область треугольника")
            else:
                self.ui.label_13.setText("точка не попала в треугольник или за кругом")



    def lab_3_1(self):
        if float(self.ui.lineEdit_7.text()) > float(self.ui.lineEdit_8.text()):
            QMessageBox.about(self, "ошибка", "правое значение не может быть меньше левого")
            return

        self.ui.listWidget.clear()
        radius = int(self.ui.lineEdit_21.text())
        for i in np.arange(float(self.ui.lineEdit_7.text()), float(self.ui.lineEdit_8.text()) + float(self.ui.lineEdit_9.text()), float(self.ui.lineEdit_9.text())):
            if float("%.3f"%(i)) > float("%.3f"%(float(self.ui.lineEdit_8.text()))):
                break
            if (i > 2 * radius) | (i < -10):
                self.ui.listWidget.addItem("ошибка! выход за рамки диапазона")
            elif (i >= -10) & (i <= 0):
                self.ui.listWidget.addItem("прямая; при x = " + str("%.3f"%(i)) + " y = " + str("%.3f"%(-radius * ((i + 6) / 6))))
            elif (i > 0) & (i < radius):
                self.ui.listWidget.addItem("первый радиус; при x = " + str("%.3f"%(i)) + " y = " + str("%.3f"%(-math.sqrt(radius ** 2 - i ** 2))))
            elif (i >= radius) & (i <= 2 * radius):
                self.ui.listWidget.addItem("второй радиус; при x = " + str("%.3f"%(i)) + " y = " + str("%.3f"%(math.sqrt(radius ** 2 - (i - 2 * radius) ** 2))))


    def lab_3_2(self):
        if(self.fire_count == 10):
            self.fire_count = 0
            self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")
            self.ui.listWidget_2.clear()
            self.ui.graphWidget_2.clear()

        radius = int(self.ui.lineEdit_12.text())
        x = float(self.ui.lineEdit_10.text())
        y = float(self.ui.lineEdit_11.text())

        self.ui.graphWidget_2.showGrid(x=True, y=True)

        x_list = list()
        y_list = list()
        x_list_line = list()
        y_list_line = list()

        for i in np.arange(-radius, radius+0.001, 0.001):#построение полусферы и прямой
            x_list.append(i)
            y_list.append(math.sqrt(radius**2-i**2))
            if i < 0:
                x_list_line.append(i)
                y_list_line.append(i)

        self.ui.graphWidget_2.plot(x_list, y_list)
        self.ui.graphWidget_2.plot(x_list_line, y_list_line)
        self.ui.graphWidget_2.plot([-radius,0], [-radius,-radius])

        pen = pg.mkPen(style=QtCore.Qt.DashLine)
        self.ui.graphWidget_2.plot([-radius,-radius], [0,-radius], pen = pen)#вертикальная прерывистая

        pen_dot = pg.mkPen(color=(255, 0, 0))
        self.ui.graphWidget_2.plot([x-0.1, x+0.1], [y+0.1, y-0.1], pen=pen_dot)
        self.ui.graphWidget_2.plot([x-0.1, x+0.1], [y-0.1, y+0.1], pen=pen_dot)

        if (x > 0) & (y > 0):
            if (x ** 2 + y ** 2 <= radius ** 2):
                self.ui.listWidget_2.addItem(f"x = {x} y = {y} точка попала в область")
                self.fire_count+=1
                self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")
            else:
                self.ui.listWidget_2.addItem(f"x = {x} y = {y} точка не попала в круг")
                self.fire_count += 1
                self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")
        elif (x < 0):
            if (x ** 2 + y ** 2 >= radius ** 2) & (y > 0):
                self.ui.listWidget_2.addItem(f"x = {x} y = {y} точка попала в область за кругом")
                self.fire_count += 1
                self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")
            elif (x > -radius) & (y > -radius) & (y >= x) & (x < 0) & (y < 0):
                self.ui.listWidget_2.addItem(f"x = {x} y = {y} точка попала в область треугольника")
                self.fire_count += 1
                self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")
            else:
                self.ui.listWidget_2.addItem(f"x = {x} y = {y} точка не попала в треугольник или за кругом")
                self.fire_count += 1
                self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")
        else:
            self.ui.listWidget_2.addItem(f"x = {x} y = {y} точка не попала в треугольник или за кругом")
            self.fire_count += 1
            self.ui.label_22.setText(f"количество выстрелов - {self.fire_count}")

    def lab_3_3(self):
        x_start = float(self.ui.lineEdit_13.text())
        x_finish = float("%.6f" % (float(self.ui.lineEdit_14.text())))

        if (abs(x_start) >= 1) | (abs(x_finish) > 1):
            QMessageBox.about(self, "ошибка", "число не может быть больше 1")
            return

        dx = float(self.ui.lineEdit_15.text())
        rezult = list()

        for i in np.arange(x_start,x_finish + dx,dx):
            x = float("%.6f" % (i))
            if x > x_finish:
                break

            tailor = 0.0
            n = 0
            while abs(float("%.7f"%(tailor)) - float("%.7f"%(math.log(x+1)))) >= 0.000001:
                tailor = tailor + float(((-1)**n*(x)**(n+1))/(n+1))
                n = n+1

            rezult.append([x,"%.6f"%(math.log(x+1)), float("%.6f"%(tailor)), n])

        self.model = TableModel(rezult)
        self.ui.tableView.setModel(self.model)

    def shellSort(self, array):
        n = len(array)
        k = int(math.log2(n))
        interval = 2 ** k - 1
        while interval > 0:
            for i in range(interval, n):
                temp = array[i]
                j = i
                while j >= interval and array[j - interval] > temp:
                    array[j] = array[j - interval]
                    j -= interval
                array[j] = temp
            k -= 1
            interval = 2 ** k - 1
        return array


    def lab_4(self):
        spisok = list(map(float, self.ui.lineEdit_16.text().split()))

        sum = 0
        key = 1
        firs_minus = last_minus = -1

        self.ui.label_27.setText(f"кол-во элементов в списке: {len(spisok)}")

        for i in np.arange(1,len(spisok), 2):
            sum = sum + spisok[i]
        self.ui.label_29.setText(f"{sum}")

        for i in np.arange(0,len(spisok), 1):
            if (spisok[i] < 0) & (key != 0):
                firs_minus = i
                key = 0
            if spisok[i] < 0:
                last_minus = i

        if (firs_minus == last_minus) | (firs_minus == -1) | (last_minus == -1):
            QMessageBox.about(self, "ошибка", "первое и последнее отрицательное число совпадают")
        else:
            sum = 0
            for i in np.arange(firs_minus + 1,last_minus, 1):
                sum = sum + spisok[i]
            self.ui.label_31.setText(f"{sum}")

        after_sort = self.shellSort(spisok)
        self.ui.label_33.setText(f"отсортированный список: {after_sort}")

    def lab_5(self):
        n = int(self.ui.lineEdit_22.text())
        matrix = [[randint(0, 9) for _ in range(n)] for _ in range(n)]
        self.ui.label_40.setText('\n'.join(list(map(str, matrix))))

        self.ui.label_46.setText(str([reduce(mul, x, 1) for x in matrix if all(map(lambda a: a >= 0, x))]))

        dct = defaultdict(int)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dct[j - i] += matrix[i][j]

        self.ui.label_44.setText(str(max(dct.values())))

    def lab_6_insert(self):
        fio = self.ui.lineEdit_17.text()
        post = self.ui.lineEdit_19.text()
        year = self.ui.lineEdit_18.text()
        salary = self.ui.lineEdit_24.text()

        query = QSqlQuery()
        query.exec(f"insert into soldat(fio, post, year, salary) values ('{fio}', '{post}', {year}, {salary})")

        if (query.lastError().number() != -1):
            QMessageBox.about(self, "ошибка", f"{query.lastError().text()}")
            return

        self.soldat_model.setQuery(self.soldat_model.query().lastQuery())

    def lab_6_delete(self):
        query = QSqlQuery()
        query.exec(f"delete from soldat where id = {int(self.soldat_model.data(self.soldat_model.index(self.ui.tableView_2.currentIndex().row(), 0)))}")

        if (query.lastError().number() != -1):
            QMessageBox.about(self, "ошибка", f"{query.lastError().text()}")
            return

        self.soldat_model.setQuery(self.soldat_model.query().lastQuery())


    def lab_6_update(self):
        fio = self.ui.lineEdit_17.text()
        post = self.ui.lineEdit_19.text()
        year = self.ui.lineEdit_18.text()
        salary = self.ui.lineEdit_24.text()

        query = QSqlQuery()
        query.exec(f"update soldat set fio ='{fio}', post ='{post}', year ={year}, salary ={salary}  where id = {int(self.soldat_model.data(self.soldat_model.index(self.ui.tableView_2.currentIndex().row(), 0)))}")

        if (query.lastError().number() != -1):
            QMessageBox.about(self, "ошибка", f"{query.lastError().text()}")
            return

        self.soldat_model.setQuery(self.soldat_model.query().lastQuery())

    def lab_6_order(self):
        radioButton = self.sender()
        order_model = QSqlQueryModel()


        if radioButton.isChecked():
            if radioButton.text() == "фамилия":
                order_model.setQuery("select * from soldat order by fio asc")
            elif radioButton.text() == "оклад":
                order_model.setQuery("select * from soldat order by salary asc")
            elif radioButton.text() == "год":
                order_model.setQuery("select * from soldat order by year asc")

        self.set_header_lab_4(order_model)
        self.ui.tableView_4.setModel(order_model)
        self.ui.tableView_4.setColumnHidden(0, True)

    def lab_6_find(self):
        find_name = self.ui.lineEdit_20.text()

        find_model = QSqlQueryModel()
        find_model.setQuery(f"select * from soldat where fio like '{find_name}%'")

        self.ui.tableView_3.setModel(find_model)

    def lab_6_save_copy(self):

        fileName, _ = QFileDialog.getSaveFileName(self, "укажите название копии без расширения", "", "All Files (*);;Sqllite Files (*.sqlite)")
        if fileName:
            full_path = fileName + ".sqllite"
            shutil.copyfile('workers.sqlite', full_path)


    def lab_7(self):

        self.ui.graph1.clear()
        self.ui.graph1.addLegend()
        self.ui.graph1.showGrid(x=True, y=True)

        x_start = float(self.ui.lineEdit_25.text())
        x_finish = float(self.ui.lineEdit_23.text())
        b_param = float(self.ui.lineEdit_27.text())
        dx = float(self.ui.lineEdit_26.text())

        x_list = list()

        y_list = list()
        z_list = list()

        for i in np.arange(x_start, x_finish + dx, dx):
            x = round(i, 10)
            if x > x_finish:
                break

            x_list.append(x)
            z_list.append(math.atan(x) + b_param)

            tailor = math.pi/2
            n = 0
            while abs(round(tailor, 10) - round(math.atan(x), 10)) >= 0.000001:
                formul = ((-1)**(n+1))/((2*n+1)*x**(2*n+1))
                tailor = tailor + round(formul, 10)
                n = n + 1
            print(n)
            y_list.append(tailor)

        pen_y = pg.mkPen(color=(255, 0, 0))
        pen_z = pg.mkPen(color=(0, 255, 0))
        self.ui.graph1.plot()
        self.ui.graph1.plot(x_list, y_list, pen = pen_y, name = 'y(x)')
        self.ui.graph1.plot(x_list, z_list, pen = pen_z, name = 'z(x)')

    def lab_10_open(self):
        self.lab_10_classs.myData = self.lab_10_classs.open(self)
        print(self.lab_10_classs.myData)

    def lab_10_close(self):
        self.lab_10_classs.close(self)

    def lab_10_write(self):
        self.lab_10_classs.write(self)

    def lab_10_read(self):
        self.lab_10_classs.read(self)


    def lab_10_path(self):
        self.lab_10_classs.getPosition(self)

    def lab_10_size(self):
        self.lab_10_classs.getLenght(self)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())