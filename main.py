#! /usr/bin/env python
# coding: utf-8

import argparse
import re
import os
import datetime
import urlparse
import shutil
import httplib
import time

from urllib2 import urlopen, HTTPError, URLError


class Spider(object):
    """爬取一个网页，并保存在本地指定的路径
    
    Attributes:
        base_path (str): 网页保存的路径，由参数-o指定
        save_path (str): 由爬取时间指定的路径
        base_url (str): 所要爬取的网页
        err_no (int): 出错的静态资源数目
        success_no (int): 成功的静态资源数目
        id (int): 静态资源的编号
        text (str): 爬取网页的html代码
    """
    def __init__(self, url, save_path):
        try:
            self.text = urlopen(url).read()
        except URLError as e:
            print(e)
        self.base_url = url
        self.save_path = save_path

    def start(self):
        """以当前时间为名创建文件夹，如果此文件夹已存在则删除该文件夹。并启动程序开始抓取网页资源。
        
        Returns:
            dict: 成功下载的资源数，失败的资源数数以及失败的url列表
        """
        self.id = 0
        self.err_no = 0
        self.success_no = 0
        self.err_list = []
        folder_name = '{:%y%m%d%H%M%S}'.format(datetime.datetime.now())
        folder_name = os.path.join(self.save_path, folder_name)
        self.base_path = folder_name
        try:
            os.makedirs(folder_name)
        except FileExistsError as e:
            shutil.rmtree(folder_name)
            print('rmtree {} and remakedirs'.format(folder_name))
        img_folder = os.path.join(folder_name, 'images')
        os.makedirs(img_folder)
        os.makedirs(os.path.join(folder_name, 'style'))
        os.makedirs(os.path.join(folder_name, 'js'))
        self.folder = {
            'jpg': img_folder,
            'png': img_folder,
            'gif': img_folder,
            'ico': img_folder,
            'css': os.path.join(folder_name, 'style'),
            'js': os.path.join(folder_name, 'js')
        }
        for src_type in ['jpg', 'png', 'gif', 'css', 'js', 'ico']:
            for url, filename, scr_type in self.get_source(src_type):
                if self._save_file(url, filename, scr_type):
                    self.success_no += 1
                else:
                    self.err_no += 1
                    self.err_list.append(url)
        self.save_html()
        return {
            'success': self.success_no,
            'error': {
                'len': self.err_no,
                'list': self.err_list
            }
        }

    def get_source(self, scr_type):
        """根据指定的后缀，得到相应的静态资源列表。    
        
        Args:
            scr_type (str): 爬取指定后缀的文件，如jpg，gif，css

        """
        if scr_type == 'css':
            pattern = re.compile(r'\shref="([^"]*?\.css)"')
        else:
            pattern = re.compile(r'\ssrc="([^"]*?\.{})"'.format(scr_type))
        files = pattern.findall(self.text)
        for url in set(files):
            file_name = '{}.{}'.format(self.id, scr_type)
            self.id += 1
            yield url, file_name, scr_type

    def save_html(self):
        """当静态资源处理完成后，保存html文件

        """
        file = os.path.join(self.base_path, 'index.html')
        with open(file, 'w') as f:
            f.write(self.text)

    def _save_file(self, url, file_name, file_type):
        """保存文件，并替换html中相对于的静态资源地址
        
        Args:
            url (str): 要抓取的静态资源地址
            file_name (str): 在本地需要保存的文件名
            file_type (str): 保存的文件类型，通过此判断应该位于哪个文件夹下
        
        Returns:
            bool: 文件是否被成功保存
        """
        abs_url = urlparse.urljoin(self.base_url, url)
        try:
            source = urlopen(abs_url).read()
        except (HTTPError, URLError) as e:
            print(e)
            return False
        except httplib.BadStatusLine:
            return False
        file = os.path.join(self.folder[file_type], file_name)
        with open(file, 'wb') as f:
            f.write(source)
            self.text = self.text.replace(url, 'file:///{}'.format(file))
            print('{} ---> {}'.format(url, file))
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser('a demo learning argparse')
    parser.add_argument('-d', dest='interval', action='store', help='任务执行间隔时间')
    parser.add_argument('-u', dest='url', action='store', help='所要爬取的网页')
    parser.add_argument('-o', dest='save_path', action='store', help='保存的路径')
    args = parser.parse_args()

    s = Spider(args.url, args.save_path)
    while True:
        info = s.start()
        print('success {}, fail {}'.format(info['success'], info['error']['len']))
        print('-'*64)
        time.sleep(int(args.interval))
