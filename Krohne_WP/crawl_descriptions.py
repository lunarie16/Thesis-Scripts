from bs4 import BeautifulSoup
import bs4
from icecream import ic
import os
import json
# -*- coding: iso-8859-1 -*-
from urllib import parse
import re

directory = ('files/urls/')
if not os.path.exists(directory):
    os.makedirs(directory)

descriptions = {}
no_descriptions = {}
for filename in os.listdir(directory):
    f_name = filename.split('_')
    name = f_name[-1].split('.')[0].replace('-', ' ')
    prod_type = f_name[0]

    with open(directory + filename) as t:
        bs = BeautifulSoup(t, 'lxml')
        div = bs.find('div', id='uebersicht')
        description = ''
        if div:
            for siblings in div.next_siblings:
                if len(siblings) > 1:
                    for child in siblings.children:
                        if len(child) > 1:
                            for c in child:
                                li_elem = ''
                                if isinstance(c, bs4.element.Tag):
                                    for li in c.findAll('li'):
                                        li_elem += li.text.strip()
                                        if li_elem[-1].strip() != '.':
                                            li_elem += '. '

                                if li_elem:
                                    description += li_elem
                                else:
                                    if not c.string:
                                        c = c.text
                                    else:
                                        c = c.string
                                    if c:
                                        if len(c) > 100 and (c != 'Mehr anzeigen'):
                                            c = c.strip()
                                            description += c


        if not description:
            no_descriptions[prod_type.capitalize()+'-'+name.upper()] = 'NO DESCRIPTION'
        else:
            descriptions[prod_type.capitalize()+'-'+name.upper()] = description.replace('\xa0', ' ').strip()


with open('files/products_description.json', 'w', encoding='UTF-8') as f_out:
    json.dump(descriptions, f_out, indent=2, ensure_ascii=False)
    f_out.close()

with open('files/products_no_description.json', 'w', encoding='UTF-8') as ff_out:
    json.dump(no_descriptions, ff_out)
    ff_out.close()
