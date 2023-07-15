# 本地化精灵天赋系统

- 源于精灵游戏《热血精灵派》，对UI以及相关功能的仿制
- 写作目的是练练英语，顺便本地化养养自己喜爱的精灵

## 项目使用的语言版本以及第三方库版本
```text
python == 3.9.12
PyQt5 == 5.15.9
```

# 项目结构

## CommonConst

### *这是一个存放全局变量的文件夹，或者说游戏配置*

- GlobalConstant文件下，我放置了大量的全局变量，这些变量在游戏的任何地方都可能会被用到

## CommonUtilWidgets

### *该文件夹封装了大量UI用到的控件，为了减少在核心UI的代码的臃肿，同时，也为了让代码层次分明*

- OptBar文件放置了进度条的封装
- OptBox文件放置了对QGroupBox的封装
- OptButton文件封装了普通按钮和切换按钮
- OptEdit有行输入框类
- OptLabel放置了QLabel的封装
- OptLog为了对话框的封装，目前放置了两个支持动画的类，一个是支持动画的控件，一个是在前者的基础，放置了一个展示区和一个按钮
- OptThread放置了封装的Qt线程和计时器
- OptWidget目前只有对QWidget的封装，我希望这里放置一些通用的基础类

## UI

### *正如其名，这里放置了核心UI布局，以及调用核心功能的调用*

- talent_ui文件，天赋系统UI
- talent.qss，相关UI对应的qss美化文件，我希望放置在同级目前，而不是资源文件中

## util

### *核心功能函数与数据解析的工具包*
- _XUtil文件目前放置了精灵天赋改造的功能函数
- AbstractObject文件里面的AbstractPortImplement是抽象类的实现，每个Object类应该继承它
- PetObject文件放置了处理精灵yaml文件获取精灵信息的PetAttr类
- UserObject文件放置了处理用户yaml文件获取用户信息的UserAttr类
- XUtil文件提供了快捷的用户和精灵天赋的工具类

## 资源结构
- pets文件夹放置了与精灵相关的gif图片
- PetsInfomation文件夹放置了精灵信息文件与对应的yaml文件格式
- UserInfomation文件夹放置了用户信息文件与对应的yaml文件格式
- test_pet_info是测试输出精灵的路径
- test_user_info是测试输出用户的路径
- resource文件夹放置了UI展示相关的资源文件

## 未考虑的几点bugs或者不足，希望后来者加油，日后我可能还会写写
- - 保存或者取消按钮还没有点击，就关闭天赋系统
- - 四个按钮，导入时，发生图标替换，再点击带图标的按钮，写一个检测是新打开文件还是选择当前精灵，建议用双击按钮事件
- 一个明显的不足 ：没有完全实现UI和功能分离
- 一个好看的加载动态界面
- VIP每天免费一次功能没写，需要在yml文件添加新属性和相关代码
- 变化值的进度条可以再优化——比如说根据正负值设置不同的条qss
 
## 灵感也有致谢
- Dart的设计思想
- 声明式编程的思想（虽然从项目代码中很少能看到他们的身影）
- 一位神秘人介绍给我的通俗易懂OOP思想以及他对我某块代码的指正
- 同样的，还有函数式编程的优势
- actionscript（虽然老，但是我在某个游戏的源代码看到的）的优美写法，哦不对，应该是致谢写这个游戏的Coders
- 同样的，感谢土木工程这个专业，让我深悟先建立框架，然后精装修的思想。土木工程真是太酷啦！

## 视频展示  
### 请查看show_example文件夹下的视频