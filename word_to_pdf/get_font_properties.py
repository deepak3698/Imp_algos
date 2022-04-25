import fitz
import re
from deepdiff import DeepDiff
def create_text_slices_for_font_properties(docs):
    text_split_list = []
    for page in range(0, len(docs)):
        for line in docs[page]:

            #             text_span_list=line['text'].split()
            text_span_list = re.findall(r"[\w']+|[.,!?;]", line['text'])
            font_size = line['size']
            font_name = line['font']
            font_color = line['color']
            font_shape = line['flags']
            origin_text = line['origin']
            bbox_text = line['bbox']
            text_page = page + 1
            for word in text_span_list:

                if word != '':
                    text_split_list.append(
                        {'text': word, 'font_name': font_name, 'font_color': font_color, 'font_size': font_size,
                         'font_shape': font_shape, "text_page": text_page,
                         'origin': origin_text, 'bbox': bbox_text})
    return text_split_list


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


file_data = get_document_data('template.pdf')
data_dict = create_text_slices_for_font_properties(file_data)