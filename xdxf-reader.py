!/usr/bin/env python
# -*- coding: utf-8 -*-
# Аuthor: Bakrivo A.R. e-mail: turkin86@mail.ru
import sys
import xml.etree.ElementTree as ET


class XDXFReader(object):
    """docstring for XDXFReader"""

    def __init__(self, xdxf_file):
        super(XDXFReader, self).__init__()
        self.full_name = ''
        self.lang_from = ''
        self.lang_to = ''
        self.xdxf_file = xdxf_file
        self.__xdxf_dict = self.__read()

    def __set_info(self, root):
        full_name = root.find('full_name').text
        if full_name:
            self.full_name = full_name
        self.lang_from = root.get('lang_from')
        self.lang_to = root.get('lang_to')

    def __read(self):
        tree = ET.parse(self.xdxf_file)
        root = tree.getroot()
        self.__set_info(root)

        dict_data = {}

        for ar in root.iter('ar'):
            ard = {}
            for a in ar:
                if a.tag == 'k':
                    ard[a.tag] = a.text.replace('&', '&amp;')
                if a.tag == 'tr':
                    ard[a.tag] = a.text
            if ard:
                ar_tag = ET.tostring(
                    ar, encoding='utf-8').decode('utf-8').strip()
                ar_tag = ar_tag.replace(
                    '<k>{0}</k>'.format(ard.get('k')), '')
                ar_tag = ar_tag.replace(
                    '<tr>{0}</tr>'.format(ard.get('tr')), '')
                ar_clr_text = ET.fromstring(ar_tag).text
                if ar_clr_text:
                    dict_data[ard.get('k')] = {
                        'tr': ard.get('tr'), 'ar': ar_clr_text}
                else:
                    print(ard)
                    print("Error parse tag ar: %s" % ar_tag)
        return dict_data

    def name(self, name):
        return self.full_name

    def count(self):
        return len(self.__xdxf_dict)

    def data(self):
        return self.__xdxf_dict.copy()

    def get(self, name):
        return self.__xdxf_dict.get(name)

    def keys(self):
        return self.__xdxf_dict.keys()

    def update(self):
        self.__xdxf_dict = self.__read()

    def search_keys(self, value):
        return [s for s in self.keys() if value in s]
