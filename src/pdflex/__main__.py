#! /usr/bin/env python
import sys
from argparse import ArgumentParser
from .cons import IFORMATS_DOC,IFORMATS_IMG,OFORMATS_IMG
from .func import split_pdf,merge_pdf,convert_format


def create_parser() -> ArgumentParser:
    """创建并配置参数解析器"""
    parser = ArgumentParser(
        prog='pdftool',     # 设置你想要的程序名
        description='PDF工具, 可以对PDF文件进行拆分、合并和转换格式.'
        )
    
    # 必需参数组
    required = parser.add_argument_group('输入输出')
    required.add_argument(
        'input', 
        nargs='?',
        help='输入文档或目录路径'
    )
    required.add_argument(
        '-o', '--output',
        required=False,     # 根据操作类型可能变为必需
        help='输出文档或目录路径'
    )

    # 操作模式组 (互斥)
    mode_group = parser.add_mutually_exclusive_group(required=False)
    mode_group.add_argument(
        '-s', '--split', 
        action='store_true',
        help='拆分PDF文档'
    )
    mode_group.add_argument(
        '-m', '--merge', 
        action='store_true',
        help='合并多个文档'
    )
    mode_group.add_argument(
        '-c', '--convert', 
        action='store_true',
        help='转换文件格式'
    )

    # 选项参数组
    options = parser.add_argument_group('处理选项')
    options.add_argument(
        '-p', '--page_count', 
        type=int, 
        default=1,
        help='拆分时每个子文档的页数 (默认: 1)'
    )
    options.add_argument(
        '-f', '--src_type',
        help=f'输入文件类型. 文档类型:{','.join(IFORMATS_DOC)}; 图片类型:{','.join(IFORMATS_IMG)}.'
    )
    options.add_argument(
        '-t', '--dst_type',
        help=f'输出文件类型. 文档类型:pdf; 图片类型:{','.join(OFORMATS_IMG)}.'
    )
    
    return parser

def main() -> None:
    """主入口函数"""

    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.split:
            split_pdf(args.input, args.output, args.page_count, args.src_type, args.dst_type)
        elif args.merge:
            merge_pdf(args.input, args.output, args.dst_type)
        elif args.convert:
            convert_format(args.input, args.output,  args.src_type, args.dst_type)
        else:
            print(f'输入 python -m {__package__} -h 查看帮助信息.')
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()