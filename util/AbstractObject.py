# Base Abstract Object
# Declare some common interfaces here.
from os import PathLike
from typing import Union
from yaml import dump as yaml_dump
class AbstractPortImplement(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        ...

    # Object self can be converted to a dict object
    def __iter__(self):
        yield from ...

    # read relevant yaml file and reinitialize
    def ReadObjectFile(self, path : Union[str, PathLike[str]], encoding : str = 'U8') -> None:
        ...

    # save modified datas to the relevant file which read by Function-ReadObjectFile
    @staticmethod
    def WriteBackObjectFile(data: dict, path: Union[str, PathLike[str]], encoding: str = 'U8'):
        with open(path, 'w', encoding=encoding) as _f:
            yaml_dump(data, _f)
        _f.close()

    # print visible datas
    def VisibleInfo(self):
        ...

    # modify an item's values
    def ModifyOneItem(self, item, alterationValue):
        ...
