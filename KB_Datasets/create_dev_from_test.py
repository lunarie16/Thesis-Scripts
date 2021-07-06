import json
from TeXooPy.texoopy.model import Dataset
import codecs
from uuid import uuid4
import os
from icecream import ic



f_test = open('krohne_servicetickets_test_texoo', 'r')
test = json.load(f_test)
data = [test]
dataset = {
            'name': 'krohne_servicetickets',
        }
documents = []
i = 0
for d in data:
    for title in d.values():
        docu = []
        g_type = ''
        for key in title.keys():
            if key == 'Gerätedaten_Typ':
                g_type = title[key]
                if g_type:
                    g_type = g_type.strip()
            else:
                doc = {
                    'id': str(uuid4()),
                    'title': key.replace('_', ' '),
                    'language': 'de',
                    'text': title[key].replace('\n', ' ').strip(),
                    'length': len(title[key]),
                    'class': 'Document',
                    'type': g_type
                }
                if doc['text']:
                    # documents.append(doc)
                    docu.append(doc)
                else:
                    continue
        if (i % 2) != 0:
            for do in docu:
                documents.append(do)
        i += 1


dataset['documents'] = documents
dataset['language'] = 'de'
texoo_ds = Dataset.Dataset.from_json(json_data=dataset)
dict_ds = json.dumps(texoo_ds.to_texoo_dict(), default=lambda o: o.to_texoo_dict(), indent=4, ensure_ascii=False).encode('utf8')

texoo_out = codecs.open('Data/krohne_servicetickets_dev_texoo.json', 'w', 'utf-8-sig')
texoo_out.write(dict_ds.decode())
texoo_out.close()
