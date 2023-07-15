# Optimized version of the progress bar
from PyQt5.QtWidgets import QProgressBar, QWidget
from PyQt5.QtCore import QRect, Qt
from typing import Optional

class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos : int,
                  y_pos : int,
                  width : int,
                  height : int,
                  object_name : Optional[str] = None,
                  # progress_information
                  min_num : int = 0,
                  max_num : int = 200,
                  current_value: int = 50,
                  direction = Qt.Horizontal,
                  # value format
                  Format : str = '%v',
                  # qss
                  qss : Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))
        self.setMinimum(min_num)
        self.setMaximum(max_num)
        self.setValue(current_value)
        self.setOrientation(direction)
        self.setFormat(Format)

        if parent is not None:
            self.setParent(parent)

        if object_name is not None:
            self.setObjectName(object_name)

        if qss is not None:
            self.setStyleSheet(qss)