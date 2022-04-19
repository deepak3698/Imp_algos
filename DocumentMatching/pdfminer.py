from io import StringIO


def parse_obj(objs):
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:
                if isinstance(o, pdfminer.layout.LTTextLine):
                    text = o.get_text()
                    if text.strip():
                        for c in o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                print("fontname %s" % c.fontname)
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)
        else:
            pass


def pdf_to_text(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    laparams = LAParams()
    converter = TextConverter(manager, output, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, converter)

    #     laparams = LAParams()
    device = PDFPageAggregator(manager, laparams=laparams)
    interpreter_out = PDFPageInterpreter(manager, device)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
        interpreter_out.process_page(page)
    layout = device.get_result()
    print(layout)
    print(parse_obj(layout._objs))
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    result = []
    for line in text.split('\n'):
        line2 = line.strip()
        if line2 != '':
            result.append(line2)
    return result


pdf_to_text("doc1.pdf")