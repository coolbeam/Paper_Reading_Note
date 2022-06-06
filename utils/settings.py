from utils.tools import tools
import os
import datetime
import shutil


# 使用绝对路径
class Settings(tools.abstract_config):
    def __init__(self, **kwargs):
        self.theme = "dark"  # "dark", light

        # ==== editor
        self.editor_font_family = 'Consolas'
        self.editor_font_size = 12
        self.editor_tab_width = 4
        self.editor_clip_image_quality = 50  # 0到100,0为最小文件大小，100为无压缩
        self.editor_markdown = 'markdown2'  # commonmark,markdown2

        # ==== file，后面可能会做根据pdf链接下载所有paper的功能
        self.download_pdf_dir = '/home'  # 暂时不用

        # ==== 列表排序方式
        self.list_sort_manner = 'reading_time'  # 排序方式，暂定：阅读时间顺序，paper出处、年份、标题
        self.list_font_size = 10

        # ===========
        self.update(kwargs)
        self.main_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        self.main_data_dir = os.path.join(self.main_dir, 'data')
        tools.check_dir(self.main_data_dir)
        self.image_save_dir = os.path.join(self.main_data_dir, 'images')  # save images
        tools.check_dir(self.image_save_dir)
        self.res_save_dir = os.path.join(self.main_data_dir, 'res')  # save images
        tools.check_dir(self.res_save_dir)
        self._update_ignore_keys = ['main_dir', 'main_data_dir', 'image_save_dir', 'res_save_dir']

    def save_settings(self):
        save_path = os.path.join(self.main_data_dir, 'settings.pkl')
        tools.pickle_saver.save_pickle(self.to_dict, save_path)

    def load_settings(self):
        save_path = os.path.join(self.main_data_dir, 'settings.pkl')
        if os.path.isfile(save_path):
            s = tools.pickle_saver.load_picke(save_path)
            self.update(s)

    @classmethod
    def demo(cls):
        s = Settings()
        print(s.to_dict)
        # s.save_settings()
        # s.load_settings()
        # print(s.to_dict)


defaut_paper_title = '无标题'
defaut_paper_text = '''
## 总结

## Motivation

## Method

'''


class Paper_Sample(tools.abstract_config):
    def __init__(self, **kwargs):
        # ==== 笔记信息
        self.text = defaut_paper_text  # 笔记内容
        self.image_ls = []  # 图片路径存储
        self.tags = []  # 技术点标签，待定,或者主题标签，类似于光流，分割等
        self.reading_date = None  # 最开始阅读的时间
        self.modify_date = None  # 最近修改的时间
        self.data_index = ''  # 用来记录在paper data里面的坐标

        # ===== 论文信息
        self.title = defaut_paper_title  # 添加新论文笔记的时候要搜索一遍标题(小写以后进行对比)
        self.years = ''  # 年份, int
        self.produce = ''  # 论文出处,str
        self.readind_progress = '1%'  # 阅读进度："1%", "20%", "50%", "80%", "99%"
        # self.auther_ls = []  # 作者，可能记录不太方便, 暂时不用
        self.pdf_url = ''  # pdf 下载链接，str，后面可能使用自动下载，下载pdf的时候要注意文件名中不能有冒号
        self.code_url = ''  # 代码链接，有就链接，无就是空的
        self.update(kwargs)

    def new_image_name(self):
        print('新建保存图片')
        print(self.to_dict)
        a = datetime.datetime.now()
        a_str = a.strftime("%Y_%m_%d_%H_%M_%S")
        im_name = 'id%s_n%s_%s.jpg' % (self.data_index, len(self.image_ls), a_str)
        print('图片名：', im_name)
        print('')
        return im_name

    def make_markdown_text(self):
        # 判断一些情况
        if self.text == '':
            note_text = '无笔记内容'
        else:
            note_text = self.text
        if self.title == '':
            title = '无论文标题'
        else:
            title = self.title
        if self.years == '':
            year = '无论文时间'
        else:
            year = self.years
        if self.produce == '':
            produ = '无论文出处'
        else:
            produ = self.produce
        if self.code_url == '':
            code = '无代码链接'
        else:
            code = 'code'
        if self.pdf_url == '':
            pdf = '无pdf链接'
        else:
            pdf = 'pdf'
        if len(self.tags) == 0:
            tags_str = '无标签'
        else:
            tags_str = '标签: '
            for i in self.tags:
                tags_str += '`%s` ' % i

        md_text = """ %s
===
`%s`, `%s`, `阅读进度:%s` 
[%s](%s), [%s](%s)<br>%s

---

%s
""" % (title, year, produ, self.readind_progress, code, self.code_url, pdf, self.pdf_url, tags_str, note_text)
        # 组织markdown的text

        return md_text


