import pandas as pd
import xml.etree.cElementTree as ET
import re


def update_text(text):
    text = re.sub("<.+?>", "", text)
    text = re.sub("&nbsp;", "", text)
    text = re.sub("&\w+;", "", text)
    text = text.replace(u";", ',')
    text = text.replace("\r\n", "")
    return text


def get_dic_from_xml(root):
    min_salary = 'min'
    max_salary = 'max'
    dc = dict()
    child_count = len(root.getchildren())
    regex = "от\s(?P<min>\d+)\s?(до\s(?P<max>\d+))?"
    for i in range(0, child_count):
        for child in root[i].iter():
            if len(child.getchildren()) == 0:
                if child.text is not None:
                    child.text = update_text(child.text)
                if child.tag == 'job-name':
                    child.text = child.text.replace(',', '_')
                if child.tag == "salary" and child.text is not None:
                    p = re.compile(regex)
                    m = p.search(child.text)
                    if m is not None:
                        if min_salary in dc:
                            dc[min_salary][i] = m.group('min')
                        else:
                            dc[min_salary] = [None] * child_count
                            dc[min_salary][i] = m.group('min')
                        if max_salary in dc:
                            dc[max_salary][i] = m.group('max')
                        else:
                            dc[max_salary] = [None] * child_count
                            dc[max_salary][i] = m.group('max')
                if child.tag != "salary":
                    if child.tag in dc:
                        if dc[child.tag][i] is not None:
                            dc[child.tag][i] = str(dc[child.tag][i]) + ', ' + str(child.text)
                        else:
                            dc[child.tag][i] = child.text
                    else:
                        dc[child.tag] = [None] * child_count
                        dc[child.tag][i] = child.text
    return dc


if __name__ == '__main__':
    tree = ET.parse('OBV_full.xml')
    vacancies = tree.getroot()[0]
    df = pd.DataFrame(get_dic_from_xml(vacancies))
    df.to_csv("parsedXML .csv", sep=";", encoding='utf-8-sig')
