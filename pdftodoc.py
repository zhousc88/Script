# -*- coding: utf-8 -*-
# author:zhousc
#Email:zhousc88@gmail.com

from  pdfminer.pdfparser import PDFParser,PDFDocument
from  pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def  parse():
    fn=open(r'1.pdf','rb')
    parser=PDFParser(fn)
    doc=PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    resource=PDFResourceManager()
    laparams=LAParams()
    device=PDFPageAggregator(resource,laparams=laparams)
    interpreter=PDFPageInterpreter(resource,device)
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout=device.get_result()
        for out in layout:
            if hasattr(out,"get_text"):
                with open('1.doc','ab') as f:
                    outtext=out.get_text().encode('utf-8')
                    #print(dir(str()))
                    print(type(outtext))
                    f.write(outtext)
              
if __name__=='__main__':
    parse()