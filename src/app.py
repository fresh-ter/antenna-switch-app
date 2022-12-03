import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, qApp, QMessageBox
from PyQt5 import QtGui

import pyhid_usb_relay


relay = None

r_status = 0


def r_all_off():
    global relay

    print("all off!!!")
    relay[1] = False
    relay[2] = False
    relay[3] = False
    relay[4] = False


def r_run(r_num):
    global relay

    r_all_off()

    print(r_num, ' (*)')

    relay[r_num] = True

    status = r_num


def main():
    global relay

    app = QApplication(sys.argv)
    icon = QtGui.QIcon('icon.png')

    try:
        relay = pyhid_usb_relay.find()
    except pyhid_usb_relay.exceptions.DeviceNotFoundError:
        print(404)
        msg = QMessageBox()
        msg.setWindowIcon(icon)   
        msg.setWindowTitle("Antenna switch")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("No device found!")
        msg.exec_()
        return

    r_all_off()

    # createTrayMenu
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(icon)

    def a_toggle(num):
        l = [
            r_1_action,
            r_2_action,
            r_3_action,
            r_4_action
            ]

        if not l[num-1].isChecked():
            r_all_off()
            return

        l.pop(num-1)

        for x in l:
            x.setChecked(False)

        r_run(num)

    def quit():
        r_all_off()
        qApp.quit()

    def print_status():
        s = ''
        s += 'relay 1 ->' + str(relay.get_state(1)) + '\n'
        s += 'relay 2 ->' + str(relay.get_state(2)) + '\n'
        s += 'relay 3 ->' + str(relay.get_state(3)) + '\n'
        s += 'relay 4 ->' + str(relay.get_state(4)) + '\n'
        print(s)
        tray_icon.showMessage(
                "Antenna switch",
                s,
                QSystemTrayIcon.Information,
                2000
            )

    r_1_action = QAction("Antenna 1")
    r_1_action.setCheckable(True)
    r_1_action.toggled.connect(lambda: a_toggle(1))
    
    r_2_action = QAction("Antenna 2")
    r_2_action.setCheckable(True)
    r_2_action.toggled.connect(lambda: a_toggle(2))

    r_3_action = QAction("Antenna 3")
    r_3_action.setCheckable(True)
    r_3_action.toggled.connect(lambda: a_toggle(3))

    r_4_action = QAction("Antenna 4")
    r_4_action.setCheckable(True)
    r_4_action.toggled.connect(lambda: a_toggle(4))

    status_action = QAction("Status")
    status_action.triggered.connect(print_status)

    quit_action = QAction("Exit")

    quit_action.triggered.connect(quit)

    tray_menu = QMenu()

    tray_menu.addAction(r_1_action)
    tray_menu.addAction(r_2_action)
    tray_menu.addAction(r_3_action)
    tray_menu.addAction(r_4_action)
    tray_menu.addSeparator()

    tray_menu.addAction(status_action)

    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)

    tray_icon.setContextMenu(tray_menu)

    tray_icon.show()

    sys.exit(app.exec())

 
if __name__ == "__main__":
    main()
