import io
from pdfminer.high_level import extract_text

with open("sample/pdf/n1_sp22.pdf",'rb') as f:
    print(io.BytesIO(f))
    text = extract_text(f)