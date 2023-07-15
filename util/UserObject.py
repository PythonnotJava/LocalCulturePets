# Process user's information.
from typing import Union
from yaml import FullLoader, load as yaml_load, dump as yaml_dump
from os import PathLike
from util.AbstractObject import AbstractPortImplement

class UserAttr(AbstractPortImplement):

    __slots__ = ['gold', 'name', 'money', 'date', '__version', '__attention']

    def __init__(self):
        super().__init__()
        # name of user
        self.name : str = ''
        # gold counts of user
        self.gold : int = 0
        # game currency counts of user
        self.money : int = 0
        # registration date of user
        self.date: str = ''
        # others
        self.__version : float = 1.0
        self.__attention : str = 'attention'

    def ReadObjectFile(self, path : Union[str, PathLike[str]], encoding : str = 'U8') -> None:
        _file = open(path, 'r', encoding=encoding)
        data = yaml_load(_file.read(), FullLoader)
        _file.close()
        self.name = data['name']
        self.gold = data['gold']
        self.money = data['money']
        self.date = data['date']
        self.__attention = data['attention']
        self.__version = data['version']

    def VisibleInfo(self):
        print(f'玩家名字：{self.name}\n'
              f'注册日期：{self.date}\n'
              f'金币：{self.gold}\n'
              f'游戏币：{self.money}')

    def __iter__(self):
        yield 'version', self.__version
        yield 'attention', self.__attention
        yield 'name', self.name
        yield 'gold', self.gold
        yield 'money', self.money
        yield 'date', self.date

    @staticmethod
    def WriteBackObjectFile(data : dict, path: Union[str, PathLike[str]], encoding: str = 'U8') -> None:
        with open(path, 'w', encoding=encoding) as _f:
            yaml_dump(data, _f)

__all__ = ['UserAttr']

if __name__ == '__main__':
    test_user = UserAttr()
    test_user.ReadObjectFile('../UserInfomation/user1.yml')
    test_user.VisibleInfo()
    test_user.WriteBackObjectFile(dict(test_user), '../UserInfomation/user2.yml')