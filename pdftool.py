#! /usr/bin/env python

import argparse
import os

from cons import IFORMATS_DOC,IFORMATS_IMG,OFORMATS_IMG
from func import split_pdf,merge_pdf,convert_format


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='PDF工具, 可以对PDF文件进行拆分、合并和转换格式.')

    parser.add_argument('input', nargs='?', help='输入文档或目录')
    parser.add_argument('-o', '--output', help='输出文档或目录')

    # 创建互斥参数组
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--split', action='store_true', help='拆分文档到输出目录')
    group.add_argument('-m', '--merge', action='store_true', help='合并输入目录中的文档到单一文档')
    group.add_argument('-c', '--convert', action='store_true', help='转换文件格式')

    # 添加其他选项参数
    parser.add_argument('-p', '--page_count', type=int, default=1, help='生成拆分文档的页数(默认1页)')
    delimiter = ','
    parser.add_argument('-f', '--src_type', help=f'输入文件类型, 文档类型:{delimiter.join(IFORMATS_DOC)}; 图片类型:{delimiter.join(IFORMATS_IMG)}.')
    parser.add_argument('-t', '--dst_type', help=f'输出文件类型, 文档类型:pdf; 图片类型:{delimiter.join(OFORMATS_IMG)}.')

    # 解析命令行参数
    args = parser.parse_args()
    
    if args.split:
        split_pdf(args.input, args.output, args.page_count, args.src_type, args.dst_type)
    elif args.merge:
        merge_pdf(args.input, args.output, args.dst_type)
    elif args.convert:
        convert_format(args.input, args.output,  args.src_type, args.dst_type)
    else:
        filename = os.path.basename(__file__)
        print(f'输入 python {filename} -h 查看帮助信息.')

if __name__ == '__main__':
    main()