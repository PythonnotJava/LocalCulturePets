from PyQt5.Qt import QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import Qt, QRect, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsDropShadowEffect
from CommonUtilWidgets import Label, PushButton, GroupBox
from sys import argv, exit
from typing import Union, Optional, Any, overload, Callable

# In fact, I encapsulate it for the purpose of animating the prompt box.
class AnimationMessageBoxLog(QWidget):
    def __init__(self):
        super().__init__()
    def setWidget(self,
                  parent : Optional[QWidget],
                  x_pos : int,
                  y_pos : int,
                  width : int,
                  height : int,
                  object_name : Optional[str] = None,
                  flags : Union[Qt.WindowFlags, Qt.WindowType] = Qt.CustomizeWindowHint,
                  modal : bool = True
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))

        if parent is not None:
            self.setParent(parent)

        if object_name is not None:
            self.setObjectName(object_name)

        if flags is not None:
            self.setWindowFlags(flags)

        if modal:
            self.setWindowModality(Qt.WindowModal)

    def setAnimation(self, _type : str, target : QObject, start : Any, end : Any, duration : int = 1000, loop : int = 1):
        _animation = QPropertyAnimation(self)
        _animation.setPropertyName(_type.encode())
        _animation.setTargetObject(target)
        _animation.setStartValue(start)
        _animation.setEndValue(end)
        _animation.setDuration(duration)
        _animation.setLoopCount(loop)
        _animation.start()

    def setEdgeShadow(self,
                      parent : Optional[QWidget] = None,
                      offset : list[int, int] = (0, 0),
                      radius : float = 10.,
                      color : Union[QColor, Qt.GlobalColor] = Qt.gray):
        _shadow = QGraphicsDropShadowEffect()
        if parent is None:
            self.setGraphicsEffect(_shadow)
        else:
            parent.setGraphicsEffect(_shadow)
        _shadow.setOffset(*offset)
        _shadow.setBlurRadius(radius)
        _shadow.setColor(color)

    def setEasingCurveAnimation(self, _type : str,
                                curveName : QEasingCurve.Type,
                                target : QObject,
                                start : Any, end : Any, duration : int = 1000,
                                loop : int = 1,
                                amplitude : Optional[float] = None,
                                overshoot : Optional[float] = None,
                                period : Optional[float] = None
                                ):
        _animation = QPropertyAnimation(self)

        easingCurve = QEasingCurve(curveName)
        if amplitude is not None:
            easingCurve.setAmplitude(amplitude)
        if overshoot is not None:
            easingCurve.setOvershoot(overshoot)
        if period is not None:
            easingCurve.setPeriod(period)

        _animation.setPropertyName(_type.encode())
        _animation.setTargetObject(target)
        _animation.setStartValue(start)
        _animation.setEndValue(end)
        _animation.setDuration(duration)
        _animation.setEasingCurve(easingCurve)
        _animation.setLoopCount(loop)
        _animation.start()

