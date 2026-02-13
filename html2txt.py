from bs4 import BeautifulSoup
from pathlib import Path

def html2txt(filename):
    file_path = Path(filename)
    soup = BeautifulSoup(open(file_path,'r').read())
    with open(file_path.with_suffix('.txt'), "wb") as text_file:
        text_file.write(soup.get_text().encode('utf-8'))

if __name__ == "__main__":
    html2txt("html2txt_eg.html")