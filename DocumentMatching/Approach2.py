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
            text_page = page + 1
            for word in text_span_list:

                if word != '':
                    text_split_list.append(
                        {'text': word, 'font_name': font_name, 'font_color': font_color, 'font_size': font_size,
                         'font_shape': font_shape, "text_page": text_page})
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


ods_text_properties_json = get_document_data('doc2.pdf')
virtual_proof_properties_json = get_document_data('doc1_2.pdf')
ods_font_text_list = create_text_slices_for_font_properties(ods_text_properties_json)
virtual_font_text_list = create_text_slices_for_font_properties(virtual_proof_properties_json)

font_compare_iter = 0
issues_list = []
while font_compare_iter < len(virtual_font_text_list):
    #     print(virtual_font_text_list[font_compare_iter],ods_font_text_list[font_compare_iter])
    data_changes = DeepDiff(virtual_font_text_list[font_compare_iter], ods_font_text_list[font_compare_iter])
    #     print("data changes",data_changes)
    if "values_changed" in data_changes.keys():
        single_text_issues = {virtual_font_text_list[font_compare_iter]['text']: []}
        for issue in data_changes['values_changed']:

            if "root['font_color']" == issue:
                issue_key = data_changes['values_changed'][issue]
                issue_dict = {"issue": "font color mismatch", "ods_data": {"color": issue_key['new_value'], "text":
                    ods_font_text_list[font_compare_iter]['text'], "text_page": ods_font_text_list[font_compare_iter][
                    'text_page']},
                              "virtual_proof_data": {"color": issue_key['old_value'],
                                                     "text": virtual_font_text_list[font_compare_iter]['text'],
                                                     "text_page": virtual_font_text_list[font_compare_iter][
                                                         'text_page']}}
                single_text_issues[virtual_font_text_list[font_compare_iter]['text']].append(issue_dict)

            if "root['font_shape']" == issue:
                issue_key = data_changes['values_changed'][issue]
                issue_dict = {"issue": "font shape mismatch", "ods_data": {"font_shape": issue_key['new_value'], "text":
                    ods_font_text_list[font_compare_iter]['text'], "text_page": ods_font_text_list[font_compare_iter][
                    'text_page']},
                              "virtual_proof_data": {"font_shape": issue_key['old_value'],
                                                     "text": virtual_font_text_list[font_compare_iter]['text'],
                                                     "text_page": virtual_font_text_list[font_compare_iter][
                                                         'text_page']}}
                single_text_issues[virtual_font_text_list[font_compare_iter]['text']].append(issue_dict)

            if "root['font_size']" == issue:
                issue_key = data_changes['values_changed'][issue]
                issue_dict = {"issue": "font size mismatch", "ods_data": {"font_size": issue_key['new_value'],
                                                                          "text": ods_font_text_list[font_compare_iter][
                                                                              'text'], "text_page":
                                                                              ods_font_text_list[font_compare_iter][
                                                                                  'text_page']},
                              "virtual_proof_data": {"font_size": issue_key['old_value'],
                                                     "text": virtual_font_text_list[font_compare_iter]['text'],
                                                     "text_page": virtual_font_text_list[font_compare_iter][
                                                         'text_page']}}
                single_text_issues[virtual_font_text_list[font_compare_iter]['text']].append(issue_dict)

            if "root['font_name']" == issue:
                issue_key = data_changes['values_changed'][issue]
                issue_dict = {"issue": "font name mismatch", "ods_data": {"font_name": issue_key['new_value'],
                                                                          "text": ods_font_text_list[font_compare_iter][
                                                                              'text'], "text_page":
                                                                              ods_font_text_list[font_compare_iter][
                                                                                  'text_page']},
                              "virtual_proof_data": {"font_name": issue_key['old_value'],
                                                     "text": virtual_font_text_list[font_compare_iter]['text'],
                                                     "text_page": virtual_font_text_list[font_compare_iter][
                                                         'text_page']}}
                single_text_issues[virtual_font_text_list[font_compare_iter]['text']].append(issue_dict)
        if len(single_text_issues) != 0:
            issues_list.append(single_text_issues)

    font_compare_iter += 1
print(issues_list)