import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui
import time

import main


class CountProgress(QtCore.QThread):
    changed = QtCore.Signal()

    def __init__(self):
        super(CountProgress, self).__init__()
        self.count = 0
        self.stop = False
        self.time_limit = 100

    def run(self) -> None:
        self.stop = False
        while not self.stop and self.count < self.time_limit:
            self.count += 1
            time.sleep(1)
            self.changed.emit()



class AskFilePopup(QtWidgets.QWidget):

    confirmed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.filename = None
        self.ask_filename = QtWidgets.QFileDialog()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.ask_filename)
        self.ask_filename.fileSelected.connect(self.file_selected)

    @QtCore.Slot()
    def file_selected(self, filename):
        self.filename = filename
        self.confirmed.emit()
        print(filename)


class Home(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.engine = main.Main()

        self.filename = None
        self.function = None
        self.algorithm = None
        self.estimated_time = None

        self.count_progress = CountProgress()
        self.ask_filename_popup = None

        self.text1 = QtWidgets.QLabel('从')
        self.text2 = QtWidgets.QLabel('中')
        self.text3 = QtWidgets.QLabel('，而且要用')
        self.text4 = QtWidgets.QLabel('!')

        self.select_file_button = QtWidgets.QPushButton('这个文件')
        self.select_function_button = QtWidgets.QPushButton('做个事情')
        self.select_algorithm_button = QtWidgets.QPushButton('这个方法')
        self.go_button = QtWidgets.QPushButton("冲了!>>>")

        self.select_function_button.setDisabled(True)
        self.select_algorithm_button.setDisabled(True)
        self.go_button.setDisabled(True)

        self.functional_menu = QtWidgets.QMenu()
        self.action_vocal_extractor = QtGui.QAction('提取人声')
        self.functional_vocal_extractor = self.action_vocal_extractor
        self.functional_TBD = QtGui.QAction('"新建文件夹"')
        self.functional_menu.addAction(self.functional_vocal_extractor)
        self.functional_menu.addAction(self.functional_TBD)
        self.select_function_button.setMenu(self.functional_menu)

        self.algorithm_menu = QtWidgets.QMenu()
        self.algorithm_unknown = QtGui.QAction('功能都不选，还挑剔方法？')
        self.algorithm_menu.addAction(self.algorithm_unknown)
        self.select_algorithm_button.setMenu(self.algorithm_menu)

        self.action_vocal_extractor.triggered.connect(self.select_function_vocal_extractor)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.text1, 0, 0)
        self.layout.addWidget(self.select_file_button, 0, 1)
        self.layout.addWidget(self.text2, 0, 2)
        self.layout.addWidget(self.select_function_button, 0, 3)
        self.layout.addWidget(self.text3, 0, 4)
        self.layout.addWidget(self.select_algorithm_button, 0, 5)
        self.layout.addWidget(self.text4, 0, 6)
        self.layout.addWidget(self.go_button, 0, 7)
        self.layout.addWidget(self.progress_bar, 1, 0, 1, 8)
        self.select_file_button.clicked.connect(self.select_file)
        self.go_button.clicked.connect(self.go)

    @QtCore.Slot()
    def select_file(self):
        self.ask_filename_popup = AskFilePopup()
        self.ask_filename_popup.confirmed.connect(self.file_selected)
        self.ask_filename_popup.resize(900, 300)
        self.ask_filename_popup.show()

    @QtCore.Slot()
    def file_selected(self):
        self.filename = self.ask_filename_popup.filename
        basename = os.path.basename(self.filename)
        self.select_file_button.setText(basename)
        self.ask_filename_popup.close()
        self.select_function_button.setDisabled(False)
        print(os.path.getsize(self.filename))
        self .estimated_time = os.path.getsize(self.filename) / 30

    @QtCore.Slot()
    def go(self):
        self.count_progress.count = 0
        self.count_progress.changed.emit()

        self.select_file_button.setDisabled(True)
        self.select_function_button.setDisabled(True)
        self.select_algorithm_button.setDisabled(True)
        self.go_button.setDisabled(True)

        self.engine.add_ffmpeg_to_env()
        print(self.filename)
        self.engine.global_objects['filename'] = self.filename
        self.count_progress.changed.connect(self.update_progress_bar)
        self.count_progress.start()
        self.engine.start()
        self.engine.finished.connect(self.engine_finished)



    @QtCore.Slot()
    def engine_finished(self):
        self.count_progress.count = 100
        self.count_progress.wait()
        self.count_progress.terminate()
        self.select_file_button.setText('这个文件')
        self.select_file_button.setDisabled(False)

    @QtCore.Slot()
    def update_progress_bar(self):
        self.progress_bar.setValue(self.count_progress.count)

    @QtCore.Slot()
    def select_function_vocal_extractor(self):
        self.select_algorithm_button.setDisabled(False)
        self.function = 'vocal_extractor'
        self.select_function_button.setText('提取人声')

        self.algorithm_vocal_extractor_menu = QtWidgets.QMenu()
        self.algorithm_action_vocal_extractor_openunmix = QtGui.QAction('Open Unmix(默认)')
        self.algorithm_action_vocal_extractor_openunmix.triggered.connect(self.select_algorithm_vocal_extractor_openunmix)
        self.algorithm_vocal_extractor_menu.addAction(self.algorithm_action_vocal_extractor_openunmix)
        self.select_algorithm_button.setMenu(self.algorithm_vocal_extractor_menu)

    @QtCore.Slot()
    def select_algorithm_vocal_extractor_openunmix(self):
        self.go_button.setDisabled(False)
        self.algorithm = 'openunmix'
        self.select_algorithm_button.setText('Open Unmix(默认)')



def run_gui():
    app = QtWidgets.QApplication([])

    widget = Home()
    widget.setWindowTitle('音频小工具')
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
