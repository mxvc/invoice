import pdfplumber

file_path = 'test\特殊字体BWSimKai.pdf'
with pdfplumber.open(file_path) as pdf:
    page = pdf.pages[0]
    lines = page.extract_text_simple()
    print(lines)
