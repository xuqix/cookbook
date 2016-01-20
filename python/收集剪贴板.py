class CopyCollector(QtGui.QWidget):
    def __init__(self,parent=None):
        self.__app=QtGui.QApplication([])
        self.Result=[]
        super(CopyCollector,self).__init__()
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('剪贴板文本收集器')
        self.__oldTxt=self.__app.clipboard().text()
        #列表框self.lst
        self.__lst=QtGui.QListWidget()
        #定时器self.timer
        self.__timer=QtCore.QTimer(self)
        self.__timer.timeout.connect(self.__ClipMonitor)
        self.__timer.setInterval(100)
        #定时器启动/暂停开关self.btnSwitch
        self.__btnSwitch=QtGui.QPushButton('Start')
        self.__btnSwitch.clicked.connect(self.__btnSwitch_Clicked)
        #列表项移除按钮self.btnRemove
        self.__btnRemove=QtGui.QPushButton('Remove')
        self.__btnRemove.clicked.connect(self.__btnRemove_Clicked)
        #设置窗口布局
        lay=QtGui.QGridLayout()
        lay.addWidget(self.__lst,0,0,5,2)
        lay.addWidget(self.__btnSwitch,6,0,1,1)
        lay.addWidget(self.__btnRemove,6,1,1,1)        
        self.setLayout(lay)
        self.show()
        self.__app.exec_()
    def __ClipMonitor(self):
        txt=self.__app.clipboard().text()
        if txt!=self.__oldTxt:
            self.__oldTxt=txt
            self.__lst.addItem(txt)
    def __btnSwitch_Clicked(self,cancel=False):
        if self.__timer.isActive():
            self.__timer.stop()
            self.__btnSwitch.setText('Start')
        else:
            self.__oldTxt=self.__app.clipboard().text()
            self.__timer.start()
            self.__btnSwitch.setText('Stop')
    def __btnRemove_Clicked(self,cancel=False):
        if self.__lst.currentRow()!=-1:
            self.__lst.takeItem(self.__lst.currentRow())
    def closeEvent(self,event):
        for i in range(self.__lst.count()):
            self.Result.append(self.__lst.item(i).text())
