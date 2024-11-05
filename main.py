from collections import defaultdict
import csv
import re
from pprint import pprint



with open("phone_book_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

def corect_fio(list_fio):
    full_fio = ' '.join(list_fio).strip().split()
    if len(full_fio) == 1:
        return [full_fio, '', '']
    elif len(full_fio) == 2:
        return [full_fio[0], full_fio[1], '']
    else:
        return full_fio

correct_dict = {}

for data in contacts_list:
    fio = corect_fio(data[:3])
    x = []
    for info in data:
        pattern = r'(\+7|8)?\s*\(?([4][9][5])\)?[\s-]*([\d+]{3})[\s-]*([\d+]{2})[\s-]*(\d+)'
        sub_pattern = r'+7(\2)\3-\4-\5'
        intermediate_result = re.sub(pattern, sub_pattern, info)
        pattern = r'\(?([д|Д][о|О][б|Б])\W\s*(\d{4})\)?'
        sub_pattern = r'\1.\2.'
        result = re.sub(pattern, sub_pattern, intermediate_result)
        x.append(result)
    person_info = fio + x[3:]
    if f'{fio[:2]}' in correct_dict.keys():
        new_contact = [x if x != '' else y for x, y in zip(correct_dict[f'{fio[:2]}'], person_info)]
        correct_dict[f'{fio[:2]}'] = new_contact
    else:
        correct_dict[f'{fio[:2]}'] = person_info

with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(correct_dict.values())