import docx
import re


def drop_junk_words(text):
    text1 = text.replace("российской федерации", "")
    text2 = text1.replace("соответствии", "")
    text3 = text2.replace(" ст ", "")
    text4 = text3.replace(" гк ", "")
    text5 = text4.replace(" рф ", "")
    text6 = text5.replace(" в ", "")
    text7 = text6.replace(" с ", "")
    text8 = text7.replace("размере", "")
    text9 = text8.replace("а также", "")
    text10 = text9.replace("также", "")
    text11 = text10.replace("решение", "")
    text12 = text11.replace("р е ш е н и е", "")
    text13 = text12.replace("уид", "")
    text14 = text13.replace("именем", "")
    text15 = text14.replace("№", " ")
    text16 = text15.replace("город", " ")
    text17 = text16.replace("города", " ")
    return text17


def drop_case_num(text):
    return " ".join(re.sub(r"\d-\d{1,4}\/\d{2,4}", " ", text.lower()).split())


def drop_case_uid(text):
    return " ".join(re.sub(r"\S{8}-\d{2}-\d{4}-\d{6}-\d{2}", " ", text.lower()).split())


def drop_dates(text):
    return " ".join(re.sub(r"\d{1,2}\.\d{1,2}\.\d{2,4}", " ", text.lower()).split())


def read_doc_file(path):
    doc = docx.Document(path)
    text = ""
    for p in doc.paragraphs:
        text += p.text
    text = text.replace('"', " ").replace("«", " ").replace("»", " ").replace("\n", " ")
    return text


def process_text(text: str):
    text = drop_case_num(text)
    text = drop_case_uid(text)
    text = drop_dates(text)
    text = drop_junk_words(text)
    return text


def process_doc_file(path):
    return process_text(read_doc_file(path))
