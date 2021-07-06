#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from TeXooPy.texoopy.model import Dataset
from uuid import uuid4
import json
import codecs


def create_document(col, text, prod_type):
    if text:
        if isinstance(text, float):
            return
        text = text.replace('\n', ' ').replace('\\n', ' ').replace('\\t', ' ').replace('\"', '').strip()
        if text[0] == 'b':
            text = text[2:-1].strip()
            l = []

        doc = {
            'id': str(uuid4()),
            'title': col,
            'language': 'de',
            'text': text,
            'length': len(text),
            'class': 'Document',
            'type': str(prod_type).strip()
        }
        return doc


sets = ['training', 'test']
columns = ['Grund der Anforderung', 'Ausgeführte Arbeiten', 'Gerätedaten:Typ']
for set in sets:
    data = pd.read_pickle(set+'_data.pkl')
    data = data.filter(columns)
    dataset = {
                'name': 'krohne_servicetickets_'+set,
            }
    documents = []
    for d in data.iterrows():
        d = d[1]
        for i in range(0, 2):
            col = columns[i]
            text = d[col]
            prod_type = d[columns[2]]
            doc = create_document(col, text, prod_type)
            if doc:
                documents.append(doc)


    dataset['documents'] = documents
    dataset['language'] = 'de'
    texoo_ds = Dataset.Dataset.from_json(json_data=dataset)
    dict_ds = json.dumps(texoo_ds.to_texoo_dict(), default=lambda o: o.to_texoo_dict(), indent=4, ensure_ascii=False).encode('utf8')
    texoo_out = codecs.open('Data/krohne_servicetickets_'+set+'_texoo.json', 'w', 'utf-8-sig')
    texoo_out.write(dict_ds.decode())
    texoo_out.close()
