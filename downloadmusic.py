import sys
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout,\
    QTableWidget,QVBoxLayout,QLineEdit,QHeaderView,QMenu,QComboBox,QTableWidgetItem,QTableView,\
    QAbstractItemView
import PyQt5.sip
from qq import qqgetsongs
from wyy import wygetsongs
from kw import kwgetsongs
import requests

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Music')
        self.setFixedSize(700,500)
        # 全局布局
        self.all_layout = QVBoxLayout()
        # 子布局
        self.top_layout = QHBoxLayout()
        self.mid_layout = QVBoxLayout()

        self.top_init()
        self.mid_init()
        self.signal_init()
        self.layout_init()



    def top_init(self):

        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText('请输入歌手或歌曲名')

        self.searchbutton = QPushButton('搜索', self)
        self.searchbutton.clicked.connect(self.searchbutton_func)
        self.my_thread = wyythread()
        self.my_thread.my_signal.connect(self.settable)

        self.choice = QComboBox()
        self.choice.addItems(['网易云音乐', 'QQ音乐', '酷我音乐'])

        self.top_layout.addWidget(self.input_line)
        self.top_layout.addWidget(self.choice)
        self.top_layout.addWidget(self.searchbutton)


    def mid_init(self):
        self.table = QTableWidget(self)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)# 设置只有行选中, 整行选中
        self.table.resizeColumnsToContents()  # 设置列宽高按照内容自适应
        self.table.resizeRowsToContents()  # 设置行宽和高按照内容自适应
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(0)  # 行下标最大值
        self.table.setColumnCount(3)  # 列
        self.table.setHorizontalHeaderLabels(['歌手', '歌曲', '状态'])  # 标题列
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 允许右键产生菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将右键菜单绑定到槽函数generateMenu
        self.table.customContextMenuRequested.connect(self.generateMenu)
        self.mid_layout.addWidget(self.table)

    def generateMenu(self,pos):
        row_num = -1
        for i in self.table.selectionModel().selection().indexes():
            row_num = i.row()

        # 表格中只有两条有效数据，所以只在前两行支持右键弹出菜单
        if row_num >=0:
            menu = QMenu()
            item1 = menu.addAction(u'下载')
            action = menu.exec_(self.table.mapToGlobal(pos))
            # 显示选中行的数据文本
            if action == item1:
                try:
                    path =songs[row_num][0]+'-'+songs[row_num][2]+'.mp3'
                    with open(path,'wb') as fp:
                        ms = requests.get(songs[row_num][1])
                        fp.write(ms.content)
                except:
                    pass



    def layout_init(self):

        self.all_layout.addLayout(self.top_layout)
        self.all_layout.addLayout(self.mid_layout)
        self.setLayout(self.all_layout)

    #searchbutton
    def searchbutton_func(self):
        global keyword
        keyword = self.input_line.text()+'.'+self.choice.currentText()
        self.my_thread.start()

    def settable(self,data):
        global songs
        songs = data
        self.table.setRowCount(0)
        i=0
        # self.table.setItem(0, 0, data)
        for song in data:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(i,0,QTableWidgetItem(song[2]))
            self.table.setItem(i, 1, QTableWidgetItem(song[0]))
            if song[1]=='':
                self.table.setItem(i, 2, QTableWidgetItem('不可下载'))
            else:
                self.table.setItem(i, 2, QTableWidgetItem('可下载'))
            i=i+1

    #初始化信号
    def signal_init(self):
        pass

class wyythread(QThread):
    #定义一个信号，传递一个list
    my_signal = pyqtSignal(list)
    def __init__(self):
        super().__init__()
    def run(self):
        try:
            key = keyword.split('.')
            if key[-1] == '网易云音乐':
                songs = wygetsongs(key[0])
            elif key[-1] == 'QQ音乐':
                songs = qqgetsongs(key[0])
            elif key[-1] == '酷我音乐':
                songs = kwgetsongs(key[0])
            self.my_signal.emit(songs)
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MusicPlayer()
    demo.show()
    sys.exit(app.exec_())
