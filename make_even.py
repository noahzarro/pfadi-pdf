from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
import os

folder = "./einseitig"
duplex = False

# remove old output
try:
    os.remove(os.path.join(os.getcwd(),folder,"output.pdf"))
except:
    pass

def multiply_pdf(file:str):
    total_list = []
    number = int(file.split("_")[1])
    for i in range(number):
        total_list.append(file)
    return total_list

def make_even(file:str):
    rewrite_needed = False
    with open(os.path.join(os.getcwd(),folder,file), 'rb') as pdfFileObj: 
        pdf=PdfFileReader(pdfFileObj)
        numPages=pdf.getNumPages()

        if numPages % 2 == 1:
            rewrite_needed = True
            outpdf=PdfFileWriter()
            outpdf.appendPagesFromReader(pdf)
            outpdf.addBlankPage()

            with open(os.path.join(os.getcwd(),folder, "temp.pdf"), 'wb') as pdfTempObj:
                outpdf.write(pdfTempObj)
    
    if rewrite_needed:
        with open(os.path.join(os.getcwd(),folder,"temp.pdf"), 'rb') as pdfTempObj:
            pdf=PdfFileReader(pdfTempObj)
            with open(os.path.join(os.getcwd(),folder, file), 'wb') as pdfFileObj:
                outpdf=PdfFileWriter()
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
        os.remove(os.path.join(os.getcwd(),folder,"temp.pdf"))
    except:
        pass

# join full pdf
fullPDF = []

for file in all_files:
    multi_list = multiply_pdf(file)
    fullPDF = fullPDF + multi_list

fullPDF.sort()

print(fullPDF)

# merge whole list
outpdf=PdfWriter()
openFileStreams = []

for file in fullPDF:
    pdfFileObj = open(os.path.join(os.getcwd(),folder,file), 'rb')
    pdf=PdfReader(pdfFileObj)
    outpdf.append_pages_from_reader(pdf)
    openFileStreams.append(pdfFileObj)

with open(os.path.join(os.getcwd(),folder, "output.pdf"), 'wb') as pdfTempObj:
                outpdf.write(pdfTempObj)

for stream in openFileStreams:
    stream.close()
