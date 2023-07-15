import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from CommonConst import (TALENT_TITLE_IMG,
                        CLOSE_BUTTON_IMG,
                        TALENT_STAR_DISTANCE_SHOW,
                        TIP_VIP_WELFARE,
                        TIP_ORDINARY_REMODELING,
                        TIP_HIGH_LEVEL_REMODELING,
                        ELF_STARS_COLORS,
                        ELF_ATTRIBUTES,
                        ELF_GRID_IN_BAG,
                        STAR_STYLES,
                        TEST_USER_INFO,
                        GAME_ICO,
                        CURRENT_TASK_STATUS
                         )
from CommonUtilWidgets import *
from util.PetObject import PetAttr
from util.XUtil import PetTalentCoreXUtil, UserCoreXUtil
from typing import Optional, overload

class _Label(Label): ...

class _ProgressBar_origianl(ProgressBar): ...

class _ProgressBar_new(ProgressBar): ...

class _ProgressBar_change(ProgressBar): ...

class GridPushButton(PushButton):

    def __init__(self):
        super().__init__()

    def openPetYamlFile(self) -> tuple[PetAttr, str] or tuple[None, None]:
        fileName, fileType = QFileDialog.getOpenFileName(self, '打开精灵信息文件', '../',
                                                         '精灵的yaml标准源文件(*.yaml;*.yml)')
        # print(fileName)
        try:
            assert fileName == ''
            return None, None
        except AssertionError:
            _info = PetAttr()
            _info.ReadObjectFile(fileName)
            return _info, fileName

