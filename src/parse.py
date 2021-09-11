# import pdfbox # move to func so system alias works for company search

# Allow relative import from anywhere
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from urllib.request import Request, urlopen
from constants import DATA_PATH, TEST_YEAR
from data import data


def get_data_(test: bool) -> Path:
    """Save as pdf file(s)"""
    Path(DATA_PATH).mkdir(exist_ok=True)
    # test with one year
    years = [TEST_YEAR] if test else [datum.year for datum in data]
    for datum in data:
        if datum.year in years:
            req = Request(datum.url, headers={"User-Agent": "XYZ/3.0"})
            mybytes = urlopen(req, timeout=10).read()
            path = Path(DATA_PATH, str(datum.year)).with_suffix(".pdf")  # pdf in bytes
            path.write_bytes(mybytes)
    return Path()


def pdf_to_string_(input_path: str) -> str:
    """Given the path of pdf input file,
    save contents as text.

    If none, do for all known years; expect pdfs exist.

    Params:
        string input_path: path to file
            if absent, do all pdfs

    Returns a string, mainly for testing.
    """
    import pdfbox

    # TODO: capture stderr
    test = False  # add as param
    pdf_ref = pdfbox.PDFBox()
    years = [datum.year for datum in data]
    input_paths = (
        [Path(input_path)]
        if input_path
        else [Path(DATA_PATH, str(year)).with_suffix(".pdf") for year in years]
    )
    all_txt = ""
    for path in input_paths:
        if not path.exists():  # skip missing files
            break
        pdf_ref.extract_text(str(path))  # -> adds suffix: .txt
        output = Path(path).with_suffix(".txt")
        txt = output.read_text(errors="ignore")  # pdfs have non text byte data
        txt = txt.casefold()
        all_txt = ";".join([all_txt, txt])
    return all_txt


# TODO: don't print this error
#     Aug 25, 2021 1:24:08 AM org.apache.pdfbox.pdmodel.font.PDSimpleFont toUnicodeWARNING: No Unicode mapping for f_f (31) in font QSPMMV+Calibre-Regular\
# TODO: if not found, save to not found list
def company_in_year_(company: str, test: bool) -> "list[str]":
    """Return true if the company in any year
    else false"""
    # test with one year
    found_in = []
    years = [TEST_YEAR] if test else [datum.year for datum in data]
    for datum in data:
        if datum.year in years:
            input = Path(DATA_PATH, str(datum.year)).with_suffix(".txt")
            txt = input.read_text()
            if company in txt:
                found_in.append(str(datum.year))
    return found_in
