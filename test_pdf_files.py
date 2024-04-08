import pytest
import os
from pdf import ParsePdf


dir_name = 'files_to_test'
files_to_test = os.listdir(dir_name)

etalon_pdf = ParsePdf('standard.pdf')
etalon_content = etalon_pdf.parse_pdf()


def check_val_len(value):
    return True if len(value) > 0 else False


@pytest.mark.parametrize("file_name", files_to_test)
def test_labels(file_name):

    current_pdf = ParsePdf(dir_name+'/' + file_name)
    current_content = current_pdf.parse_pdf()

    # Checking if all labels exist in the testing pdf file
    for tested_key in etalon_content['labels'].keys():
        assert tested_key in current_content['labels'], f'Label "{tested_key}" not found in file "{file_name}"'

    # Check labels positions
    for tested_key, tested_value in etalon_content['labels'].items():
        assert tested_value['x0'] == current_content['labels'][tested_key]['x0'], \
            f'Label "{tested_key}" has wrong position in file "{file_name}"'
        assert tested_value['y0'] == current_content['labels'][tested_key]['y0'], \
            f'Label "{tested_key}" has wrong position in file "{file_name}"'

    # Check labels values
    for tested_key, tested_value in etalon_content['labels'].items():
        assert check_val_len(tested_value['value']) == check_val_len(current_content['labels'][tested_key]['value']), \
            f'Label "{tested_key}" doesn\'t have required value in file "{file_name}"'

    # Number barcodes in the file
    assert len(current_content['barcodes']) > 0, f'Pdf file "{file_name}" doesn\'t have any barcodes'

    # Compare number of the barcodes
    assert len(current_content['barcodes']) == len(etalon_content['barcodes']), \
        f'Number of barcodes doesn\'t match expected number in file "{file_name}"'

    # Check the type of each barcode in pdf file
    for barcode_key, barcode_value in current_content['barcodes'].items():
        barcode_type = barcode_value['type']
        assert barcode_type == 'CODE128', \
            f'Barcode "{barcode_key}" has wrong type ({barcode_type}) in file "{file_name}"'

    # Check the data of each barcode
    for barcode_key, barcode_value in current_content['barcodes'].items():
        assert len(barcode_value['data']) > 0, \
            f'Barcode "{barcode_key}" has no data in file "{file_name}"'

    # Check position of each barcode
    for barcode_key, barcode_value in current_content['barcodes'].items():
        assert barcode_value['x'] == etalon_content['barcodes'][barcode_key]['x'], \
            f'Barcode "{barcode_key}" has wrong position "{file_name}"'
        assert barcode_value['y'] == etalon_content['barcodes'][barcode_key]['y'], \
            f'Barcode "{barcode_key}" has wrong position "{file_name}"'

    # Check for barcode orientation
    for barcode_key, barcode_value in current_content['barcodes'].items():
        barcode_orientation = barcode_value['orientation']
        assert barcode_orientation == 'UP', \
            f'Barcode "{barcode_key}" has wrong orientation ({barcode_orientation}) in file "{file_name}"'


    # Test for images (not implemented)
