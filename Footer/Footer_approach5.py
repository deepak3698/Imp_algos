ods_footers = [{'page_no': 1, 'footer': "footer1"}, {'page_no': 2, 'footer': "footer2"}]
template_footers = [{'page_no': 1, 'footer': "footer1"}, {'page_no': 2, 'footer': "footer1"},
                    {'page_no': 3, 'footer': "footer5"}]

ods_footers_dict = {}
for i in ods_footers:
    ods_footers_dict[i['footer']] = i['page_no']
unique_ods_footers = list(ods_footers_dict.keys())

template_footers_dict = {}
for i in template_footers:
    template_footers_dict[i['footer']] = i['page_no']
unique_template_footers = list(set(template_footers_dict.keys()))

print(unique_ods_footers, unique_template_footers)
for i in unique_ods_footers:
    if i in unique_template_footers:
        unique_template_footers.remove(i)
    else:
        print("footer at page " + str(ods_footers_dict[i]) + " of proof is not found in template")

for i in unique_template_footers:
    if i not in ods_footers_dict.keys():
        print("new footer " + str(template_footers_dict[i]) + " found in template ")