class Paper_Data():
    def __init__(self, settings: Settings):
        self.conf = settings
        self.data_ls = {}
        self.title_low_ls = []
        self.years_ls = []
        self.produce_ls = []
        self.all_tags = []

    def save(self):
        save_path = os.path.join(self.conf.main_data_dir, 'data.pkl')
        tools.pickle_saver.save_pickle(self, save_path)

    def load(self):
        save_path = os.path.join(self.conf.main_data_dir, 'data.pkl')
        if os.path.isfile(save_path):
            s = tools.pickle_saver.load_picke(save_path)
            self.data_ls = s.data_ls
        if len(self) == 0:
            self.new_paper_note()
        self.update_static_ls()

    def keys(self):
        return list(self.data_ls.keys())

    def __len__(self):
        return len(self.data_ls.keys())

    def __getitem__(self, item):
        return self.data_ls[item]

    def __contains__(self, item):
        if item in self.data_ls.keys():
            return True
        else:
            return False

    def fetch(self, index_key=''):
        if index_key in self.keys():
            return self.data_ls[index_key]
        else:
            raise ValueError('wrong index key for: %s' % index_key)

    def serach_for_title(self, title: str):
        for i in self.keys():
            if title.lower() == self[i].title.lower():
                return True, self[i], i
        return False, None, None

    def new_paper_note(self):
        # 先查找一遍，如果已经存在有新笔记(标题=无标题),那么就载入那个
        for i_k in self.keys():
            p_item = self[i_k]
            if p_item.title == '无标题' and p_item.text == '笔记内容':
                return p_item, i_k
        N = len(self.keys())
        new_k = '%s' % N
        if new_k in self.keys():
            new_k = '%s_' % N
        paper_note = Paper_Sample(reading_date=datetime.datetime.now())
        paper_note.data_index = new_k
        paper_note.modify_date = datetime.datetime.now()
        self.data_ls[new_k] = paper_note
        return paper_note, new_k

    # check paper笔记里面的图片，如果有的文件没有在note里面就把图片删了节省空间
    def check_paper_sample_image(self, paper_sample: Paper_Sample):
        def get_local_markdown_img_namess(text):
            lines = text.splitlines()
            d_ls = []
            for item in lines:
                if '![' in item:
                    s1 = item.split('![')[1]
                    if '](' in s1:
                        s2 = s1.split('](')[1]
                        if ')' in s2:
                            img_path = s2.split(')')[0]
                            if img_path.endswith('.png') or img_path.endswith('.jpg'):
                                img_name = os.path.basename(img_path)
                                d_ls.append(img_name)
            return d_ls

        new_image_ls = []
        temp_ls = ['temp.png', 'temp1.png', 'temp2.png', 'defaut_paper_ico.jpg']
        img_ls_in_text = get_local_markdown_img_namess(paper_sample.text)
        # print('image_ls', paper_sample.image_ls)
        # print('img_ls_in_text', img_ls_in_text)
        for im_name in paper_sample.image_ls:
            save_path = os.path.join(self.conf.image_save_dir, im_name)
            # print(save_path)
            if im_name in img_ls_in_text or im_name in temp_ls:  # 在笔记中，且文件存在
                if os.path.isfile(save_path):
                    new_image_ls.append(im_name)
            else:  # 不在笔记中，且文件存在，删除该文件
                if os.path.isfile(save_path):
                    # shutil.rmtree(save_path)#windows好像会出错
                    os.remove(save_path)
        # print('new_image_ls',new_image_ls)
        paper_sample.image_ls = new_image_ls

    # 更新统计信息：year，title，tag，produce
    def update_static_ls(self):
        for i in self.keys():
            paper = self[i]
            assert isinstance(paper, Paper_Sample)
            if paper.title.lower() not in self.title_low_ls:
                self.title_low_ls.append(paper.title.lower())
            if paper.years not in self.years_ls:
                self.years_ls.append(paper.years)
            if paper.produce.lower() not in self.produce_ls:
                self.produce_ls.append(paper.produce)
            for k in paper.tags:
                if k not in self.all_tags:
                    self.all_tags.append(k)

    @classmethod
    def demo_data(cls):
        pdata = Paper_Data(Settings())
        N_paper = 1000
        for i in range(N_paper):
            p, ind = pdata.new_paper_note()
            p.title = '论文 %s' % ind
            p.years = '%s' % (2000 + i)
            p.produce = 'CCTV'
            p.text = '笔记内容 %s' % ind
            if i == 2:
                p.image_ls = ['temp2.png', ]
            if i == 4:
                p.text = '笔记内容%s,<br>显示一下看看' % ind
            if i == 5:
                p.image_ls = ['temp1.png', ]
            if i == 7:
                p.image_ls = ['temp.png', ]
        return pdata


if __name__ == '__main__':
    Settings.demo()
