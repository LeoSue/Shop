# Copyright(c)2019 Yifan Li
from PyQt5.QtWidgets import *
import numpy as np
import functools
import time


class Cart(QWidget):
    def __init__(self, username, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.username = username
        self.initUI()

    def initUI(self):
        """
        设置确认订单按钮，点击后执行此函数，显示订单页面
        :return:
        """
        self.setWindowTitle("MY CART")
        self.resize(500, 650)
        self.layout = QVBoxLayout()
        data = self.get_data()
        rows = data.shape[0]
        data = data.transpose()
        self.TableWidget = QTableWidget(rows, 5)
        self.TableWidget.setHorizontalHeaderLabels(
            ['商品编号', '商品名称', '商品数量', '商品单价', '删除'])
        # TODO 设置水平方向表格为自适应的伸缩模式
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # TODO 将表格变为禁止编辑
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # TODO 设置表格整行选中
        self.TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # TODO 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(self.TableWidget)
        QTableWidget.resizeRowsToContents(self.TableWidget)
        data = data.transpose()
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                newItem = QTableWidgetItem(str(data[i][j]))
                self.TableWidget.setItem(i, j, newItem)

        for i in range(data.shape[0]):
            searchBtn = QPushButton('删除')
            searchBtn.tag = i + 1
            searchBtn.setDown(True)
            searchBtn.setStyleSheet('Button{margin:3px}')
            self.TableWidget.setCellWidget(i, 4, searchBtn)
            searchBtn.clicked.connect(
                functools.partial(
                    self.sub_goods, data[i][0]))
            # self.searchBtn.clicked.connect(self.add)

        # 计算总价
        price = []
        num = []
        data = data.transpose()
        self.label = QLabel(self)
        self.label.setText('总价：0')
        if len(data) > 0:
            for i in data[2]:
                num.append(int(i))
            for j in data[3]:
                price.append(float(j))
            sum_row = data.shape[1] + 1
            sum = np.dot(num, price)
            self.label.setText('总价：' + str(sum))

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.TableWidget)
        self.setLayout(self.layout)

    def sub_goods(self, n):
        self.cursor.execute(
            "SELECT UNIQUE_ID from user_goods where USER_ID='" +
            self.username +
            "' AND id='" +
            str(n) +
            "'")
        result = self.cursor.fetchall()
        if len(result) > 0:
            self.cursor.execute(
                "DELETE from user_goods where UNIQUE_ID=" +
                result[0][0])
        self.db.commit()
        self.updata_data()

    def get_data(self):
        self.cursor.execute(
            "select ID,GOODS_NAME,count(ID),Price from user_goods where USER_ID='" +
            self.username +
            "'group by ID, USER_ID")
        data = self.cursor.fetchall()
        array = np.array(data)
        return array

    def updata_data(self):
        data = self.get_data()
        self.TableWidget.clear()
        self.TableWidget.setRowCount(len(data))
        self.TableWidget.setHorizontalHeaderLabels(
            ['商品编号', '商品名称', '商品数量', '商品单价', '删除'])

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                newItem = QTableWidgetItem(str(data[i][j]))
                self.TableWidget.setItem(i, j, newItem)

        for i in range(data.shape[0]):
            searchBtn = QPushButton('删除')
            searchBtn.tag = i + 1
            searchBtn.setDown(True)
            searchBtn.setStyleSheet('Button{margin:3px}')
            self.TableWidget.setCellWidget(i, 4, searchBtn)
            searchBtn.clicked.connect(
                functools.partial(
                    self.sub_goods, data[i][0]))

        self.label.setText('总价：0')
        price = []
        num = []
        data = data.transpose()
        if len(data) > 0:
            for i in data[2]:
                num.append(int(i))
            for j in data[3]:
                price.append(float(j))
            sum = np.dot(num, price)
            self.label.setText('总价：' + str(sum))
