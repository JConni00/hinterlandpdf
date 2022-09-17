from flask import Flask

import io
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
# pdf mining
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

def pdfparser(target_url="https://pexam-storage.b-cdn.net/hinterland/skill-based-cv.pdf"):
    data = ''
    # fp = open(data, 'rb')
    # get_url= urllib.request.urlopen('https://pexam-storage.b-cdn.net/lecture_1.pdf')
    # fp = get_url.read()

    remote_file = urlopen(Request(target_url)).read()
    fp = io.BytesIO(remote_file)
    # fp = PdfFileReader(memory_file)

    # print("Response Status: "+ str(get_url.getcode()) )
    # fp = get_url.open()
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    print("TEXT")
    print(data)
    sentences = nltk.sent_tokenize(data) #tokenize sentences
    print(sentences)
    nouns = [] #empty to array to hold all nouns

    for sentence in sentences:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
               nouns.append(word)

    return nouns

@app.route('/', methods=["GET"])
def hello_world():
    return pdfparser()