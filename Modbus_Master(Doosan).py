import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from pymodbus.client import ModbusTcpClient
import time

if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행파일일 때
    base_path = sys._MEIPASS  # 임시로 리소스가 풀리는 경로
else:
    # 개발 환경(스크립트 직접 실행)일 때
    base_path = os.path.abspath(".")

ui_path = os.path.join(base_path, "qt", "modbus_master.ui")

from_class = uic.loadUiType(ui_path)[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Modbus_Master")
        #combobox 범위 설정
        for i in range(128,256):
            self.cb_read_start.addItem(str(i))
            self.cb_read_end.addItem(str(i))
            self.cb_write_start.addItem(str(i))
            self.cb_write_end.addItem(str(i))
        #로봇 상태 데이터 
        self.robot_states = {
            0: "BACKDRIVE HOLD : All brakes of 6 joints are engaged, and Backdrive motion is locked.",
            1: "BACKDRIVE RELEASE : Break of one or more joint(s) is released due to the selection of brake release.",
            2: "BACKDRIVE RELEASE by COCKPIT : Break of one or more joint(s) is released due to the Cockpit.",
            3: "SAFE OFF : The servo off state. This is robot stop state due to a function error or operation error.",
            4: "INITIALIZING : The initialization state for setting various parameters.",
            5: "INTERRUPTED : The system is in a protective stop state due to protective stop input, exceeding the safety threshold, etc.",
            6: "EMERGENCY STOP : The emergency stop state.",
            7: "AUTO MEASURE : The weight and center of gravity point of the end effector are measured automatically.",
            8: "RECOVERY STANDBY : Recovery in progress. All safety functions except for axis and TCP speed monitoring are disabled during recovery.",
            9: "RECOVERY JOGGING : The jogs of each axis can be used to correct the exceeded safety threshold.",
            10: "RECOVERY : The robot can be moved directly by hand to correct the exceeded safety threshold.",
            11: "MANUAL STANDBY : This is the default status of teaching.",
            12: "MANUAL JOGGING : The jog function is used to operate the robot.",
            13: "MANUAL HANDGUIDING : The robot can be operated manually during teaching.",
            14: "HIGH PRIORITY : The task program is being executed. White and Yellow are displayed by turns for a High Priority Zone.",
            15: "STANDALONE STANDBY : The Teach Pendant UI is in the actual mode execution screen in a single work space. White is displayed for a Standalone Zone.",
            16: "STANDALONE RUNNING : The task program is being executed. White is displayed for a Standalone Zone.",
            17: "HANDGUIDING CONTROL RUNNING : The robot pose can be changed by pressing the 'Handguiding' button.",
            18: "COLLABORATIVE RUNNING : The task program is being executed. Green is displayed for a Collaborative Zone.",
            19: "HANDGUIDING CONTROL STANDBY : The Handguiding command is executed during task program execution.",
            20: "HANDGUIDING CONTROL RUNNING : The robot pose can be changed by pressing the 'Handguiding' button.",
        }
        
        #UI 설정
        self.Read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Write_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Read_table.setAlternatingRowColors(True)
        self.Write_table.setAlternatingRowColors(True)
        #read, write 버튼 비활성화
        self.Read_bt.setEnabled(False)
        self.Write_bt.setEnabled(False)
        self.Read_Auto_bt.setEnabled(False)
        
        #클릭 버튼
        self.Connect_bt.clicked.connect(self.connect_clicked)
        self.Disconnect_bt.clicked.connect(self.disconnect_clicked)
        self.Close_bt.clicked.connect(self.close_clicked)
        self.Read_bt.clicked.connect(self.read_clicked)
        self.Write_bt.clicked.connect(self.write_clicked)
        # self.read_auto_bt.setCheckable(True)  # 토글 가능하게 만듬
        self.Read_Auto_bt.clicked.connect(self.Read_Auto_clicked)    
        
        #값 변화
        self.cb_write_start.currentIndexChanged.connect(self.write_table_update)
        self.cb_write_end.currentIndexChanged.connect(self.write_table_update)

        #실행 시 Write 범위 읽기
        self.write_table_update()

    def connect_clicked(self):
        ip = self.IP_Edit.text()
        port = self.PORT_Edit.text()
        
        #데이터 확인
        if ip == "" or port == "":
            QMessageBox.warning(self, 'None Data', 'Please insert IP, Port Number')
            return 90

        self.client = ModbusTcpClient(str(ip), port=int(port), timeout=3)
   
        # 서버에 연결 확인
        if self.client.connect():
            self.textEdit.setTextColor(QColor(0,255,0))
            self.textEdit.setText("Connecting")

            # QTimer 설정 - 로봇 상태 확인
            self.read_state_timer = QTimer(self)
            self.read_state_timer.timeout.connect(self.read_state)
            self.read_state_timer.start(500)  # 500ms마다 read_state 실행

            #read, write 버튼 활성화
            self.Read_bt.setEnabled(True)
            self.Write_bt.setEnabled(True)
            self.Read_Auto_bt.setEnabled(True)

        else:
            self.textEdit.setTextColor(QColor(255,0,0))
            self.textEdit.setText("Disconnecting")          

    def read_state(self): #로봇 상태 주소 259 번 
        try:
            result = self.client.read_holding_registers(address=259)
            self.Robot_State.setText(str(result.registers[0]))

            state_text = self.robot_states.get(result.registers[0], "Unknown State")
            self.Robot_State_label.setText(state_text)
        except Exception as e:
            # 예외 발생 시 메시지 출력 및 안전 종료
            self.Robot_State.setText("Comm Error")
            self.Robot_State_label.setText(f"Error: {str(e)}")

    def disconnect_clicked(self):
        try:
            self.client.close()
            self.read_state_timer.stop()
            self.read_state_timer.deleteLater()
        except:
            pass 

        self.textEdit.setTextColor(QColor(255,0,0))
        self.textEdit.setText("Disconnecting") 
        self.Robot_State.clear()
        self.Robot_State_label.clear()
        self.Read_table.clear()
        self.Write_table.clear()
        #read, write 버튼 비활성화
        self.Read_bt.setEnabled(False)
        self.Write_bt.setEnabled(False)
        self.Read_Auto_bt.setEnabled(False)

    def close_clicked(self):
        self.disconnect_clicked()
        sys.exit(app.exec_())

    def read_clicked(self):
        try:
            read_addr = min(int(self.cb_read_start.currentText()), int(self.cb_read_end.currentText()))
            read_cnt = abs(int(self.cb_read_start.currentText()) - int(self.cb_read_end.currentText())) + 1 #거꾸로 넣어도 절대값으로 count

            result = self.client.read_holding_registers(address=read_addr, count=read_cnt)

            #Table 에 데이터 표시
            self.Read_table.setRowCount(0) #항상 처음부터 표시
            for i in range(read_cnt):
                row = self.Read_table.rowCount()
                self.Read_table.insertRow(row)
                self.Read_table.setItem(i, 0, QTableWidgetItem(str(read_addr+i)))
                self.Read_table.setItem(i, 1, QTableWidgetItem(str(result.registers[i])))
        except:
            QMessageBox.warning(self, 'Read Fail', 'Please Check IP, Port Number')
    
    def Read_Auto_clicked(self, chacked):
        try:
            if chacked: #timer로 실시간 확인
                # 서버에 연결 확인
                if self.client.connect():
                    # QTimer 설정
                    self.read_auto_timer = QTimer(self)
                    self.read_auto_timer.timeout.connect(self.read_clicked)
                    self.read_auto_timer.start(500)  # 500ms마다 read_state 실행
                else:
                    self.textEdit.setTextColor(QColor(255,0,0))
                    self.textEdit.setText("Disconnecting") 
            else: #타이머 종료
                self.read_auto_timer.stop()
                self.read_auto_timer.deleteLater()
        except:
            QMessageBox.warning(self, 'Read Fail', 'Please Check IP, Port Number')

    def write_clicked(self):
        try:
            write_cnt = self.Write_table.rowCount() #개수 가져오기

            for row in range(write_cnt):
                write_addr = self.Write_table.item(row, 0).text()
                write_value = self.Write_table.item(row, 1).text()

                print("write_cnt = ",write_cnt)
                print(type(write_addr), type(write_value))

                if write_value != None: 
                    self.client.write_register(address=int(write_addr), value=int(write_value))
                else:
                    self.client.write_register(address=int(write_addr), value=0)
        except:
            QMessageBox.warning(self, 'Write Fail', 'Please Check IP, Port Number')

    def write_table_update(self):
        addr = min(int(self.cb_write_start.currentText()), int(self.cb_write_end.currentText()))
        cnt = abs(int(self.cb_write_start.currentText()) - int(self.cb_write_end.currentText())) + 1 #거꾸로 넣어도 절대값으로 count
        self.Write_table.setRowCount(0)
        for i in range(cnt):
            row = self.Write_table.rowCount()
            self.Write_table.insertRow(row)
            self.Write_table.setItem(i, 0, QTableWidgetItem(str(addr+i)))
            self.Write_table.setItem(i, 1, QTableWidgetItem("0"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # "Windows", "Fusion", "Macintosh" 등 시도 가능
    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 10pt;
        }
        QPushButton {
            background-color: #44475a;
            border: 1px solid #6272a4;
            border-radius: 6px;
            padding: 6px;
            color: #f8f8f2;
        }
        QPushButton:hover {
            background-color: #6272a4;
        }
        QPushButton:pressed {
            background-color: #44475a;
        }
        QPushButton:disabled {
            background-color: #3c3c3c;
            border: 1px solid #555555;
            color: #777777;  /* 흐릿한 회색 글자 */
        }
        QLineEdit, QComboBox, QTextEdit {
            background-color: #3c3f41;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px;
            color: #f8f8f2;
        }
        QHeaderView::section {
            background-color: #44475a;
            color: #f8f8f2;
            padding: 4px;
            border: 1px solid #555555;
        }
        QTableWidget {
            background-color: #2b2b2b;
            color: #f8f8f2;
            gridline-color: #6272a4;
            border: 1px solid #6272a4;
            alternate-background-color: #3a3f4b;  /* 홀수 줄 배경색 지정 */
        }

        QTableWidget::item {
            background-color: #2b2b2b;  /* 기본(짝수 줄) 배경색 */
            border-right: 1px solid #6272a4;
            border-bottom: 1px solid #6272a4;
        }

        QTableWidget::item:alternate {
            background-color: #3a3f4b;  /* 홀수 줄 배경색 */
        }

        QTableWidget::item:selected {
            background-color: #88aaff;
            color: #000000;
        }
        QTableWidget QTableCornerButton::section {
            background-color: #44475a;
            border: 1px solid #6272a4;
        }
    """)

    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())