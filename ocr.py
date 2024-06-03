from paddleocr import PaddleOCR

import pdf_util

ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory


def parse(image_path):
    result = ocr.ocr(image_path, cls=True)[0]
    return result


if __name__ == '__main__':
    jpg = "test/1.jpg"
    pdf_util.convert_to_image('test/1.pdf', jpg)
    parse(jpg)