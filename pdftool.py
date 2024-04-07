#! /usr/bin/env python

import argparse
import fitz
import os
from typing import Optional
from cons import *
from func import *


def split_pdf(input_path: str, output_path: Optional[str], page_count: int = 1, src_type: Optional[str] = None, dst_type: Optional[str] = None) -> RC:
    """
    拆分文件到指定目录


    参数：
        input_path -- 输入文件
        output_path -- 输出目录
        page_count -- 拆分页数
        src_type -- 输入文件类型
        dst_type -- 输出文件类型

    
    返回值：
        执行结果
    """

    if input_path is None:
        print(f'拆分文件发生错误: 没有指定输入文件')
        return RC.NULL_INPUT
    
    # 如果 src_type 不为空则将其转换为小写字母形式；否则通过文件扩展名获取文件类型
    src_type = src_type.lower() if src_type else get_file_type(input_path)
    if src_type not in IFORMATS_DOC:
        print(f'拆分文件发生错误: 不支持的输入类型 {src_type}')
        return RC.INVALID_INPUT

    try:
        with fitz.open(input_path, filetype=src_type) as in_doc:
            pass
    except Exception as e:
        # 捕获所有类型的异常
        print(f'拆分文件发生错误 {type(e).__name__}: {e}')
        return RC.INVALID_INPUT
    
    # 如果 dst_type 不为空则将其转换为小写字母形式；否则将其设为默认值 'pdf'
    dst_type = dst_type.lower() if dst_type else 'pdf'
    if dst_type != 'pdf' and dst_type not in OFORMATS_IMG:
        print(f'拆分文件发生错误: 不支持的输出类型 {dst_type}')
        return RC.INVALID_OUTPUT

    # 通过 splitext 将路径拆分为 (root, ext)
    dst_dir = os.path.splitext(os.path.basename(input_path))[0]+'-split'
    # 如果 output_path 非空则保留其原值；否则赋值为 dst_dir
    output_path = output_path or dst_dir

    if os.path.exists(output_path):
        print(f'拆分文件发生错误: {os.path.abspath(output_path)} 已存在，请重新指定一个目录')
        return RC.INVALID_OUTPUT
    
    # 创建输出目录
    os.mkdir(output_path)

    in_doc = fitz.open(input_path, filetype=src_type)
    if not in_doc.is_pdf and src_type in IFORMATS_DOC:
        in_doc.close()
        in_doc = fitz.open()
        in_doc.insert_file(input_path)
    
    # 获取要拆分文件的总页数
    total_pages = in_doc.page_count

    # 按指定的页数拆分为单独的文件
    page_count = page_count if page_count > 0 else 1
    if total_pages <= page_count:
        print(f'{input_path} 总页数为 {total_pages}，无需拆分。')
        # 关闭源文件
        in_doc.close()
        return RC.SUCCESS
    
    for i in range(0,total_pages,page_count):
        # 拆分文件的结束页
        last_page = min(i+page_count,total_pages)-1
        # 构建输出文件名
        ofile_path = os.path.join(output_path, f'{dst_dir}{i+1}-{last_page+1}.{dst_type}')

        if dst_type == 'pdf':
            # 创建一个新的 PDF 文件
            out_pdf = fitz.open()
            # 将拆分页添加到新的 PDF 文件中
            out_pdf.insert_pdf(in_doc, from_page=i, to_page=last_page)
            # 保存新的 PDF 文件
            out_pdf.save(ofile_path)
            out_pdf.close()
        elif dst_type in OFORMATS_IMG:
            src_pixs = []
            zoom_x = 2.0
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x, zoom_y)

            for j in range(i,min(i+page_count,total_pages)):
                # 使用 PixMap 将页面转换为图像
                src_pixs.append(in_doc[j].get_pixmap(matrix=mat))
            
            tar_pix = merge_pixmap(src_pixs)

            # 保存图像
            tar_pix.save(ofile_path,output=dst_type)

    # 关闭源文件
    in_doc.close()
    return RC.SUCCESS


def merge_pdf(input_path: str, output_path: str, dst_type: Optional[str] = None) -> RC:
    """
    合并文件

    参数：
        input_path -- 输入目录
        output_path -- 输出文件
        dst_type -- 输出文件类型

    返回值：
        执行结果
    """

    if input_path is None:
        print(f'合并文件发生错误: 没有指定输入目录')
        return RC.NULL_INPUT

    if not os.path.isdir(input_path):
        print(f'合并文件发生错误: 输入不是有效目录')
        return RC.INVALID_INPUT

    # 如果 dst_type 不为空则将其转换为小写字母形式；否则通过文件扩展名获取文件类型
    dst_type = dst_type.lower() if dst_type else get_file_type(output_path)
    dst_type = dst_type if dst_type else 'pdf'
    if dst_type != 'pdf' and dst_type not in OFORMATS_IMG:
        print(f'合并文件发生错误: 不支持的输出类型 {dst_type}')
        return RC.INVALID_OUTPUT

    dir_name = os.path.basename(input_path.rstrip('/\\'))
    output_path = output_path if output_path else f'{dir_name}-merge.{dst_type}'

    if os.path.exists(output_path):
        print(f'合并文件发生错误: {os.path.abspath(output_path)} 已存在，请指定一个新文件名')
        return RC.INVALID_OUTPUT

    pdf_merger = fitz.open()
    count = 0
    files = sorted(os.listdir(input_path))
    for file_name in files:
        ipath = os.path.join(input_path, file_name)
        src_type = get_file_type(file_name)
        if src_type in IFORMATS_DOC or src_type in IFORMATS_IMG:
            pdf_merger.insert_file(ipath)
            count += 1
        else:
            print(f'合并文件发生错误: 不支持的输入文件 {ipath}')

    if dst_type == 'pdf':
        # 保存合并后的 PDF 文件
        pdf_merger.save(output_path)
        pdf_merger.close()
    elif dst_type in OFORMATS_IMG:
        src_pixs = []
        zoom_x = 2.0
        zoom_y = 2.0
        mat = fitz.Matrix(zoom_x, zoom_y)

        for page in pdf_merger:
            # 使用 PixMap 将页面转换为图像
            src_pixs.append(page.get_pixmap(matrix=mat))
        
        tar_pix = merge_pixmap(src_pixs)
        # 保存图像
        tar_pix.save(output_path,output=dst_type)

    print(f'指定目录共有文件 {len(files)} 个，合并 {count} 个，无法处理 {len(files)-count} 个')
    return RC.SUCCESS


