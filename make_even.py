from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import os

folder = "./sw"
duplex = True

# remove old output
try:
    os.remove(os.path.join(os.getcwd(), folder, "output.pdf"))
except BaseException:
    pass


def multiply_pdf(file: str):
    total_list = []
    number = int(file.split("_")[0].split("x")[0])
    for i in range(number):
        total_list.append(file)
    return total_list


def make_even(file: str):
    rewrite_needed = False
    with open(os.path.join(os.getcwd(), folder, file), "rb") as pdfFileObj:
        pdf = PdfFileReader(pdfFileObj)
        numPages = pdf.getNumPages()

        if numPages % 2 == 1:
            rewrite_needed = True
            outpdf = PdfFileWriter()
            outpdf.appendPagesFromReader(pdf)
            outpdf.addBlankPage()

            with open(
                os.path.join(os.getcwd(), folder, "temp.pdf"), "wb"
            ) as pdfTempObj:
                outpdf.write(pdfTempObj)

    if rewrite_needed:
        with open(os.path.join(os.getcwd(), folder, "temp.pdf"), "rb") as pdfTempObj:
            pdf = PdfFileReader(pdfTempObj)
            with open(os.path.join(os.getcwd(), folder, file), "wb") as pdfFileObj:
                outpdf = PdfFileWriter()
                outpdf.appendPagesFromReader(pdf)
                outpdf.write(pdfFileObj)
                print("made even: " + file)


# load all file names
all_files = []

for filename in os.listdir(os.path.join(os.getcwd(), folder)):
    if filename.endswith(".pdf"):
        all_files.append(filename)

# make all files even if desired
if duplex:
    for file in all_files:
        make_even(file)
    try:
        os.remove(os.path.join(os.getcwd(), folder, "temp.pdf"))
    except BaseException:
        pass

# join full pdf
fullPDF = []

for file in all_files:
    multi_list = multiply_pdf(file)
    fullPDF = fullPDF + multi_list

print(fullPDF)

# merge whole list
outpdf = PdfFileWriter()
openFileStreams = []

for file in fullPDF:
    pdfFileObj = open(os.path.join(os.getcwd(), folder, file), "rb")
    pdf = PdfFileReader(pdfFileObj)
    outpdf.appendPagesFromReader(pdf)
    openFileStreams.append(pdfFileObj)

with open(os.path.join(os.getcwd(), folder, "output.pdf"), "wb") as pdfTempObj:
    outpdf.write(pdfTempObj)

for stream in openFileStreams:
    stream.close()
