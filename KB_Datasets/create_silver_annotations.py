import json
import re
import codecs
from TeXooPy.texoopy.model import NamedEntityAnnotation, Annotation, Dataset
import os

sets = ['train', 'test', 'dev']
for set in sets:
    kb = json.load(codecs.open('Data/krohne_products_description_texoo.json', 'r', 'utf-8-sig'))
    data = json.load(codecs.open('krohne_servicetickets_'+set+'_texoo', 'r', 'utf-8-sig'))
    product_names = set()
    for doc in kb['documents']:
        product_names.add((doc['title'].lower().replace(' ', ''), doc['id']))

    for text in data['documents']:
        t = text['text']
        matches = re.findall(r'([A-Z]+\s*[a-z]*\s*\d+\s*[CFLPSW]*\s*'
                             r'[STDHN]*\s*(Ex)*\d*\s?)', t)
        for match in matches:
            m = match.strip().lower().replace(' ', '')
            for name, name_id in product_names:
                if name.lower().replace(' ', '') in m:
                    ix = [m.start() for m in re.finditer(match.strip(), t)]
                    for idx in ix:
                        annotation: NamedEntityAnnotation = {
                            "begin": idx,
                            "length": len(match.strip()),
                            "text": match.strip(),
                            "source": "SILVER",
                            "refId": name_id,
                            "class": "NamedEntityAnnotation"
                             }
                        if annotation and (annotation not in text['annotations']):
                            text['annotations'].append(annotation)

    texoo_ds = Dataset.Dataset.from_json(json_data=data)
    dict_ds = json.dumps(texoo_ds.to_texoo_dict(), default=lambda o: o.to_texoo_dict(), indent=4, ensure_ascii=False).encode('utf8')
    texoo_out = codecs.open('Data/krohne_servicetickets_'+set+'_annotations_texoo.json', 'w', 'utf-8-sig')
    texoo_out.write(dict_ds.decode())
    texoo_out.close()
