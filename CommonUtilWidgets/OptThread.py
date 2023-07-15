# Encapsulated QThread and QTimer
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from typing import Callable

class Loader(QThread):

    load_suc : pyqtSignal = pyqtSignal(str)

    def __init__(self, path : str, delayTime : int = 1):
        super().__init__()
        self.fpath = path
        self.delay = delayTime

    def run(self) -> None:
        self.sleep(self.delay)
        with open(self.fpath, 'r', encoding='U8') as file:
            qss = file.read()
        self.load_suc.emit(qss)

class Timer(QTimer):
    def __init__(self):
        super().__init__()

    def setTimer(self, linked_func : Callable, step : int = 100, *args):
        self.setInterval(step)
        self.timeout.connect(lambda : linked_func(args))
