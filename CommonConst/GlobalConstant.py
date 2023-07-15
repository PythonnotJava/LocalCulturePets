# I place global constants here
from pathlib import Path

path = Path(__file__).parent

CLOSE_BUTTON_IMG = (path / "../" / "resource" / "close.svg").__str__()
TALENT_CURRENT_ELF = (path / "../" / "resource" / "frames.gif").__str__()
CONFIRM_CHANGE_CURRENT_ELF_TALENT = (path / "../" / "resource" / "confirm.png").__str__()
ELF_GRID_IN_BAG = (path / "../" / "resource" / "big_grid.png").__str__()
TALENT_TITLE_IMG = (path / "../" / "resource" / "title.png").__str__()

TEST_TALENT_CURRENT_ELF_NAME = 'LV：100 御神•月盈武皇'
TIP_ORDINARY_REMODELING = "花费10000金币进行普通改造，\n每次改造概率成功"
TIP_HIGH_LEVEL_REMODELING = '花费10游戏币进行高级改造，\n每次改造必定成功'
ORIGINAL_TALENT_CHANGE_COST = 10000
HIGH_LEVEL_TALENT_CHANGE_COST = 10
TIP_VIP_WELFARE = '• VIP用户每天可以享受一次免费的高级改造哦'
ELF_ATTRIBUTES = ['物攻', '物防', '魔攻', '魔防', '超攻', '超防', '生命', '速度']
ELF_STARS_COLORS = ['white', 'white', 'green', 'blue', 'purple', 'gold', 'red']
COMMON_TIP_QSS = '''
QToolTip {
    color : red;
    border : 2px solid white;
    border-radius:5px;
    font-size : 18px;
    font-weight : bold;
    font-family : 黑体;
    background-color : lightskyblue;
}
'''

ELF_TYPES = {
    0 : '未知',
    1 : '光',
    2 : '暗',
    3 : '水',
    4 : '火',
    5 : '电',
}

TALENT_STAR_DISTANCE_SHOW = '''
                                   <p style="font-size : 16px;font-weight:bold;color : gold;">
                                        天赋星级：
                                        <span style="color: {};">
                                            {}
                                        </span>
                                   </p>
                                   <p style="font-size : 14px;color : white;font-family:黑体">
                                        总天赋值：
                                        <span style="color:gold;">
                                            {}
                                        </span>
                                            ，离升星还差：
                                        <span style="color:gold;">
                                            {}
                                        </span>
                                   </p>
                                   '''

ELF_SKILLS = ['普攻', '超攻', '觉醒技', '援护技']
MAX_SINGLE_TALENT_ATTR_VALUE = 200
MIN_SINGLE_TALENT_ATTR_VALUE = 0

PETS_CODEX = [(path / "../" / "PetsInfomation" / f"{_}.yml").__str__() for _ in range(1, 11)]

# attention : the ⭐'s background-color is yellow, it has default but fixed color that I can't change it by qss or css.
# However, I'm pretty fond of '⭐', case its cuteness indeed
# '⛤' can be beautified by qss or css, but its sharp corner and small appearance make it look quite ugly.
# yeah, I would like to use english here
STAR_STYLES = ['⛤⛤⛤⛤⛤⛤', '⭐⭐⭐⭐⭐⭐']


GAME_ICO = (path / "../" / "resource" / "logo.png").__str__()

TEST_USER_INFO = (path / "../" / "UserInfomation" / "user1.yml").__str__()

CURRENT_TASK_STATUS = {
    1 : '您的金币不够用哦',
    2 : '您的游戏币不够用哦',
    3 : '恭喜完成任务',
    4 : '您尚未选择精灵哦',
    5 : '您无法进行其他操作哦',
    6 : '每项属性值最高为200哦',

    10 : '状态验证-新写入',
    11 : '状态验证-在读',
    12 : '状态验证-替换',
    13 : '用户连接失败',
    14 : '存档成功',

    21 : '知道了',
    22 : '等一下',
    23 : '出发吧'
}


