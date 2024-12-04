import os.path
import requests
import pytest
import shutil
import zipfile
from zipfile import ZipFile
from io import BytesIO
from pypdf import PdfReader
import openpyxl
import pandas as pd

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
TMP_DIR = os.path.join(CURRENT_DIR, "tmp")

url = "https://freetestdata.com/wp-content/uploads/2021/09/"
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"}

files = [
    "Free_Test_Data_100KB_PDF.pdf",
    "Free_Test_Data_100KB_XLSX.xlsx",
    "Free_Test_Data_200KB_CSV-1.csv"
]


@pytest.fixture(scope="session", autouse=True)
def creating_folder_with_files():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    for file in files:
        download_url = url + file
        content = requests.get(url=download_url, headers=headers).content  # скачиваем файл
        with open(os.path.join(TMP_DIR, file), 'wb') as file:  # путь
            file.write(content)

    yield
    shutil.rmtree(TMP_DIR)


def test_create_archive_and_counting_files():
    with zipfile.ZipFile("tmp/multiple_files.zip", mode="w") as archive:
        for file in files:
            add_file = os.path.join(TMP_DIR, file)  # склеиваем путь к файлам которые добавляют в архив
            archive.write(add_file, os.path.basename(add_file))  # добавляем файл в архив
    assert len(archive.infolist()) == 3
    assert zipfile.is_zipfile("tmp/multiple_files.zip") == True


def test_pdf_file_size():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert round(myzip.getinfo("Free_Test_Data_100KB_PDF.pdf").file_size // 1000, -1) == 100


def test_pdf_file_quantity_pages():
    with ZipFile("tmp/multiple_files.zip") as zip_file:
        content = PdfReader(BytesIO(zip_file.read("Free_Test_Data_100KB_PDF.pdf")))
        assert len(content.pages) == 3


def test_xlsx_file_size():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert round(myzip.getinfo("Free_Test_Data_100KB_XLSX.xlsx").file_size // 1000, -1) == 100


def test_xlsx_file_quantity_sheet():
    with ZipFile("tmp/multiple_files.zip") as zip_file:
        content = openpyxl.load_workbook(BytesIO(zip_file.read("Free_Test_Data_100KB_XLSX.xlsx")))
        assert len(content.sheetnames) == 1


def test_csv_file_size():
    with ZipFile("tmp/multiple_files.zip", "r") as myzip:
        assert round(myzip.getinfo("Free_Test_Data_200KB_CSV-1.csv").file_size // 1000, -1) == 200


def test_csv_file_quantity_lines():
    with ZipFile("tmp/multiple_files.zip") as zip_file:
        content = pd.read_csv(BytesIO(zip_file.read("Free_Test_Data_200KB_CSV-1.csv")))
        assert len(content) == 15723
