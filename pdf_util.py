import fitz  # 导入fitz库

def convert_to_image(pdf_path, output_image_path):
    """
    将PDF的第一页转换为图片。

    :param pdf_path: PDF文件的路径。
    :param output_image_path: 输出图片的路径。
    """
    try:
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)

        # 选择PDF的第一页
        page = pdf_document[0]

        # 将页面转换为图像
        pix = page.get_pixmap()
        pix.save(output_image_path)

        # 关闭PDF文件
        pdf_document.close()

        print(f"First page saved as {output_image_path}")
    except Exception as e:
        print(f"转换过程中发生错误: {e}")

