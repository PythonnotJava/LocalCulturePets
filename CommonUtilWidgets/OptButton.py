# Optimized buttons
from PyQt5.QtWidgets import QPushButton, QWidget, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QRect
from typing import Optional, Callable

class PushButton(QPushButton):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos : int,
                  y_pos : int,
                  width : int,
                  height : int,
                  object_name: Optional[str] = None,
                  # func
                  func: Optional[Callable] = None,
                  # icon
                  use_icon: bool = False,
                  icon_path : Optional[str] = None,
                  icon_fixed_size : bool = True,
                  # text
                  button_name : Optional[str] = None,
                  # tips
                  tip_content : Optional[str] = None,
                  # qss
                  qss : Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))

        if parent is not None:
            self.setParent(parent)

        if func is not None:
            self.clicked.connect(func)

        if object_name is not None:
            self.setObjectName(object_name)

        if use_icon and icon_path is not None:
            self.setIcon(QIcon(QPixmap(icon_path)))
            if icon_fixed_size:
                self.setIconSize(self.size())
        else:
            if button_name is not None:
                self.setText(button_name)

        if tip_content is not None:
            self.setToolTip(tip_content)

        if qss is not None:
            self.setStyleSheet(qss)
# I prefer to call QRadioButton ToggleButton，instead of RadioButton.
class ToggleButton(QRadioButton):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos: int,
                  y_pos: int,
                  width: int,
                  height: int,
                  object_name: Optional[str] = None,
                  # func
                  func: Optional[Callable] = None,
                  # tips
                  tip_content: Optional[str] = None,
                  # qss
                  qss: Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))

        if parent is not None:
            self.setParent(parent)

        if object_name is not None:
            self.setObjectName(object_name)

        if func is not None:
            self.clicked.connect(func)

        if tip_content is not None:
            self.setToolTip(tip_content)

        if qss is not None:
            self.setStyleSheet(qss)
