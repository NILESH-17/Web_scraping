import requests
from bs4 import BeautifulSoup
import pandas as pd
HEADERS = ({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 'Accept-Language': 'en-US, en;q=0.5'})

def scrape():
    url = "https://www.imdb.com/search/title/?sort=user_rating,desc&groups=top_100"
    response = requests.get(url,headers=HEADERS)
    soup  = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('div', {'class':"ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-be6f1408-9 srahg dli-title"})
    years = soup.findAll('span', {'class':'sc-be6f1408-8 fcCUPU dli-title-metadata-item'})
    ratings = soup.findAll('div',{'class':'sc-e2dbc1a3-0 ajrIH sc-be6f1408-2 dAeZAQ dli-ratings-container'})
    runtimes = soup.findAll('span', {'class':'sc-be6f1408-8 fcCUPU dli-title-metadata-item'})

    title_ = []
    year_ = []
    rating_ = []
    runtime_ = []
    for title in titles:
        t = title.text
        title_.append(t)
    
    for year in years:
            year = year.text
            try:
                year = int(year)
                year_.append(year)
            except:
                None

    for rating in ratings:
        r =  rating.text
        rating_.append(r)
        
    for runtime in runtimes:
        rt = runtime.text
        runtime_.append(rt)
    
    for runtime in runtimes:
        try:
            for r in runtime:
                r = str(r)
                if  not r.isalpha():
                    runtime_.append(r)       
        except:
            None
    for item in runtime_:
        if item == "R" or item == "PG-13" or  item == "Not Rated" or item == "PG" or item == "Approved":
            runtime_.remove(item)

    for item in runtime_:
        
        try:
            item = int(item)
            if item in year_:
                runtime_.remove(item)
        except:
                None
                
    nr = []
    for i in runtime_:
        if len(i) > 4:
            nr.append(i)
    print(len(nr))
    nr_ = nr[0:50]

    df = pd.DataFrame({'title':title_, 'rating': rating_, 'year':year_,'duration':nr_})
    df.title=df.title.str[2:]
    df.title=df.title.str.replace('.','')
    df.rating=df.rating.str[0:3]
    df['rating'] = df['rating'].astype(float)
    print(df)

scrape()
