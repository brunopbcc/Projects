import pytesseract
from PIL import Image
import PyPDF2
import io
import os

# INSERT YOUR TESSERACT PATH BELOW
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
    return text


def ocr_page(page):
    try:
        xObject = page['/Resources']['/XObject'].get_object()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].get_data()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                img = Image.frombytes(mode, size, data)
                text = pytesseract.image_to_string(img)
                return text
    except Exception as e:
        return ""
    return ""


def ocr_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text() or ocr_page(page)
            text += page_text
            writer.add_page(page)

    output_pdf_path = os.path.splitext(pdf_path)[0] + "_with_text.pdf"
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    return text


def main():
    ###INSERT YOUR PDF BELOW
    pdf_path = r'PATH/TO/FILE.pdf'
    extracted_text = pdf_to_text(pdf_path)
    print("Texto extraído do PDF:")
    print(extracted_text)
    print("\n")

    ocr_text = ocr_pdf(pdf_path)
    print("Texto extraído do OCR:")
    print(ocr_text)


if __name__ == "__main__":
    main()
