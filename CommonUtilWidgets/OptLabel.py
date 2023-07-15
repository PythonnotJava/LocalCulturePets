# I use label as a board
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from typing import Optional

class Label(QLabel):
    def __init__(self):
        super().__init__()

    def setWidget(self,
                  parent: Optional[QWidget],
                  x_pos: int,
                  y_pos: int,
                  width: int,
                  height: int,
                  object_name: Optional[str] = None,
                  auto_wrap : bool = False,
                  # text
                  label_text: Optional[str] = None,
                  # img
                  set_pixmap : bool = False,
                  pixmap_path : Optional[str] = None,
                  scaled : bool = True,
                  # tips
                  tip_content: Optional[str] = None,
                  # qss
                  qss: Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))
        self.setWordWrap(auto_wrap)

        if parent is not None:
            self.setParent(parent)

        if object_name is not None:
            self.setObjectName(object_name)

        if set_pixmap and pixmap_path is not None:
            if scaled:
                self.setPixmap(QPixmap(pixmap_path).scaled(self.size()))
            else:
                self.setPixmap(QPixmap(pixmap_path))
        else:
            if label_text is not None:
                self.setText(label_text)

        if tip_content is not None:
            self.setToolTip(tip_content)

        if qss is not None:
            self.setStyleSheet(qss)
