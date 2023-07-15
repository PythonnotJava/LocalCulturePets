# PetAttr is a class inherited from abstrat object and used to process elf's various information.
from typing import Union
from yaml import FullLoader, load as yaml_load, dump as yaml_dump
from os import PathLike
from CommonConst import ELF_ATTRIBUTES, ELF_TYPES, ELF_SKILLS
from util import AbstractPortImplement
from pathlib import Path

class PetAttr(AbstractPortImplement):
    __path = Path(__file__).parent
    __slots__ = ['elf_name', 'elf_attrs', 'elf_level', 'elf_type',
                 'elf_seq', 'cur_level_exp', 'elf_skills', 'linked_gif',
                 '__attention', '__version']

    def __init__(self, *args, **kwargs):
        # name of elf
        super().__init__(*args, **kwargs)
        self.elf_name: str = ''
        # list of elf's each attribute
        self.elf_attrs: list = []
        # level of elf
        self.elf_level: int = 1
        # type of elf
        self.elf_type: int = 0
        # sequence number of elf
        self.elf_seq: int = 9999
        # current experience of elf's current level
        self.cur_level_exp: int = 0
        # introductory list of elf skills
        self.elf_skills: list = []
        # relevant gif of elf
        self.linked_gif: str = ''
        # others
        self.__version: float = 1.0
        self.__attention: str = 'attention'

    def __iter__(self):
        keys = ['version', 'attention', 'name', 'level', 'type',
                'seqnum', 'exp', 'skills', 'talent_atrrs']
        values = [self.__version, self.__attention, self.elf_name,
                  self.elf_level, self.elf_type, self.elf_seq,
                  self.cur_level_exp, self.elf_skills, self.elf_attrs]
        yield from zip(keys, values)

    # read an elf yaml file
    def ReadObjectFile(self, path: Union[str, PathLike[str]], encoding: str = 'U8') -> None:
        _file = open(path, 'r', encoding=encoding)
        _data = _file.read()
        _file.close()
        data = yaml_load(_data, FullLoader)
        self.elf_level = data['level']
        for _ in range(8):
            self.elf_attrs.append(data['talent_atrrs'][_])
        self.elf_name = data['name']
        self.elf_seq = data['seqnum']
        self.elf_type = data['type']
        self.cur_level_exp = data['exp']
        for _ in range(4):
            self.elf_skills.append(data['skills'][_])
        self.linked_gif = (self.__path / "../" / "pets" / f"{self.elf_seq}.gif").__str__()

    def VisibleInfo(self) -> None:
        print(f"当前精灵名字 ：{self.elf_name}")
        print(f"精灵等级 ：{self.elf_level}")
        print("精灵的各项天赋 ：")
        sumAttrs = 0
        _index = 0
        for attr in ELF_ATTRIBUTES:
            print(f'\t> {attr} ：{self.elf_attrs[_index]}')
            sumAttrs += self.elf_attrs[_index]
            _index += 1
        stars = '⭐⭐⭐⭐⭐⭐'
        _curStar: int = self.JudgeElfStarAndDistance()[0]
        if _curStar == 0:
            print('星级 ：无')
        else:
            _ = ''.join(stars[: _curStar])
            print(f'星级 ：{_}')
        print(f'精灵类别：{ELF_TYPES[self.elf_type]}系')
        _index2 = 0
        for skill in self.elf_skills:
            if skill is not None:
                print(f'{ELF_SKILLS[_index2]}：{skill}')
            else:
                print(f'{ELF_SKILLS[_index2]}：无')
            _index2 += 1

    # By current talents, determine elf's star numbers and get the values of distance from next star.
    def JudgeElfStarAndDistance(self) -> tuple[int, int]:
        _values = sum(self.elf_attrs)
        if _values == 0:
            return 0, 100
        elif 0 < _values <= 100:
            return 1, 100 - _values
        elif 100 < _values <= 300:
            return 2, 300 - _values
        elif 300 < _values <= 500:
            return 3, 500 - _values
        elif 500 < _values <= 700:
            return 4, 700 - _values
        elif 700 < _values <= 800:
            return 5, 800 - _values
        elif 800 < _values <= 1600:
            return 6, 1600 - _values
        else:
            return 0, 0

    @staticmethod
    def WriteBackObjectFile(data: dict, path: Union[str, PathLike[str]], encoding: str = 'U8') -> None:
        with open(path, 'w', encoding=encoding) as _f:
            yaml_dump(data, _f)

__all__ = ['PetAttr']

# Conducting a test is a must.
if __name__ == '__main__':
    test_file = PetAttr()
    test_file.ReadObjectFile('../PetsInfomation/1.yml')
    test_file.WriteBackObjectFile(dict(test_file), '../PetsInfomation/5.yml')
    test_file.VisibleInfo()