def convert_format(input_path: str, output_path: Optional[str] = None, src_type: Optional[str] = None, dst_type: Optional[str] = None) -> RC:
    """
    转换文件类型

    参数：
        input_path -- 输入文件
        output_path -- 输出文件
        src_type -- 输入文件类型
        dst_type -- 输出文件类型

    返回值：
        执行结果
    """
    if input_path is None:
        print(f'转换文件发生错误: 没有指定输入文件')
        return RC.NULL_INPUT

    # 如果 src_type 不为空则将其转换为小写字母形式；否则通过文件扩展名获取文件类型
    src_type = src_type.lower() if src_type else get_file_type(input_path)
    if src_type not in IFORMATS_DOC and src_type not in IFORMATS_IMG:
        print(f'转换文件发生错误: 不支持的输入类型 {src_type}')
        return RC.INVALID_INPUT

    try:
        with fitz.open(input_path, filetype=src_type) as in_doc:
            pass
    except Exception as e:
        # 捕获所有类型的异常
        print(f'转换文件发生错误 {type(e).__name__}: {e}')
        return RC.INVALID_INPUT

    # 如果 dst_type 不为空则将其转换为小写字母形式；否则通过文件扩展名获取文件类型
    dst_type = dst_type.lower() if dst_type else get_file_type(output_path)
    dst_type = dst_type if dst_type else 'pdf'
    if dst_type != 'pdf' and dst_type not in OFORMATS_IMG:
        print(f'转换文件发生错误: 不支持的输出类型 {dst_type}')
        return RC.INVALID_OUTPUT

    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = output_path if output_path else f'{file_name}.{dst_type}'

    if os.path.exists(output_path):
        print(f'转换文件发生错误: {os.path.abspath(output_path)} 已存在，请指定一个新文件名')
        return RC.INVALID_OUTPUT

    if src_type == dst_type:
        print(f'输入输出格式相同，都为 {dst_type} ，不需要转换')
        return RC.SUCCESS

    if dst_type == 'pdf':
        in_doc = fitz.open()
        in_doc.insert_file(input_path)
        in_doc.save(output_path)
        in_doc.close()

    elif dst_type in OFORMATS_IMG:
        if src_type in IFORMATS_DOC:
            src_pixs = []
            zoom_x = 2.0
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x, zoom_y)

            in_doc = fitz.open(input_path)
            for page in in_doc:
                # 使用 PixMap 将页面转换为图像
                src_pixs.append(page.get_pixmap(matrix=mat))
            
            tar_pix = merge_pixmap(src_pixs)
            # 保存图像
            tar_pix.save(output_path, output=dst_type)
            in_doc.close()
        elif src_type in IFORMATS_IMG:
            pix = fitz.Pixmap(input_path)
            pix.save(output_path, output=dst_type)

    return RC.SUCCESS


if __name__ == '__main__':

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='PDF 工具，可以拆分和合并 PDF 文件，转换文件格式。')

    parser.add_argument('input', nargs='?', help='输入路径')
    parser.add_argument('-o', '--output', help='输出路径')

    # 创建互斥参数组
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--split', action='store_true', help='拆分文档到指定的目录')
    group.add_argument('-m', '--merge', action='store_true', help='合并指定目录中的文件到单一文件')
    group.add_argument('-c', '--convert', action='store_true', help='转换文件格式')

    # 添加其他选项参数
    parser.add_argument('-p', '--page_count', type=int, default=1, help='拆分文档时单个拆分文件所包含的页数，默认为 1 页')
    parser.add_argument('-f', '--src_type', help='输入文件类型')
    parser.add_argument('-t', '--dst_type', help='输出文件类型')

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
        delimiter = ', '
        print(f'输入 {filename} -h 查看帮助信息')
        print(f'{filename} 的输入输出支持以下文件类型:')
        print(f'输入[input]\n文档格式: {delimiter.join(IFORMATS_DOC)}\n图片格式: {delimiter.join(IFORMATS_IMG)}')
        print(f'输出[-o, --output]\n文档格式: pdf\n图片格式: {delimiter.join(OFORMATS_IMG)}')

