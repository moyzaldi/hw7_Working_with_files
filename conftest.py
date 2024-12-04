import os.path
import requests
import pytest
import shutil
import zipfile

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
    with zipfile.ZipFile("tmp/multiple_files.zip", mode="w") as archive:
        for file in files:
            add_file = os.path.join(TMP_DIR, file)  # склеиваем путь к файлам которые добавляют в архив
            archive.write(add_file, os.path.basename(add_file))  # добавляем файл в архив
    yield
    shutil.rmtree(TMP_DIR)