class Talent_UI(QDialog):
    # UI建立之前，就应该有一个用户在运行
    UserCore : Optional[UserCoreXUtil] = None

    @overload
    def __new__(cls, *args, **kwargs):
        ...
    @overload
    def __new__(cls, _userCore : Optional[UserCoreXUtil] = None, *args, **kwargs):
        ...
    def __new__(cls, _userCore: Optional[UserCoreXUtil] = None, *args, **kwargs):
        _ = super().__new__(cls, *args, **kwargs)
        if _userCore is not None:
            cls.UserCore = _userCore
        return _

    @classmethod
    def setUser(cls, _userCore: Optional[UserCoreXUtil] = None, *args, **kwargs):
        return cls.__new__(cls, _userCore=_userCore, *args, **kwargs)

    def __init__(self):
        super().__init__()
        # 核心控件
        # 关闭按钮
        self.close_btn = PushButton()
        # 标题
        self.title_label = Label()
        # 精灵改造区
        self.elf_show = GroupBox()
        # 精灵背包
        self.elf_bags_area = GroupBox()

        # 界面初始化
        self.setUI()
        self.setStyleSheet(open('talent.qss', 'r', encoding='U8').read())
        self.setWidgets()

        self.loading_label = QLabel(self)  # 加载提示或占位符界面
        self.loading_label.setStyleSheet('font-size : 72px;background-color : red;')
        self.loading_label.setText("玩命加载中……")
        self.loading_label.setGeometry(QRect(0, 0, 1000, 550))

        self.qss_loader_to_solve_delay = Loader('talent.qss')
        self.qss_loader_to_solve_delay.load_suc.connect(self.setQss)
        self.qss_loader_to_solve_delay.start()

        # UI上选择改造模式, True代表普通改造，反之
        self.marker: bool = True
        # 已经导入精灵文件和当前导入的精灵文件
        # 考虑到 ： 在导入前提下，如果重复导入同一个精灵文件，使用之前的数据，如果新导入，则添加
        # load_files_and_relevant_datas, such as {"pet_yaml_file" : PetTalentCoreXUtil_example, ...}
        # 我希望的是，在天赋系统关闭之前，数据都放在内存，而不是存档，当天赋系统关闭，统一存档，这个功能链接在close函数上
        self.load_files_and_relevant_datas : dict[str : PetTalentCoreXUtil] = {}
        self.cur_file : Optional[str] = None

    def setUI(self):
        self.setFixedSize(QSize(1000, 550))
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setObjectName('main')

    def setWidgets(self):
        # 标题
        self.title_label.setWidget(self, 350, 2, 300, 45, 'title_label', False, '', True, TALENT_TITLE_IMG)

        # 关闭按钮
        self.close_btn.setWidget(self, 945, 0, 45, 45, 'close_btn', lambda: self.rewriteClose(), True, CLOSE_BUTTON_IMG, False)

        # 精灵改造区
        self.elf_show.setWidget(self, 150, 45, 825, 495, 'elf_show')

        # 精灵背包
        self.elf_bags_area.setWidget(self, 10, 45, 135, 495, 'elf_bags_area')

        # 精灵展示区
        talent_elf_area = Label()
        talent_elf_area.setWidget(self.elf_show, 25, 30, 250, 360, 'talent_elf_area')

        elf_name = Label()
        elf_name.setWidget(talent_elf_area, 5, 5, 240, 50, 'elf_name', False)

        # 改变天赋系统区域
        talent_change_area = Label()
        talent_change_area.setWidget(self.elf_show, 285, 30, 500, 300, 'talent_change_area')

        # 用于显示当前精灵的星级
        current_elf_star = Label()
        current_elf_star.setWidget(self.elf_show, 25, 400, 250, 80, 'current_elf_star')

        # 改造核心按钮
        change_talent_two_buttons = BaseWidget()
        change_talent_two_buttons.setWidget(self.elf_show, 285, 345, 250, 90, 'change_talent_two_buttons')

        rdbt1 = ToggleButton()
        rdbt2 = ToggleButton()
        rdbt1_type1 = Label()
        rdbt2_type2 = Label()

        rdbt1.setWidget(change_talent_two_buttons, 5, 5, 30, 35, 'rdbt1', tip_content=TIP_ORDINARY_REMODELING)
        rdbt2.setWidget(change_talent_two_buttons, 5, 50, 30, 35, 'rdbt2', tip_content=TIP_HIGH_LEVEL_REMODELING)
        rdbt1.setChecked(True)

        rdbt1_type1.setWidget(change_talent_two_buttons, 40, 5, 200, 35, 'rdbt1_type1',
                              label_text='普通改造(<span style="color : gold;">10000🪙</span>)')
        rdbt2_type2.setWidget(change_talent_two_buttons, 40, 50, 200, 35, 'rdbt2_type2',
                              label_text='高级改造(<span style="color : blue;">10🧆</span>)')
        rdbt1.clicked.connect(lambda : self.toggleSignal(1))
        rdbt2.clicked.connect(lambda : self.toggleSignal(2))

        # 天赋改造的核心函数
        def confirmTalentChange(which_button_clicked : int):
            # 天赋改造
            if which_button_clicked == 1:
                # 考虑报错——先检查有没有连接用户，然后检测有没有选择精灵
                if self.UserCore is None:
                    self.statusPopUpLog(True, CURRENT_TASK_STATUS[13], CURRENT_TASK_STATUS[21])
                elif self.cur_file is None:
                    self.statusPopUpLog(True, CURRENT_TASK_STATUS[4], CURRENT_TASK_STATUS[21])
                # 这时候说明你已经导入精灵文件了
                # 整理下即将要做的逻辑
                # 1.判断使用普通改造还是高级改造--self.marker
                # 2.按钮变换
                # 3.保存下：当前星级区数值变化、进度条变化、两个lineEdit要变化
                # 4.取消时，进度条、两个lineEdit回到原来的
                # 5.最最最重要的，一定要实现：保存和取消按钮出现时，千万不能打开新的精灵文件，不然会乱写
                # 为了解决此bug，而且不给自己找麻烦，我决定此期间禁用导入按钮
                else:
                    # 用户数据改造
                    # 当前在读数据
                    currentPetTalentCoreXUtil : PetTalentCoreXUtil = self.load_files_and_relevant_datas[self.cur_file]
                    print('本次改造前数据', currentPetTalentCoreXUtil.current_list_mirror)
                    # 获取状态码
                    print('self.marker', self.marker)
                    statusCode = currentPetTalentCoreXUtil.costByRelevantCurrencyAndCheckIt(self.UserCore, mode=self.marker)
                    # 资源不够或者没有连接用户
                    if statusCode != 3:
                        self.statusPopUpLog(True, CURRENT_TASK_STATUS[statusCode], CURRENT_TASK_STATUS[21])
                    # 够用才能显示下一步——保存还是取消
                    else:
                        confirm_change_talent.hide()
                        save_change.show()
                        cancel_change.show()
                        for btn in grids_put_elf_head_pictures:
                            btn : GridPushButton
                            btn.setEnabled(False)
                            btn.setToolTip(CURRENT_TASK_STATUS[5])
                        # 总属性变化
                        total_talent_values_line.setText(sum(currentPetTalentCoreXUtil.new_list).__str__())
                        total_talent_values_change_line.setText(str(sum(currentPetTalentCoreXUtil.change_list)))
                        # 进度条变化
                        print('currentPetTalentCoreXUtil.change_list', currentPetTalentCoreXUtil.change_list)
                        for i in range(8):
                            attrs_original_progressbars[i].setValue(currentPetTalentCoreXUtil.current_list[i])
                            attrs_new_progressbars[i].setValue(currentPetTalentCoreXUtil.new_list[i])
                            attrs_change_progressbars[i].setValue(currentPetTalentCoreXUtil.change_list[i])
                            print('currentPetTalentCoreXUtil.change_list[i]', currentPetTalentCoreXUtil.change_list[i])
            # 保存
            elif which_button_clicked == 2:
                currentPetTalentCoreXUtil: PetTalentCoreXUtil = self.load_files_and_relevant_datas[self.cur_file]
                currentPetTalentCoreXUtil.save(True)
                print('保存了本次改造', currentPetTalentCoreXUtil.current_list)
                confirm_change_talent.show()
                save_change.hide()
                cancel_change.hide()
                for btn in grids_put_elf_head_pictures:
                    btn: GridPushButton
                    btn.setEnabled(True)
                    btn.setToolTip(CURRENT_TASK_STATUS[5])

                # 总属性变化
                total_talent_values_change_line.setText('-')
                # 进度条变化
                for i in range(8):
                    attrs_original_progressbars[i].setValue(currentPetTalentCoreXUtil.current_list[i])
                    attrs_new_progressbars[i].setValue(0)
                    attrs_change_progressbars[i].setValue(0)
                # 星级区变化
                _star: int
                _distance: int
                _stars: str
                _color: str
                _star, _distance = currentPetTalentCoreXUtil.reWriteJudgeElfStarAndDistance()
                print('_star, _distance', _star, _distance)
                if _star != 0:
                    _stars = STAR_STYLES[0][0: _star]
                    _color = ELF_STARS_COLORS[_star]
                else:
                    _stars = '无星级'
                    _color = ELF_STARS_COLORS[0]
                current_elf_star.setText(TALENT_STAR_DISTANCE_SHOW.format(_color, _stars, sum(currentPetTalentCoreXUtil.current_list), _distance))

            # 取消
            elif which_button_clicked == 3:
                currentPetTalentCoreXUtil: PetTalentCoreXUtil = self.load_files_and_relevant_datas[self.cur_file]
                currentPetTalentCoreXUtil.save(False)
                print('取消了本次改造', currentPetTalentCoreXUtil.current_list)
                confirm_change_talent.show()
                save_change.hide()
                cancel_change.hide()
                for btn in grids_put_elf_head_pictures:
                    btn: GridPushButton
                    btn.setEnabled(True)
                    btn.setToolTip(CURRENT_TASK_STATUS[5])
                # 总属性变化
                total_talent_values_line.setText(sum(currentPetTalentCoreXUtil.current_list).__str__())
                total_talent_values_change_line.setText('-')
                # 进度条变化
                for i in range(8):
                    attrs_original_progressbars[i].setValue(currentPetTalentCoreXUtil.current_list[i])
                    attrs_new_progressbars[i].setValue(0)
                    attrs_change_progressbars[i].setValue(0)
            else : ...

        # 确认天赋改造
        confirm_change_talent = PushButton()
        confirm_change_talent.setWidget(self.elf_show, 550, 370, 200, 45, 'confirm_change_talent',
                                        button_name='天 赋 改 造')
        confirm_change_talent.clicked.connect(lambda : confirmTalentChange(1))

        # 保存/不保存此处改造
        save_change = PushButton()
        cancel_change = PushButton()
        save_change.clicked.connect(lambda : confirmTalentChange(2))
        cancel_change.clicked.connect(lambda : confirmTalentChange(3))
        save_change.setWidget(self.elf_show, 550, 370, 100, 45, 'save_change', button_name='保存')
        cancel_change.setWidget(self.elf_show, 675, 370, 100, 45, 'cancel_change', button_name='取消')
        save_change.hide()
        cancel_change.hide()

        talent_tips = Label()
        talent_tips.setWidget(self.elf_show, 285, 470, 500, 30, 'talent_tips',
                              label_text=f'<p style="font-size : 16px; color : gold; font-weight : 900;background-color :#58568e;text-align:center;">{TIP_VIP_WELFARE}</p>')

        # 各类属性的统计可视化
        # 原属性
        original_attr = Label()
        original_attr.setWidget(talent_change_area, 100, 10, 75, 25, 'original_attr', label_text='原属性')

        # 新属性
        new_attr = Label()
        new_attr.setWidget(talent_change_area, 255, 10, 75, 25, 'new_attr', label_text='新属性')

        # 属性变化
        talent_change_show = Label()
        talent_change_show.setWidget(talent_change_area, 388, 10, 75, 25, 'talent_change_show', label_text='变化值')

        # 属性有哪些
        attrs_labels = []
        attrs_original_progressbars = []
        attrs_new_progressbars = []
        attrs_change_progressbars = []

        for each_attr in ELF_ATTRIBUTES:
            _index = ELF_ATTRIBUTES.index(each_attr)
            # label
            cur_attr = _Label()
            cur_attr.setWidget(talent_change_area, 15, 35 + _index * 25, 55, 25, None, label_text=each_attr)
            attrs_labels.append(cur_attr)

            # progressbar
            cur_origianl_attr_progress = _ProgressBar_origianl()
            cur_origianl_attr_progress.setWidget(talent_change_area, 70, 38 + _index * 25, 135, 20, current_value=0)
            attrs_original_progressbars.append(cur_origianl_attr_progress)

            cur_new_attr_progress = _ProgressBar_new()
            cur_new_attr_progress.setWidget(talent_change_area, 225, 38 + _index * 25, 135, 20, current_value=0)
            attrs_new_progressbars.append(cur_new_attr_progress)

            cur_attr_change = _ProgressBar_change()
            cur_attr_change.setWidget(talent_change_area, 380, 38 + _index * 25, 80, 20, min_num=-5, max_num=5, current_value=0)
            attrs_change_progressbars.append(cur_attr_change)

        # 总天赋值
        total_talent_values_label = Label()
        total_talent_values_label.setWidget(talent_change_area, 15, 245, 100, 35, 'total_talent_values_label',
                                            label_text='总天赋值 :', tip_content=CURRENT_TASK_STATUS[6])

        total_talent_values_line = LineEdit()
        total_talent_values_line.setWidget(talent_change_area, 120, 245, 100, 35, 'total_talent_values_line', True,
                                           True, text='-')
        # 总天赋值变化
        total_talent_values_change_label = Label()
        total_talent_values_change_label.setWidget(talent_change_area, 235, 245, 130, 35,
                                                   'total_talent_values_change_label', label_text='总天赋变化值 :')

        total_talent_values_change_line = LineEdit()
        total_talent_values_change_line.setWidget(talent_change_area, 370, 245, 90, 35,
                                                  'total_talent_values_change_line', True, True, text='-')

        # 背包里面放置格子
        # 这些格子是可以点击的
        grids_put_elf_head_pictures = []
        for each_grid_index in range(4):
            cur_grid = GridPushButton()
            cur_grid.setWidget(self.elf_bags_area, 15, 20 + each_grid_index * 115, 105, 105, use_icon=True,
                               icon_path=ELF_GRID_IN_BAG)

            def cur_grid_func():
                pet_info, fileName = cur_grid.openPetYamlFile()
                if pet_info is not None:
                    pet_info : PetAttr
                    fileName : str
                    # 如果没有读入此精灵文件
                    if fileName not in self.load_files_and_relevant_datas.keys():
                        self.cur_file = fileName
                        # 更新名字
                        elf_name.setText(f'LV：{pet_info.elf_level} {pet_info.elf_name}')
                        # 更新gif
                        # nonlocal movie
                        # del movie
                        movie = QMovie(pet_info.linked_gif)
                        talent_elf_area.setMovie(movie)
                        movie.start()
                        # 更新星级显示区
                        _star: int
                        _distance: int
                        _stars: str
                        _color: str
                        _star, _distance = pet_info.JudgeElfStarAndDistance()
                        if _star != 0:
                            _stars = STAR_STYLES[0][0: _star]
                            _color = ELF_STARS_COLORS[_star]
                        else:
                            _stars = '无星级'
                            _color = ELF_STARS_COLORS[0]
                        current_elf_star.setText(TALENT_STAR_DISTANCE_SHOW.format(_color, _stars, sum(pet_info.elf_attrs), _distance))
                        # 更新原有属性
                        _index = 0
                        for each_original_attr in pet_info.elf_attrs:
                            attrs_original_progressbars[_index].setValue(each_original_attr)
                            _index += 1
                        # 总天赋值变化
                        total_talent_values_line.setText(sum(pet_info.elf_attrs).__str__())
                        # 建立一个对应的PetTalentCoreXUtil并记录
                        _PetTalentCoreXUtil = PetTalentCoreXUtil(fileName)
                        # 注意：这里完全可以做一个优化，包括下面的else里面也是
                        # 当一个文件被读取时，额外创建一个记录对应文件是否被修改的变量，
                        # 这样，在关闭天赋系统时，如果检测精灵文件只被读取，那就不需要保存重写入了
                        # 反之，重写入；这样可节省性能
                        # 但是我不打算这么做
                        self.load_files_and_relevant_datas[fileName] = _PetTalentCoreXUtil
                        print('You load your pet {}.gif successfully! Now, you have loaded {} pets'
                              .format(pet_info.elf_seq, self.load_files_and_relevant_datas.__len__()))
                        print(CURRENT_TASK_STATUS[10])
                    # 如果已经读入此文件
                    # 如果当前文件是读入文件
                    else:
                        if self.cur_file == fileName :
                            print(CURRENT_TASK_STATUS[11])
                        # 如果不是，则调用已经读入（并且可能被修改数据）的精灵文件
                        else:
                            _ : PetTalentCoreXUtil = self.load_files_and_relevant_datas[fileName]
                            renew_pet_info_dict : dict = _.relevantPet_info
                            self.cur_file = fileName
                            # 更新名字
                            elf_name.setText('LV：{} {}'.format(renew_pet_info_dict['level'], renew_pet_info_dict['name']))
                            # 更新gif
                            movie = QMovie(_.relevantPet.linked_gif)
                            talent_elf_area.setMovie(movie)
                            movie.start()
                            # 更新星级显示区
                            _star: int
                            _distance: int
                            _stars: str
                            _color: str
                            _star, _distance = _.relevantPet.JudgeElfStarAndDistance()
                            if _star != 0:
                                _stars = STAR_STYLES[0][0: _star]
                                _color = ELF_STARS_COLORS[_star]
                            else:
                                _stars = '无星级'
                                _color = ELF_STARS_COLORS[0]
                            current_elf_star.setText(
                                TALENT_STAR_DISTANCE_SHOW.format(_color, _stars, sum(_.current_list), _distance))
                            # 更新原有属性
                            _index = 0
                            for each_original_attr in renew_pet_info_dict['talent_atrrs']:
                                attrs_original_progressbars[_index].setValue(each_original_attr)
                                _index += 1
                            # 总天赋值变化
                            total_talent_values_line.setText(sum(_.current_list).__str__())
                            print(CURRENT_TASK_STATUS[12])

            cur_grid.clicked.connect(cur_grid_func)
            grids_put_elf_head_pictures.append(cur_grid)

    def toggleSignal(self, which : int):
        if which == 1:
            self.marker = True
            print('Attention : 您选择了普通改造模式')
        elif which == 2:
            self.marker = False
            print('Attention : 您选择了高级改造模式')
        else : ...

    def setQss(self, qss: str):
        self.setStyleSheet(qss)
        self.loading_label.hide()

    # 状态类弹出
    def statusPopUpLog(self, if_show : bool, reason : str, btnStr : str):
        popUpBox = AssembleAnimationMessageBoxLog_SingleButton()
        # 这一步因为继承类的原因导致代码被写麻烦了
        popUpBox.setAnimation('geometry',
                              popUpBox.baseWidget,
                              QRect(300, -500, 400, 300),
                              QRect(300, 125, 400, 300),
                              250)
        popUpBox.setWidget(self, 0, 0, 1000, 550,
                           object_name='popUpBox',
                           # label
                           reason=reason,
                           label_rect=[50, 20, 300, 200],
                           # button
                           button_text=btnStr,
                           button_rect=[160, 240, 80, 50],
                           button_function=lambda: popUpBox.close(),
                           )
        popUpBox.setEdgeShadow(popUpBox.baseWidget, radius=50, color=Qt.darkBlue)
        if if_show : popUpBox.show()

    # 关闭时，保存精灵数据
    def rewriteClose(self):
        # 测试期间，还是把数据写到新路径
        # self.load_files_and_relevant_datas: dict[str: PetTalentCoreXUtil] = {}
        # 如果想实现真正的功能，即原路写回，建议在__new__传入一个bool?（bool?代表bool或者空值，我只能说我的设计思想源于Dart）变量，如下
        # def __new__(cls,
        #     _userCore: Optional[UserCoreXUtil] = None,
        #     allowWriteBack : Optional[bool] = True,
        #     *args, **kwargs): ...
        if self.UserCore is not None:
            print('write back your data before close……')
            print(self.load_files_and_relevant_datas)
            _index = 1
            for currentPetTalentCoreXUtil in self.load_files_and_relevant_datas.values():
                path_pet = f"../test_pet_info/test_pet_info_{_index}.yml"
                currentPetTalentCoreXUtil: PetTalentCoreXUtil
                currentPetTalentCoreXUtil.writeBackFileStream(path_pet)
                print(f'has written in : {path_pet}')
                _index += 1
            path_user = "../test_user_info/test_user_info_1.yml"
            self.UserCore.writeBackFileStream(path_user)
            self.statusPopUpLog(True, CURRENT_TASK_STATUS[14], CURRENT_TASK_STATUS[21])
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap(GAME_ICO)))
    ui = Talent_UI()
    ui.setUser(UserCoreXUtil(TEST_USER_INFO))
    ui.show()
    sys.exit(app.exec())
