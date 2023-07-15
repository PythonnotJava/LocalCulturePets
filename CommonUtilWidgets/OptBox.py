
from PyQt5.QtWidgets import QGroupBox, QWidget
from PyQt5.QtCore import QRect
from typing import Optional

class GroupBox(QGroupBox):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos: int,
                  y_pos: int,
                  width: int,
                  height: int,
                  object_name: Optional[str] = None,
                  # title
                  title : Optional[str] = None,
                  # qss
                  qss: Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))

        if parent is not None:
            self.setParent(parent)

        if object_name is not None:
            self.setObjectName(object_name)

        if title is None:
            self.setTitle('')
        else:
            self.setTitle(title)

        if qss is not None:
            self.setStyleSheet(qss)