# I'm actually having trouble writing the AnimationMessageBoxLog.
# The AssembleAnimationMessageBoxLog_SingleButton inside is
# only a label which is used to send status to user
# (The status you can see its definition in global constants--CURRENT_TASK_STATUS)
# and a single button.
class AssembleAnimationMessageBoxLog_SingleButton(AnimationMessageBoxLog):
    def __init__(self):
        super().__init__()

        self.centerLabel = Label()
        self.singleButton = PushButton()
        self.baseWidget = GroupBox()
        self.baseWidget.setParent(self)
        self.baseWidget.setObjectName('baseWidget')
    @overload
    def setWidget(self,
                  parent : Optional[QWidget],
                  x_pos : int,
                  y_pos : int,
                  width : int,
                  height : int,
                  object_name : Optional[str] = None,
                  flags : Union[Qt.WindowFlags, Qt.WindowType] = Qt.CustomizeWindowHint,
                  modal : bool = True,
                  reason : Optional[str] = None
                  ): ...
    @overload
    def setWidget(self,
                  parent : Optional[QWidget],
                  x_pos : int,
                  y_pos : int,
                  width : int,
                  height : int,
                  object_name : Optional[str] = None,
                  flags : Union[Qt.WindowFlags, Qt.WindowType] = Qt.CustomizeWindowHint,
                  modal : bool = True,
                  # label
                  reason: Optional[str] = None,
                  label_rect: list[int, int, int, int] = (10, 10, 10, 10),
                  label_name: Optional[str] = 'centerLabel',
                  # button
                  button_text: str = "",
                  button_rect: list[int, int, int, int] = (20, 20, 20, 20),
                  button_name: Optional[str] = 'button',
                  button_function: Callable = lambda: ...,
                  # all_qss
                  qss_with_child_qss: Optional[str] = None
                  ): ...
    def setWidget(self,
                  parent : Optional[QWidget],
                  x_pos : int,
                  y_pos : int,
                  width : int,
                  height : int,
                  object_name : Optional[str] = None,
                  flags : Union[Qt.WindowFlags, Qt.WindowType] = Qt.CustomizeWindowHint,
                  modal : bool = True,
                  # label
                  reason : Optional[str] = None,
                  label_rect : list[int, int, int, int] = (10, 10, 10, 10),
                  label_name : Optional[str] = 'centerLabel',
                  # button
                  button_text: str = "",
                  button_rect : list[int, int, int, int] = (20, 20, 20, 20),
                  button_name : Optional[str] = 'button',
                  button_function : Callable = lambda : ...,
                  # all_qss
                  qss_with_child_qss: Optional[str] = None
                  ):
        self.setGeometry(QRect(x_pos, y_pos, width, height))

        if parent is not None:
            self.setParent(parent)

        if object_name is not None:
            self.setObjectName(object_name)

        if flags is not None:
            self.setWindowFlags(flags)

        if modal:
            self.setWindowModality(Qt.WindowModal)

        # 只要Reason为空，就说明是普通界面，但是我不希望这样
        if reason is not None:
            self.centerLabel.setWidget(self.baseWidget, *label_rect, object_name=label_name, label_text=reason)
            self.singleButton.setWidget(self.baseWidget, *button_rect,
                                        object_name=button_name,
                                        button_name=button_text,
                                        func=button_function)
            if qss_with_child_qss is not None:
                self.baseWidget.setStyleSheet(qss_with_child_qss)

# Conducting tests is a must.
def test1():
    test_app = QApplication(argv)
    test_ui = AnimationMessageBoxLog()
    test_ui.setWidget(parent=None,
                      x_pos=700,
                      y_pos=300,
                      width=800,
                      height=600,
                      object_name=None,
                      flags=Qt.CustomizeWindowHint,
                      )
    bg = QWidget(test_ui)
    bg.setObjectName('bg')
    bg.setStyleSheet("""background-color : grey;border-radius : 20px;""")
    bg.setGeometry(QRect(10, 10, 100, 100))
    test_ui.setEdgeShadow(bg, [0, 0], 50, Qt.blue)
    test_ui.setAnimation(_type='geometry',
                         target=bg,
                         start=QRect(10, 10, 100, 100),
                         end=QRect(600, 450, 100, 50),
                         duration=2500)
    test_ui.show()
    exit(test_app.exec())

def test2():
    test_app = QApplication(argv)
    test_ui = AssembleAnimationMessageBoxLog_SingleButton()
    qss = """
                      #centerLabel {
                        background-color :tan;
                        border-radius : 29px;
                      }"""
    reason = '<p style="color : gold;font-size : 18px;>您尚未选择精灵哦!</p>'
    test_ui.setWidget(parent=None,
                      x_pos=400,
                      y_pos=200,
                      width=420,
                      height=500,
                      reason=reason,
                      qss_with_child_qss=qss,
                      label_rect=[10, 10, 400, 400],
                      flags=Qt.CustomizeWindowHint,
                      button_text='确认',
                      button_rect=[10, 420, 400, 50],
                      )
    test_ui.show()
    exit(test_app.exec())

if __name__ == '__main__':
    test2()
