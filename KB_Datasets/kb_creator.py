from TeXooPy.texoopy.model import Dataset, Document
from uuid import uuid4
import json
import os
import codecs
from langdetect import detect
from statistics import mode


f_in='../Krohne_WP/files/products_description.json'
kb='Data/krohne_products_description_texoo.json'
with open(f_in, 'r', encoding="UTF-8") as json_file:
    if not os.path.exists('Data'):
        os.makedirs('Data')
    name = f_in.split('/')[-1].split('.')[0]
    data = json.load(json_file)
    dataset = {
        'name': name,
    }
    languages = []
    documents = []
    for title, text in data.items():
        title = title.split('-')
        language = detect(text)
        doc = {
            'id': str(uuid4()),
            'title': title[-1],
            'language': language,
            'text': text,
            'type': title[0].replace('ue', 'ü').replace('oe', 'ö').replace('produkt', 'Produkt'),
            'length': len(text),
            'class': 'Document'
        }
        documents.append(doc)
        languages.append(language)
    dataset['documents'] = documents
    dataset['language'] = mode(languages)
    texoo_ds = Dataset.Dataset.from_json(json_data=dataset)
    dict_ds = json.dumps(texoo_ds.to_texoo_dict(), default=lambda o: o.to_texoo_dict(), ensure_ascii=False, indent=4).encode('utf8')

    texoo_out = codecs.open(kb, 'w', 'utf-8-sig')
    texoo_out.write(dict_ds.decode())
    texoo_out.close()
