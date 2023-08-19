# 这里放置了核心功能
from util._XUtil import changeTalents
from util.UserObject import UserAttr
from os import PathLike
from typing import Union, Optional, Generator
from CommonConst.GlobalConstant import ORIGINAL_TALENT_CHANGE_COST, HIGH_LEVEL_TALENT_CHANGE_COST
from util.PetObject import PetAttr

# 实现多个精灵文件对应同一个用户，而不是每个精灵都对应一个用户
# 否则，会出现每个精灵单独读取用户资源而导致写入混乱问题
# 所以，每次精灵系统运作的时候，只能对应一个全局用户
class UserCoreXUtil(UserAttr):
    def __init__(self, userInfo_path: Union[str, PathLike[str]]):
        super().__init__()
        # 连接用户
        self.userInfo_path = userInfo_path
        self.ReadObjectFile(userInfo_path)

    # I hope that changing values instead of attributes like version numbers
    def ModifyOneItem(self, item, alteration):
        if item == 'gold':
            self.gold += alteration
        elif item == 'money':
            self.money += alteration
        else:
            ...
    # write back
    def writeBackFileStream(self,
                            writeBackPath: Union[Optional[str], PathLike[str]] = None,
                            encoding: str = 'U8'):
        self.WriteBackObjectFile(
            dict(self),
            writeBackPath if writeBackPath is not None else self.userInfo_path,
            encoding)

