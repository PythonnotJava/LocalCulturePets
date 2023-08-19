# Core utility classes
from util import changeTalents, UserAttr, PetAttr
from os import PathLike
from typing import Union, Optional, Generator
from CommonConst import ORIGINAL_TALENT_CHANGE_COST, HIGH_LEVEL_TALENT_CHANGE_COST

# Implemente multiple elf datas for the same user, rather than each elf data for one user
# so, when the system is running, the user have had prepended.
class UserCoreXUtil(UserAttr):
    def __init__(self, userInfo_path: Union[str, PathLike[str]]):
        super().__init__()
        # connect a user
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
        # the counts of talents-modification
        self.successive_failures_talents_change_times : int = 0
        # connect an elf and get it's infomation
        self.relevantPet = PetAttr()
        self.petInfo_path = petInfo_path
        self.relevantPet.ReadObjectFile(petInfo_path)
        self.relevantPet_info : dict = dict(self.relevantPet)
        # current list of each talent attriibute
        # newly changed list of each talent attriibute
        # changed values of list of each talent attriibute
        # mirrors of three list above, used for recovery
        self.current_list : list = self.relevantPet_info['talent_atrrs']
        self.new_list = []
        self.change_list = []
        self.current_list_mirror : list = self.relevantPet_info['talent_atrrs']
        self.new_list_mirror = []
        self.change_list_mirror = []

        self.generatorToList : list = []

    # The function performance
    # 1.get ...
    # 2.optimize the algorithm named changeTalents(you can see its implementation in _XUtil.py)
    # - if using ordinary talent-modifacation, once the current fails, it will be counted,
    #   when counts equals 5, the talent-modifacation will succed next time.
    # 3.consider changed values which is equal 0 as success
    def __getComponent(self, mode: bool) -> None:
        _data: Generator = changeTalents(self.current_list, mode)
        print("Base on self.current_list --> ", self.current_list)
        # generatorToList is a list used to convert generator to list
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
        # ordinary talent-modification
        if mode:
            # if failure-counts is equal 5, next time talent-modification is sure to succed.
            if self.successive_failures_talents_change_times == 5:
                self.__getComponent(False)
                self.successive_failures_talents_change_times = 0
            else:
                self.__getComponent(True)
                # low the attribute
                if sum(self.change_list) < 0:
                    self.successive_failures_talents_change_times += 1
                else:
                    # if want to realize continuous talent-modification-next-time-lift, you can add this code below
                    # self.successive_failures_talents_change_times = 0
                    ...
        # high-level reconstruction
        else:
            self.__getComponent(False)

    # rewrite JudgeElfStarAndDistance
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

    # every modifocation needs money/gold
    # if succeds, reduce relevant counts
    # return status-code
    def costByRelevantCurrencyAndCheckIt(self,
                                         # connect the user
                                         userCoreXUtil : Optional[UserCoreXUtil] = None,
                                         mode : bool = True,
                                         cost1 : int = ORIGINAL_TALENT_CHANGE_COST,
                                         cost2 : int = HIGH_LEVEL_TALENT_CHANGE_COST
                                         ) -> int:
        # if connects a user
        if userCoreXUtil is not None:
            if mode:
                # if gold is enough
                if userCoreXUtil.gold >= cost1:
                    self.getComponent(True)
                    userCoreXUtil.ModifyOneItem('gold', -cost1)
                    # userCoreXUtil.gold -= cost1
                    return 3
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
    # save : if saved, renew the list
    # on condition that the status-code is equal 3
    def save(self, save : bool = True):
        if save:
            self.current_list_mirror = self.current_list
            self.current_list = self.new_list.copy()
        else:
            self.current_list = self.current_list_mirror.copy()
    def writeBackFileStream(self,
                            writeBackPath : Union[Optional[str], PathLike[str]] = None,
                            encoding: str = 'U8'):
        # original file(s) will be covered if not income path
        # Of course, we shouldn't income path indeed. It's just a test for incoming path to check if relevnt codes run.
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
