# Copyright(c)2019 Chunyu Su
from PyQt5.QtWidgets import *
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QTableWidgetItem)
import time
import threading


# 商城Mall类
class Shop(QWidget):
    def __init__(self, username, db, cursor):
        super().__init__()
        self.username = username
        self.db = db
        self.cursor = cursor
        self.init_ui()

    def init_ui(self):
        self.cursor.execute("SELECT * FROM GOODS")
        self.data = self.cursor.fetchall()

        self.setWindowTitle("Mall")
        self.resize(900, 700)
        layout = QHBoxLayout()
        TableWidget = QTableWidget(len(self.data), 6)
        # Todo 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        TableWidget.setHorizontalHeaderLabels(
            ['商品编号', '商品名称', '商品品牌', '价格', '添加购物车', '减少购物车'])
        # Todo  设置垂直方向的表头标签
        # TableWidget.setVerticalHeaderLabels(['行1', '行2', '行3', '行4'])

        # TODO 设置水平方向表格为自适应的伸缩模式
        TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # TODO 将表格变为禁止编辑
        TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # TODO 设置表格整行选中
        TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # TODO 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(TableWidget)
        QTableWidget.resizeRowsToContents(TableWidget)

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                newItem = QTableWidgetItem(str(self.data[i][j]))
                TableWidget.setItem(i, j, newItem)

        for i in range(len(self.data)):
            addBtn = QPushButton('添加' + str(i + 1))
            addBtn.setDown(True)
            addBtn.setStyleSheet('QPushButton{margin:3px}')
            TableWidget.setCellWidget(i, 4, addBtn)
            addBtn.clicked.connect(lambda: self.add_goods())
        for i in range(len(self.data)):
            addBtn = QPushButton('减少' + str(i + 1))
            addBtn.setDown(True)
            addBtn.setStyleSheet('QPushButton{margin:3px}')
            TableWidget.setCellWidget(i, 5, addBtn)
            addBtn.clicked.connect(lambda: self.sub_goods())

        layout.addWidget(TableWidget)
        self.setLayout(layout)

    def add_goods(self):
        sender = self.sender().text()
        commodity_num = str(sender[2:10])
        num = int(commodity_num)
        print((time.time(),
               self.data[num][0],
               self.username,
               self.data[num][1],
               1,
               self.data[num][3]))
        self.cursor.execute(
            '''INSERT INTO USER_GOODS (UNIQUE_ID,ID,USER_ID,GOODS_NAME,QUANTITY,PRICE) VALUES(?, ?, ?, ?, ?, ?)''',
            (time.time(),
             self.data[num][0],
             self.username,
             self.data[num][1],
             1,
             self.data[num][3]))
        self.db.commit()

    def sub_goods(self):
        sender = self.sender().text()
        commodity_num = str(sender[2:10])
        self.cursor.execute(
            "SELECT UNIQUE_ID FROM USER_GOODS WHERE USER_ID=? AND ID=?",
            (self.username,
             commodity_num))
        result = self.cursor.fetchall()
        if len(result) > 0:
            self.cursor.execute(
                "DELETE FROM USER_GOODS WHERE UNIQUE_ID=" +
                result[0][0])
        self.db.commit()
