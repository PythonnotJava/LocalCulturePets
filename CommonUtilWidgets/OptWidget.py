# It's necessary to wrap some common base widgets.
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QRect
from typing import Optional

class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos: int,
                  y_pos: int,
                  width: int,
                  height: int,
                  object_name: Optional[str] = None,
                  # qss
                  qss: Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))

        if object_name is not None:
            self.setObjectName(object_name)

        if qss is not None:
            self.setStyleSheet(qss)
            print('qss = ', qss)

        if parent is not None:
            self.setParent(parent)