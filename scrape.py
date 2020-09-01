import requests
import os
import sys
import datetime
import pandas as pd
from requests_html import HTML

BASE_DIR=os.path.dirname(__file__)


def url_to_txt(url,filename='world.html',save=False):
    r=requests.get(url)
    if r.status_code==200:
        html_text=r.text
        if save:
            with open("world-{}.html".format(start_year),'w') as f:
                f.write(html_text)
        return html_text
    return None 


def parse_and_extract(url,name):
    html_text=url_to_txt(url)
    if html_text==None:
        return 
    r_html=HTML(html=html_text)
    table_class= ".imdb-scroll-table"
    r_table=r_html.find(table_class)
    table_data=[]
    if len(r_table)==0:
        return False
    parsed_table=r_table[0]
    rows=parsed_table.find('tr')
    header_row=rows[0]
    header_cols=header_row.find('th')
    header_names=[x.text for x in header_cols]
    for row in rows[1:]:
        cols=row.find('td')
        row_data=[]
        for col in cols:
            row_data.append(col.text)
        table_data.append(row_data)
        #to conver scrapped data into csv
    df=pd.DataFrame(table_data,columns=header_names)
    path=os.path.join(BASE_DIR,'data')              #To create directory
    os.makedirs(path,exist_ok=True)
    filepath=os.path.join('data',f'{name}.csv')
    df.to_csv(filepath,index=False)
    return True

def run(start_year=None,years_ago=10):
    if start_year==None:
        now=datetime.datetime.now()
        start_year=now.year
    assert isinstance(start_year,int)
    assert len(str(start_year))==4
    for i in range(0,years_ago+1):
        url='https://www.boxofficemojo.com/year/world/{}/'.format(start_year)  
        finished=parse_and_extract(url,name=start_year)
        if finished:
            print('Finished {}'.format(start_year))
        else:
            print('Not Found {}'.format(start_year))
        start_year-=1 

if __name__ == "__main__":
    
    start,count=sys.argv[1],sys.argv[2]
    try:
        start=int(start)
    except:
        start=None
    try:
        count=int(count)
    except:
        count=1
    run(start_year=start,years_ago=count)