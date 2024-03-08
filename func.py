import fitz
import os

def merge_pixmap(pixmap_list: list[fitz.Pixmap]) -> fitz.Pixmap:
    """
    合并 Pixmap 图像列表为单一 Pixmap 图像

    参数：
    pixmap_list -- 需要合并的 Pixmap 图像列表

    返回值：
    合并后的 Pixmap 图像
    """

    if not pixmap_list:
        return None

    tar_pix_width = max([x.width for x in pixmap_list])
    tar_pix_height = sum([x.height for x in pixmap_list])

    # create target pixmap
    tar_pix = fitz.Pixmap(pixmap_list[0].colorspace, (0,0,tar_pix_width,tar_pix_height), pixmap_list[0].alpha)

    pos_y = 0
    # now fill target with src_pixs
    for pix in pixmap_list:
        pix.set_origin(0, pos_y)
        pos_y += pix.height
        # copy input to new loc
        tar_pix.copy(pix, pix.irect)

    return tar_pix


def get_file_type(filename: str) -> str:
    """
    通过文件的扩展名获取文件类型

    参数：
    filename -- 文件名或文件路径

    返回值：
    文件类型字符串
    """
    filename = filename if filename else ''
    file_ext = os.path.splitext(filename)[1].lower()
    file_type = file_ext[1:] if len(file_ext) > 1 else ''
    return file_type