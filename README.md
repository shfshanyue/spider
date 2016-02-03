> usage: a demo learning argparse [-h] [-d INTERVAL] [-u URL] [-o SAVE_PATH]

> optional arguments:
    -h, --help    show this help message and exit
    -d INTERVAL   任务执行间隔时间
    -u URL        所要爬取的网页
    -o SAVE_PATH  保存的路径

下载html文件，解析其中的静态资源，保存在相应的路径。每当把文件保存至本地时，便把html文件的在线路径替换为本地路径。
完成后，应对css文件做相应的处理，因为css文件会包含大量的背景图片。

分析题目如下

1. 参数解析。可以使用sys模块的argv，不过略显麻烦。考虑采用optparse或者argparse模块。
2. 下载网页。python2，用urlliib2模块下载网页，urlparse解析url路径。python3，只用一个urllib即可，不过在python3上遇上了编码问题。另外，也可以考虑使用requests模块，不过显得有些重了。
3. 解析网页。使用正则表达式，是re模块。也可以考虑使用lxml或者bs4。
4. 文件处理。会涉及到创建文件夹，使用模块shutil和os。
5. 时间处理。使用datetime模块。

最后代码有如下几个问题

1. 不能下载所有的静态文件，有正则表达式的问题，可以使用bs4或者lxml模块代替。
2. 未对css中的背景图片做下载处理。处理css文件与处理html文件一样，但是在其他函数中把self.text写死了，不能重用代码，故暂时还未做处理。
3. 没有进行多线程处理。

