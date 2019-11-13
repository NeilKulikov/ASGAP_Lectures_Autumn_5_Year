import os
import re
from PyPDF2 import PdfFileReader, PdfFileWriter

pattern = r'[\w /]+MagneticField\d\d\d'

def handle_walk(step):
    folder_path = step[0]
    patm = re.match(pattern, folder_path)
    if patm != None:
        file_path = folder_path + '/main.pdf'
        if os.path.exists(file_path):
            return file_path

def targets_in_directory(dir):
    fps = [handle_walk(d) for d in os.walk(dir)]
    fps = list(filter(lambda x: x != None, fps))
    return sorted(fps)

def open_pdf_streams(files):
    input_streams = []
    try:
        input_streams = [open(f, 'rb') for f in files]
    except:
        return None
    return input_streams

def handle_pdf_readers(rdrs, wrtr):
    for n in range(rdrs.getNumPages()):
        wrtr.addPage(rdrs.getPage(n))

if __name__ == "__main__":
    root = os.getcwd()
    fps = targets_in_directory(root)
    pdfs = open_pdf_streams(fps)
    reds = map(PdfFileReader, pdfs)
    wrtr = PdfFileWriter()
    for rd in reds:
        handle_pdf_readers(rd, wrtr)
    outp = open(root + '/full.pdf', 'wb')
    wrtr.write(outp)
    outp.close()
    for fs in pdfs:
        fs.close()
    
    
    

