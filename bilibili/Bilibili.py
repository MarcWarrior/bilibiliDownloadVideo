#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import argparse
from base import *


class BiliBili:
    def __init__(self, aid, directory=r'video', danmu=None):
        """
        初始化
        :param aid: 普通视频AV号
        :param directory: 目录名
        :param danmu: 是否下载视频弹幕
        :return None
        """
        self.aid = aid
        self.directory = directory
        self.danmu = True if danmu is not None and danmu != 0 else False

    def download_video(self):
        video = Video(self.aid)
        if self.danmu:
            video.multi_thread_download_video(self.directory)
        else:
            video.async_download_video(self.directory)


if __name__ == '__main__':
    """
    sys.argv
    传递给Python脚本的命令行参数列表。
    argv[0]是脚本名称（依赖于操作系统，无论这是否是完整路径名）。
    如果使用-c解释器的命令行选项执行命令，argv[0]则将其设置为字符串'-c'。
    如果没有脚本名称传递给Python解释器，argv[0]则为空字符串
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    """
    该argparse模块可以轻松编写用户友好的命令行界面。
    该程序定义了它需要的参数，并且argparse将弄清楚如何解析sys.argv。
    当用户给程序提供无效参数时，该argparse模块还会自动生成帮助和使用消息并发出错误。

    class argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[],
                                formatter_class=argparse.HelpFormatter, prefix_chars='-',
                                fromfile_prefix_chars=None, argument_default=None, conflict_handler='error',
                                add_help=True, allow_abbrev=True)
    创建一个新ArgumentParser对象。所有参数都应作为关键字参数传递，它们是：
    PROG -程序的名称（默认：sys.argv[0]）
    usage - 描述程序用法的字符串（默认值：从添加到解析器的参数生成）
    description - 参数help之前显示的文本（默认值：none）
    epilog - 参数help后显示的文本（默认值：none）
    parents - ArgumentParser还应包含其参数的对象列表
    formatter_class - 用于自定义帮助输出的类
    prefix_chars - 前缀可选参数的字符集（默认值：' - '）
    fromfile_prefix_chars -该组文件前缀字符从额外的参数应该读（默认值：None）
    argument_default -为参数的全局默认值（默认值：None）
    conflict_handler - 解决冲突选项的策略（通常是不必要的）
    add_help -添加-h/--help选项解析器（默认值：True）
    allow_abbrev - 如果缩写是明确的，则允许缩写长选项。（默认值：True）

    默认情况下，ArgumentParser对象用于sys.argv[0]确定如何在帮助消息中显示程序的名称。
    这个默认值几乎总是可取的，因为它会使帮助消息与命令行上调用程序的方式相匹配。
    """
    parser = argparse.ArgumentParser()
    """
    ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices]
                                [, required][, help][, metavar][, dest])
    定义应如何解析单个命令行参数。每个参数在下面都有自己更详细的描述，但简而言之，它们是：

    name or flags - 选项字符串的名称或列表，例如foo 或-f, --foo
    action - 在命令行遇到此参数时要采取的基本操作类型。
    nargs - 应该使用的命令行参数的数量。
    const - 某些操作和nargs选择所需的常量值。
    default - 如果命令行中不存在参数，则生成的值。
    type - 应转换命令行参数的类型。
    choices - 参数允许值的容器。
    required - 是否可以省略命令行选项（仅限选项）。
    help - 对参数的作用的简要说明。
    metavar - 用法消息中参数的名称。
    dest - 要添加到返回的对象的属性的名称 parse_args()。
    """
    parser.add_argument('-i', '--input', required=True, help='The AV number of the video for downloading', type=str)
    parser.add_argument('-d', '--dir', required=False, help='Save download file to a directory path', type=str, default='video')
    parser.add_argument('-D', '--Danmu', required=False, help='Whether to download the danmu of the video,if Yes,input non_zero number', type=int, default=0)

    """
    ArgumentParser.parse_args(args=None, namespace=None)
    将参数字符串转换为对象并将其指定为命名空间的属性。
    返回填充的命名空间。
    以前的调用add_argument()确切地确定创建了哪些对象以及如何分配它们。
    args - 要解析的字符串列表。默认值取自 sys.argv。
    namespace - 获取属性的对象。默认值是一个新的空 Namespace对象。
    """
    args = parser.parse_args()
    b_video = BiliBili(args.input, args.dir, args.Danmu)
    b_video.download_video()
