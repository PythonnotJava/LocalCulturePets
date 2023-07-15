# I want to put widgets that is uesd to input by users here.
from PyQt5.QtWidgets import QLineEdit, QWidget
from PyQt5.QtCore import QRect, Qt
from typing import Optional

class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos: int,
                  y_pos: int,
                  width: int,
                  height: int,
                  object_name: Optional[str] = None,
                  just_read : bool = True,
                  forbid_right_action : bool = True,
                  # text
                  text : Optional[str] = None,
                  # tips
                  tip_content: Optional[str] = None,
                  # qss
                  qss: Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))
        self.setReadOnly(just_read)

        if parent is not None:
            self.setParent(parent)

        if text is not None:
            self.setText(text)

        if object_name is not None:
            self.setObjectName(object_name)

        if forbid_right_action:
            self.setContextMenuPolicy(Qt.NoContextMenu)

        if tip_content is not None:
            self.setToolTip(tip_content)

        if qss is not None:
            self.setStyleSheet(qss)
