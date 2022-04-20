import fitz
from deepdiff import DeepDiff


def flags_decomposer(flags):
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)


def get_document_data(path):
    doc = fitz.open(path)
    document_details = []
    for page in doc:

        page_data = []
        blocks = page.get_text("dict", flags=11)["blocks"]

        for b in blocks:
            for l in b['lines']:
                for s in l['spans']:
                    page_data.append(s)
                    font_properties = "Font: '%s' (%s), size %g,color #%06x" % (
                    s['font'], flags_decomposer(s['flags']), s['size'], s['color'])
        document_details.append(page_data)
    return document_details


doc1 = get_document_data('doc2.pdf')
doc2 = get_document_data('doc1_2.pdf')
DeepDiff(doc1, doc2)
