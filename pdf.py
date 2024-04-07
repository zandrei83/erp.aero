import math
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTRect, LTFigure, LTImage, LTTextBox, LTLine, LTCurve
import pypdfium2 as pdfium
from pyzbar.pyzbar import decode


class ParsePdf:
    def __init__(self, file_name):
        self.file_name = file_name
        self.content = {'labels': {}, 'barcodes': {}, 'images': {}}

    def parse_pdf(self):

        counter_key = 0

        for page_layout in extract_pages(self.file_name):
            for element in page_layout:
                cur_elem = {}
                if isinstance(element, LTTextContainer):
                    elem_content = element.get_text()
                    if elem_content not in (' \n', '', ' ', '\n'):
                        elem_parts = elem_content.split(":")
                        if len(elem_parts) > 1:
                            key = elem_parts[0]
                            value = elem_parts[1][:-1]
                            if value in (' '):
                                value = '';
                        else:
                            value = elem_parts[0][:-1]
                            if value.find('LLC') != -1:
                                key = 'COMPANY NAME'
                            elif value.find('notes') != -1:
                                key = 'INSPECTION NOTES'
                            else:
                                key = 'UNRECOGNISED KEY ' + str(counter_key)
                                counter_key += 1

                        cur_elem[key] = {
                            'TYPE': 'text', 'value': value, 'x0': math.ceil(element.x0),
                            'y0': math.ceil(element.y0), 'x1': math.ceil(element.x1), 'y1': math.ceil(element.y1)
                        }

                    self.content['labels'].update(cur_elem)

                elif isinstance(element, LTImage):
                    # Extract images
                    pass
                elif isinstance(element, LTRect):
                    # Extract rects
                    pass

        # Getting barcode information
        self.content['barcodes'].update(self.parse_barcodes())

        return self.content

    def parse_barcodes(self):

        barcode_list = {}
        barcode_counter = 1

        pdf = pdfium.PdfDocument(self.file_name)

        for i in range(len(pdf)):

            page = pdf[i]
            image = page.render(scale=4).to_pil()
            decoded_barcodes = decode(image)

            for barcode in decoded_barcodes:
                key = 'barcode'+str(barcode_counter)
                (x, y, width, height) = barcode.rect

                barcode_list[key] = {
                    'data': barcode.data.decode('UTF-8'), 'type': barcode.type, 'orientation': barcode.orientation,
                    'x': x, 'y': y, 'width': width, 'height': height
                }
                barcode_counter += 1

        return barcode_list

if __name__ == '__main__':

    pdf = ParsePdf('standard.pdf')
    content = pdf.parse_pdf()
    print(content)
