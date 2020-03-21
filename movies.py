from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import json
moviesDict = {}
# create a user agent to fake a browser visit
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}
i = 1
page = 1
MoviesInfo = {}
MoviesInfo['movies'] = []
while (page < 1484):
    url = 'https://30nama.cool/movies/page/'+str(page)
    # get url using UA
    cinama = requests.get(url, headers=header)
    soup = BeautifulSoup(cinama.text, 'html.parser')
    # find every single movie post on the page
    posts = soup.findAll(class_='post')
    # select a post and open it for scraping data
    for post in posts:
        # get title in post (main page)
        title = post.find('h2')
        print(title.text)
        # get image url
        imgLink = post.find('img').attrs['src']
        # get post url
        movieurl = post.a.attrs['href']
        # fetch whole movie page into a var
        moviepage = requests.get(movieurl, headers=header)
        parsedPage = BeautifulSoup(moviepage.text, 'html.parser')
        # get summery
        summery = parsedPage.find(id="tab_fa").p.text
        # get left column
        leftCol = parsedPage.find(id='info-left')
        # get right column
        rightCol = parsedPage.find(id='info-right')
        # variables
        Genre = []
        Year = ''
        Director = ''
        Metacritic = ''
        Actors = ''
        IMDb = ''
        RottenTomatoes = ''
        Lang = ''
        # get movies info :D
        genre = leftCol.find(class_='info')
        atag = genre.findAll('a')
        # get all genres
        for a in atag:
            Genre.append(a.text)
            titleWithoutYear = title.text
        # check for datas like diuration, actor, director, country, year of release,rates(imdb,rotten,metacritic),lang
        try:
            if(leftCol.find(text='سال انتشار')):
                getYear = leftCol.find(text='سال انتشار').findNext('bdi')
                Year = getYear.text
        except:
            Year = ''
        try:
            if(leftCol.find(text='کارگردان')):
                getDirector = leftCol.find(text='کارگردان').findNext('bdi')
                Director = getDirector.text
        except:
            Director = ''
        try:
            if(leftCol.find(text='بازیگران اصلی')):
                Actors = leftCol.find(
                    text='بازیگران اصلی').findNext('bdi').text
        except:
            Actors = ''
        try:
            if(rightCol.find(text='امتیاز Metacritic')):
                getMetacritic = rightCol.find(
                    text='امتیاز Metacritic').findNext('em')
                Metacritic = getMetacritic.text
        except:
            Metacritic = ''
        try:
            if(leftCol.find(text='امتیاز Rotten Tomatoes')):
                getRottenTomatoes = leftCol.find(
                    text='امتیاز Rotten Tomatoes').findNext('em')
                RottenTomatoes = getRottenTomatoes.text
        except:
            RottenTomatoes = ''
        try:
            if(leftCol.find(text='امتیاز IMDb')):
                getIMDb = leftCol.find(text='امتیاز IMDb').findNext('em')
                IMDb = getIMDb.text
        except:
            IMDb = ''
        try:
            if(rightCol.find(text='محصول کشور')):
                getCountry = rightCol.find(text='محصول کشور').findNext('a')
                Country = getCountry.text
        except:
            Country = ''
        try:
            secDiv = rightCol.findAll(class_='info')
            langText = secDiv[1]
            if(langText.find(text='زبان انیمیشن / شامل زبان های')):
                Lang = langText.text.replace(
                    'زبان انیمیشن / شامل زبان های', '')
            elif(langText.find(text='زبان فیلم / شامل زبان های')):
                Lang = langText.text.replace('زبان فیلم / شامل زبان های', '')
        except:
            lang = ''
        # if(i != 10 and i != 11 and i != 17 and i != 19):
        try:
            thirddiv = rightCol.findAll(class_='info')
            if(thirddiv[2].find(text='مدت زمان')):
                time = thirddiv[2].text
                time = time.replace('مدت زمان', '')
            else:
                time = 'none'
        except:
            time = 'none'
        MoviesInfo['movies'].append({"title": titleWithoutYear, "Year": Year, "Genre": Genre, "Actors": Actors, "DIrector/s": Director, "Metacritic": Metacritic,
                                     "IMDb": IMDb, "RottenTomatoes": RottenTomatoes, "image link": imgLink, "Summery": summery, "Lang": Lang, "time": time, "country": Country})
        print(str(i)+'-'+title.text + " added")
        i += 1
        # write movie data into a json file
        with open("MoviesInfo.json", "w", encoding='utf-8') as writeJSONmovies:
            json.dump(MoviesInfo, writeJSONmovies,
                      ensure_ascii=False, indent=4)
    page += 1