# Yeah, I didn't make this new class inherit from PetAttr
class PetTalentCoreXUtil:

    def __init__(self, petInfo_path : Union[str, PathLike[str]]):
        # 连续失败改造次数
        self.successive_failures_talents_change_times : int = 0
        # 连接精灵
        self.relevantPet = PetAttr()
        self.petInfo_path = petInfo_path
        self.relevantPet.ReadObjectFile(petInfo_path)
        self.relevantPet_info : dict = dict(self.relevantPet)
        # 当前的天赋值列表、新变化的天赋值列表、变化的天赋值列表
        # 当前的天赋值列表的镜像、新变化的天赋值列表的镜像、变化的天赋值列表的镜像，这三个是用于取消恢复
        self.current_list : list = self.relevantPet_info['talent_atrrs']
        self.new_list = []
        self.change_list = []
        self.current_list_mirror : list = self.relevantPet_info['talent_atrrs']
        self.new_list_mirror = []
        self.change_list_mirror = []

        self.generatorToList : list = []

    # 1.获取...
    # 2.在每次开启天赋系统时，有以下算法
    # - 每个精灵每5次降低必定在第六次提升，第六次指的是普通改造第六次
    # 3.视变化值为0时属于提升的情况
    def __getComponent(self, mode: bool) -> None:
        _data: Generator = changeTalents(self.current_list, mode)
        print("Base on self.current_list --> ", self.current_list)
        # generatorToList是用于存放每次生成器转换为列表的属性
        self.generatorToList = list(_data)
        self.current_list_mirror : list = self.current_list.copy()
        self.new_list_mirror = self.new_list.clear()
        self.change_list_mirror = self.change_list.copy()
        self.current_list.clear()
        self.new_list.clear()
        self.change_list.clear()
        each_change: tuple[int, int, int]
        print("Here is detailed datas-changing : ")
        for each_change in self.generatorToList:
            print(each_change)
            self.current_list.append(each_change[0])
            self.new_list.append(each_change[1])
            self.change_list.append(each_change[2])
            print('get each_change[2]', each_change[2])
        print('current_list', self.current_list)
        print('new_list', self.new_list)
        print('change_list', self.change_list)

    def getComponent(self, mode : bool) -> None:
        # 普通改造
        if mode:
            # 连续失败,但是概率比较小，于是选择每累计五次为准
            if self.successive_failures_talents_change_times == 5:
                self.__getComponent(False)
                self.successive_failures_talents_change_times = 0
            else:
                self.__getComponent(True)
                # 降低属性了
                if sum(self.change_list) < 0:
                    self.successive_failures_talents_change_times += 1
                else:
                    # 本来想写连续失败，但是概率比较小，于是选择每累计五次为准
                    # self.successive_failures_talents_change_times = 0
                    ...
        # 高级改造
        else:
            self.__getComponent(False)

    # 星级提升/降低功能还有下一个星级的距离
    def reWriteJudgeElfStarAndDistance(self) -> tuple[int, int]:
        _value = sum(self.current_list)
        if _value == 0:
            return 0, 100
        elif 0 < _value <= 100:
            return 1, 100 - _value
        elif 100 < _value <= 300:
            return 2, 300 - _value
        elif 300 < _value <= 500:
            return 3, 500 - _value
        elif 500 < _value <= 700:
            return 4, 700 - _value
        elif 700 < _value <= 800:
            return 5, 800 - _value
        elif 800 < _value <= 1600:
            return 6, 1600 - _value
        else:
            return 0, 0

    # 每次改造都需要花费
    # 这里处理花费问题
    # 使用哪种改造，就会对相关货币进行响应，mode参数为True表明采用普通改造
    # 返回包含状态码，请到全局变量查询
    def costByRelevantCurrencyAndCheckIt(self,
                                         # 连接用户
                                         userCoreXUtil : Optional[UserCoreXUtil] = None,
                                         mode : bool = True,
                                         cost1 : int = ORIGINAL_TALENT_CHANGE_COST,
                                         cost2 : int = HIGH_LEVEL_TALENT_CHANGE_COST
                                         ) -> int:
        # 连接用户前提下
        if userCoreXUtil is not None:
            if mode:
                # 钱够
                if userCoreXUtil.gold >= cost1:
                    self.getComponent(True)
                    userCoreXUtil.ModifyOneItem('gold', -cost1)
                    # userCoreXUtil.gold -= cost1
                    return 3
                # 钱不够
                else:
                    return 1
            else:
                if userCoreXUtil.money >= cost2:
                    self.getComponent(False)
                    userCoreXUtil.ModifyOneItem('money', -cost2)
                    # userCoreXUtil.money -= cost2
                    return 3
                else:
                    return 2
        else:
            return 13
    # save : 为True则保存，反之（保存或者取消保存按钮功能，UI思路是先因此天赋改造按钮，如何展现这两个按钮以及链接功能，切换来回）
    # 保存的情况下，原来的各个属性列表，会被新的属性列表代替
    # 前提是状态码为3
    def save(self, save : bool = True):
        if save:
            self.current_list_mirror = self.current_list
            self.current_list = self.new_list.copy()
        else:
            self.current_list = self.current_list_mirror.copy()

    # 把改造（被读入也算，这一步完全可以优化，请看核心UI的思路，虽然没实现）的精灵信息写回
    def writeBackFileStream(self,
                            writeBackPath : Union[Optional[str], PathLike[str]] = None,
                            encoding: str = 'U8'):
        # 不传新路径就覆盖，其实本来就是这样，传入新路径是测试用的
        self.relevantPet_info['talent_atrrs'] = self.current_list
        self.relevantPet.WriteBackObjectFile(self.relevantPet_info,
                                             writeBackPath if writeBackPath is not None else self.petInfo_path,
                                             encoding)

if __name__ == '__main__':
    test_user = UserCoreXUtil('../UserInfomation/user1.yml')
    test_file = PetTalentCoreXUtil('../PetsInfomation/1.yml')
    test_file2 = PetTalentCoreXUtil('../PetsInfomation/2.yml')
    cost = test_file.costByRelevantCurrencyAndCheckIt(test_user)
    cost2 = test_file2.costByRelevantCurrencyAndCheckIt(test_user, False)
    if cost == cost2 == 3:
        test_file.save()
        test_file2.save()
        test_file.writeBackFileStream('../PetsInfomation/xutil_test_file1.yml')
        test_file2.writeBackFileStream('../PetsInfomation/xutil_test_file2.yml')
        test_user.writeBackFileStream('../UserInfomation/xutil_test_user1.yml')
    else: print('Error Found!')
