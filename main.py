from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

soup = BeautifulSoup(requests.get('https://questboard.xyz').text, 'html.parser')
for br in soup.find_all("br"):
  br.replace_with("\n")
news = soup.find(id='News')
daytexts = news.find_all(id='daytext')
newstexts = news.find_all(id='newstext')
titletexts = news.find_all(id='newstitle')
newsjson = {}
for i in range(0, len(daytexts)):
  newsjson[i] = {
    "date": daytexts[i].getText(),
    "content": newstexts[i].getText(),
    "title": titletexts[i].getText()
  }


@app.route('/collections')
def collections():
  return render_template('collections.html')

@app.route('/api/collections')
def apicollections():
  page = request.args.get('page')
  html = requests.get('https://hitbloq.com/map_pools/'+page).text
  soup = BeautifulSoup(html, 'html.parser')
  collections = soup.find_all("div", {"class": "ranked-lists-entry-container"})
  colljson = {}
  for i in range(0, len(collections)):
    colljson[i] = {
      "download": "https://hitbloq.com"+collections[i].find("a", {"class": "hashlist-download"})['href'],
      "image": collections[i].find("img", {"class": "ranked-lists-entry-img"})['src'],
      "title": collections[i].find("div", {"class": "ranked-lists-entry-title"}).getText()
    }
  return colljson

@app.route('/api/ssscrape')
def ssscrape():
  PHPSESSID = requests.get('https://scoresaber.com').cookies['PHPSESSID']
  cat = request.args.get('cat')
  sort = request.args.get('sort')
  star = request.args.get('maxStar')
  star1 = request.args.get('minStar')
  page = request.args.get('page')
  verified = request.args.get('verified')
  ranked = request.args.get('ranked')
  if verified == 'true':
    verified = '1'
  if ranked == 'true':
    ranked = '1'
  if ranked == 'false':
    ranked = '0'
  if verified == 'false':
    verified = '0'
  cookie_dict = {
    'cat': cat,
    'dark': '0',
    'sort': sort,
    'star': star,
    'star1': star1,
    'PHPSESSID': PHPSESSID,
    'verified': verified,
    'ranked': ranked
  }
  req_u_1 = f'https://scoresaber.com/imports/user-setting.php?verified={verified}&ranked={ranked}&sort={sort}&cat={cat}&star={star}&star1={star1}'
  requests.get(req_u_1)
  html = requests.get('https://scoresaber.com?page='+page, cookies=cookie_dict).text
  soup = BeautifulSoup(html, 'html.parser')
  songs = soup.find('tbody')
  songs = songs.find_all('tr')
  songJson = {}
  for i in range(0, len(songs)):
    songJson[i] = {
      "image": songs[i].find("td", class_="song").find('img')['src'],
      "name": songs[i].find("td", class_="song").find('a').getText().strip(),
      "difficulty": songs[i].find("td", class_="difficulty").getText().strip(),
      "author": songs[i].find("td", class_="author").find('a').getText().strip(),
      "total_plays": songs[i].find("td", class_="scores").getText().strip(),
      "plays_pastday": songs[i].find("td", class_="percentage").getText().strip(),
      "stars": songs[i].find("td", class_="stars").getText().strip()
    }

  return songJson






@app.route('/api/noticeboard')
def noticeboard():
  return newsjson

@app.route('/')
def main():
  out_html = ''
  for item in newsjson:
    out_html += f'<span><strong>{newsjson[item]["title"]}</strong><br><span style="color:#FDFFFC">{newsjson[item]["date"]}</span><br><br> {newsjson[item]["content"]}</span><br><hr>'
  return render_template('testing.html', board=out_html)


@app.route('/api/maps')
def apimaps():
  sort = request.args.get('sort')
  page = request.args.get('page')
  query = request.args.get('query')
  chroma = request.args.get('chroma')
  ranked = request.args.get('ranked')
  noodle = request.args.get('noodle')
  if query is None:
    req_url = f"https://api.beatsaver.com/search/text/{page}?sortOrder={sort}"
  else:
    req_url = f"https://api.beatsaver.com/search/text/{page}?q={query}&sortOrder={sort}&chroma={chroma}&noodle={noodle}&ranked={ranked}"
  print(req_url)
  return requests.get(req_url).json()


@app.route('/api/models')
def apimodels():
  sort = request.args.get('sort')
  query = request.args.get('query')
  page = int(request.args.get('page'))
  modeltype = request.args.get('type')
  direction = request.args.get('direction')
  req_url = f'https://modelsaber.com/api/v2/get.php?type={modeltype}&sort={sort}&filter={query}&start={page*26}&end={(page+1)*26}&sortDirection={direction}'
  print(req_url)
  r = requests.get(req_url)
  return r.json()

@app.route('/scoresaber')
def scoresaber():
  return render_template('scoresaber.html')

@app.route('/api/scoresaber')
def apiscoresaber():
  page = int(request.args.get('page'))+1
  cat = request.args.get('cat')
  req_url = f'http://scoresaber.com/api.php?function=get-leaderboards&cat={cat}&page={page}&limit=14'
  print(req_url)
  r = requests.get(req_url)
  return r.json()


@app.route('/api/downloadscoresaber')
def downloadscoresaber():
  url = f"https://beatsaver.com/api/search/text/0?q={request.args.get('name')}"
  r = requests.get(url)
  id = r.json()['docs'][0]['id']
  print(id)
  return 'beatsaver://'+id

@app.route('/maps')
def maps():
  return render_template('maps.html')

@app.route('/models')
def models():
  return render_template('models.html')

@app.route('/testing')
def testing():
  return render_template('testing.html')


@app.route('/api/saberimg')
def saberimg():
  id = request.args.get('id')
  data = 'empty'
  png = requests.get(f'https://modelsaber.com/files/saber/{id}/image.png')
  if png.status_code == 200:
    data = png.raw
  jpg = requests.get(f'https://modelsaber.com/files/saber/{id}/image.jpg')
  if jpg.status_code == 200:
    data = jpg.raw
  gif = requests.get(f'https://modelsaber.com/files/saber/{id}/image.gif')
  if gif.status_code == 200:
    data = gif.raw
  print(data)
  return data


app.run(host='0.0.0.0', port=8080)

