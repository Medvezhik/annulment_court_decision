from airflow.operators.python import PythonOperator
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from airflow import DAG
import requests
import datetime
import random
import shutil
import time
import docx
import os

dir_doc = "/home/user/sud/doc/"
dir_info = "/home/user/sud/info/"
dir_case = "/home/user/sud/case/"

def get_from_url(fn, url):
    if(os.path.exists(fn)):
        print(fn)
        return open(fn, 'rb').read()
    
    time.sleep(random.randint(1, 3))
    ua = UserAgent()
    header = {'User-Agent':str(ua.random)}
    responce = requests.get(url, verify=False, headers=header)
    print(url, responce.status_code)

    if responce.status_code == 200:
        if fn != '':
            file = open(fn, 'wb')
            file.write(responce.content)
            file.close()
        return responce.text
    else:
        return ''

def parse_list(content):
    res = []
    soup = BeautifulSoup(content, 'lxml')
    table = soup.body.find('table', {"class": "custom_table"})
    for row in table.tbody.childGenerator():
        if(row.name=='tr'):
            url = row.find('a')
            print(url['href'])
            res.append(url['href'])
    return res

def parse_case(content):
    res = []
    soup = BeautifulSoup(content, 'lxml')
    table = soup.body.find('div', {'class', 'cardsud_wrapper'})
    if table.find('a') != None:
        url = table.find('a')['href']
        return 'https://www.mos-gorsud.ru' + url
    return ''

def parse_info(content):
    soup = BeautifulSoup(content, 'lxml')
    table = soup.body.find('table', {'class', 'custom_table mainTable'})
    for row in table.tbody.childGenerator():
        if row.name == 'tr':
            key = cut_word(row.find_all('td')[1].text)
            if(key == 'Мотивированноерешение'):
                if row.find('a') != None:
                    url = row.find('a')['href']
                    if url != '#':
                        return 'https://www.mos-gorsud.ru' + url
    return ''

def cut_word(text):
    return text.replace(' ','').replace('\n', '')

def get_page(page, date1, date2):
    n = 0
    
    content = get_from_url('', f'https://mos-gorsud.ru/mgs/search?caseDateFrom=&caseDateTo=&caseFinalDateFrom={date1}&caseFinalDateTo={date2}&caseLegalForceDateFrom=&caseLegalForceDateTo=&caseNumber=&letterNumber=&category=&codex=&courtAlias=mgs&docsDateFrom=&docsDateTo=&documentStatus=&documentText=&documentType=&instance=2&judge=&participant=&processType=2&publishingState=&uid=&year=&formType=fullForm&page={page}')

    try:
        cases = parse_list(content)
    except:
        return True

    for case in cases:
        n += 1
        name = str(page).zfill(5)+str(n).zfill(2)
        content = get_from_url(dir_case + name + '.htm', 'https://mos-gorsud.ru'+case)
        url = parse_case(content)
        if url != '':
            info = get_from_url(dir_info + name + '.htm', url)
            url = parse_info(info)
            if url != '':
                get_from_url(dir_doc + name + '.doc', url)
                
    return False

def get_info(name):
    d = {}
    file = open(name, encoding='utf8')
    content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.body.find('div', {'class', 'cardsud_wrapper'})
    for row in table.childGenerator():
        if row.name!=None:        
            key = row.find_all('div')[0].text
            val = row.find_all('div')[1].text
            key = key.replace(' ','').replace('\n', '')
            val = val.replace('"', ' ').replace('«', ' ').replace('»', ' ').replace(',', ' ').replace('\n', '')
            val = val.strip()
            #print(key, val)
            d[key] = val
    return d

def getd(d, key):
    if key in d:
        return d[key]
    else:
        return ''

def download():
    try:
        os.mkdir(dir_doc)
        os.mkdir(dir_info)
        os.mkdir(dir_case)
    except FileExistsError:
        print("FileExistsError")
        
    page = 1
    date1 = datetime.date.today()-datetime.timedelta(days=14)
    date2 = datetime.date.today()-datetime.timedelta(days=6)
    
    done = False
    while not done:
        try:
            done = get_page(page, date1.strftime('%d.%m.%Y'), date2.strftime('%d.%m.%Y'))
            #done = True
        except:
            print("exception", page)
            time.sleep(1)
        else:
            page +=1

def make_csv():
    file = open('/home/user/sud/mosgorsud.csv', 'w', encoding='utf-8')
    file.write('id,side,date1,date2,category,status,verdict,verdict_up,reason,text\n')

    files = sorted(os.listdir(dir_doc))
    for name in files:
        if name.endswith('.doc'):
            text = os.popen(f'antiword {dir_doc + name}').read()
            if text=='':
                try:
                    doc = docx.Document(dir_doc + name)
                    for p in doc.paragraphs:
                        text += p.text + ' '
                except:
                    print('not open', name)
                else:
                    print('docx', name)
                
            if text=='':
                continue
        
            d = get_info(dir_info + name[0:8] + 'htm')
            file.write(getd(d, 'Уникальныйидентификатордела') + ',')
            file.write(getd(d, 'Стороны') + ',')
            file.write(getd(d, 'Датапоступления') + ',')
            file.write(getd(d, 'Датарассмотренияделавпервойинстанции') + ',')
            file.write(getd(d, 'Категориядела') + ',')
            file.write(getd(d, 'Текущеесостояние') + ',')
            file.write(getd(d, 'Решениеапелляции') + ',')        

            d = get_info(dir_case + name[0:8] + 'htm')
            file.write(getd(d, 'Результатрассмотрения') + ',')
            file.write(getd(d, 'Основаниерешениясуда') + ',')                
    
            text = text.replace('"', ' ').replace('«', ' ').replace('»', ' ').replace('\n', ' ')
            file.write('"' + text + '"\n')
        
    file.close()

    shutil.rmtree(dir_case)
    shutil.rmtree(dir_info)
    shutil.rmtree(dir_doc)

    
with DAG(dag_id='mosgorsud_weekly_dag', start_date=datetime.datetime(2022, 10, 20, 6, 0), end_date=datetime.datetime(2022, 10, 26, 6, 0), schedule="0 6 * * 7") as dag:
    download_operator = PythonOperator(task_id='download', python_callable=download)
    make_csv_operator = PythonOperator(task_id='make_csv', python_callable=make_csv)

    download_operator >> make_csv_operator
    