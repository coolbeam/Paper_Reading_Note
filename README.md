# my_paper_reading


```
python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py
```

### Demo
目前的初步效果是这样的
![a](./data/images/demo_sample.png) 
 
目前基础功能基本完成了, 能够:
- markdown记录笔记, 截图粘贴的图片会保存在`./data/images`下面, 笔记的文字内容会保存在`./data/data.pkl`下面
- 服务器同步, 目前没有服务器同步, 我是在github开了一个私有的project,通过github进行同步
- 欢迎提出关于需要什么样功能的建议
 
 
 ### 记录一下todo
 - [ ] 软件的第三页做成一个计划安排的贴纸, 正好分了5份, 对应周一到周五, 也许是得7份吧, 对应一周7天, 加一个列表, 展示之前的,每个周的安排, 选一个周就载入到笔记页面中. 
 最右边再做一个markdown展示窗口, 选中哪个窗口, 就显示哪个窗口的markdown信息?
 - [ ] 自定义边框，默认的顶部window太难看了，参考： [pyqt-custom-titlebar-window](https://github.com/yjg30737/pyqt-custom-titlebar-window)
 - [ ] 写年份，写出处的时候希望能弹个文本补全出来
 - [ ] 一些快捷键设置，如：ctrl+s保存啊，等等，也得加入到设置页面里面，虽然设置页面还没开始做
 - [ ] 在设置里面换theme，现在有light和dark但还没有设置页面
 - [ ] 换一批图标？看 [qtawesome](https://github.com/spyder-ide/qtawesome) 里面的图标 ``qta-browser``进行查看
 - [ ] 一些markdown的快捷键，如ctrl+b得到加粗字体，ctrl+I 自动换行加tab折叠对齐等
 - [ ] markdown编辑器中高亮一些标签
 - [ ] editor和previewer中字体修改等等
 - [ ] 自动化根据所有paper的pdf链接下载pdf到本地的某个文件夹下，并且item给上图标表明有无本地pdf
 - [ ] 隔一定的时间间隔自动保存数据？加了一个保存按钮,后面链接到ctrl+s
 - [ ] 列表中的搜索功能还没做呢,搜索栏里面,文字框没有文字的时候显示搜索,搜索选项选择为标签的时候,文字框变为不可写,
 然后,空的时候就显示请编辑选择标签.然后按编辑标签按钮得到标签,并输出到文字框里面,
 - [ ] markdown公式支持,试试这个: [https://github.com/mikidown/mikidown](https://github.com/mikidown/mikidown) ,[https://facelessuser.github.io/pymdown-extensions/](https://facelessuser.github.io/pymdown-extensions/)
 - [ ] 快捷的加字体颜色控制,<font color=#008000>绿色</font>, 加上一些编辑按钮,比如字体粗等等, 
 目前写了个快捷键ctrl+q来加颜色,后面做一个颜色选取的界面设置这个快捷键产出的默认颜色.
 - [ ] 标签选择的界面字体可能得大一点方便一点
 是不是可以像latex一样用\textcolor{red}{text}? 得加上输入候选?
 - [x] 每次打开都打开之前最后修改的那份笔记
 - [x] list里面的那个paper图标好像没啥用看不出来啥东西，看看能不能搞别的事儿,干脆弄阅读进度条吧
 - [x] treeview里面现在是三列：年份，出处，title，增加了一列`修改时间`,并默认按照修改时间排序
 - [x] 窗口得搞个图标好看点，名字也得改改？不然窗口就叫python？
 - [x] 程序关闭的时候要有个弹窗问是最小化还是关掉（还是不问了利索一点），先保存数据和设置
 - [x] 开局要load之前的设置和数据
 - [x] markdown编辑，复制粘贴图片
 - [x] 设置标签，给每个note设置标签，方便后面搜索，或者根据标签生成汇总页，可以参考微信电脑版，添加朋友的时候给朋友添加标签的页面，
 - [x] 添加一下status对一些动作进行说明，比如添加note的时候有重复title，或者已经存在空note，比如一些按钮的功能 
 - [x] 发现一个bug，好像用这个preview里面的链接点击打开的pdf网页，在关掉的时候会让浏览器崩掉，小心一点，应该不影响使用
 - [x] 设置类似于qq的VIP，就是有些note的标题颜色改变？具有标签`收藏`的note在list里面显示为红色,当然去掉该标签以后也就恢复了
 
 
## Thanks
 - [学习demo: PyQt](https://github.com/amikey/PyQt)
 - [学习demo: PyQTDemo](https://github.com/bigdot123456/PyQTDemo) 
 - [学习demo: pyqt5-demo](https://github.com/mach8686devops/pyqt5-demo)
 - [学习demo: CustomWidgets](https://github.com/PyQt5/CustomWidgets) 这里面有相关无边框的设计,这个的demo感觉很不错
 - [学习demo: PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
 - [主题UI：PyQtDarkTheme](https://github.com/5yutan5/PyQtDarkTheme), python -m qdarktheme.widget_gallery
 <br>目前整个框架都是基于PyQtDarkTheme来搞的
 - [读取md文件并进行markdown展示:QMarkdownPreviewer](https://github.com/Patitotective/QMarkdownPreviewer)
 - [markdown编辑和展示展示:pymarkview](https://github.com/0ip/pymarkview)
 - [编辑和展示html:PythonHTMLEditor](https://github.com/laurensnol/PythonHTMLEditor)

