import zipfile
from zipfile import ZipFile
from io import BytesIO
from pypdf import PdfReader
import openpyxl
import pandas as pd


def test_create_archive_and_counting_files():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert len(myzip.infolist()) == 3
        assert zipfile.is_zipfile("tmp/multiple_files.zip") == True


def test_pdf_file_size():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert round(myzip.getinfo("Free_Test_Data_100KB_PDF.pdf").file_size // 1000, -1) == 100


def test_pdf_file_quantity_pages():
    with ZipFile("tmp/multiple_files.zip") as myzip:
        content = PdfReader(BytesIO(myzip.read("Free_Test_Data_100KB_PDF.pdf")))
        assert len(content.pages) == 3


def test_xlsx_file_size():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert round(myzip.getinfo("Free_Test_Data_100KB_XLSX.xlsx").file_size // 1000, -1) == 100


def test_xlsx_file_quantity_sheet():
    with ZipFile("tmp/multiple_files.zip") as myzip:
        content = openpyxl.load_workbook(BytesIO(myzip.read("Free_Test_Data_100KB_XLSX.xlsx")))
        assert len(content.sheetnames) == 1


def test_csv_file_size():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert round(myzip.getinfo("Free_Test_Data_200KB_CSV-1.csv").file_size // 1000, -1) == 200


def test_csv_file_quantity_lines():
    with ZipFile("tmp/multiple_files.zip") as myzip:
        content = pd.read_csv(BytesIO(myzip.read("Free_Test_Data_200KB_CSV-1.csv")))
        assert len(content) == 15723
