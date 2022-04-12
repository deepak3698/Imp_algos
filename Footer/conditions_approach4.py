max_key_value = max(footers_ods.keys())
for i in range(1, len(footers_proof) + 1):
    if i not in footers_ods.keys():
        footers_proof[i] = ""
max_key_value = max(footers_template.keys())
for i in range(1, len(footers_template) + 1):
    if i not in footers_template.keys():
        footers_template[i] = ""
i = 1
j = 1
sequence_page = 0
while i <= len(footers_ods):
    if j < len(footers_ods) and (
            (footers_ods[i] == footers_ods[j] or footers_ods[j] == '') and footers_ods[i] == footers_proof[j + 1]):
        print("footer shrink")

    elif footers_ods[i] == footers_proof[j]:
        print("footer match")
        i += 1
    elif footers_ods[i] != footers_proof[j]:
        print("footer mismatch")
        i += 1
    j += 1
