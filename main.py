from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

soup = BeautifulSoup(requests.get('https://www.questboard.xyz/').text, 'html.parser')
news = soup.find(id='News')
daytexts = news.find_all(id='daytext')
newstexts = news.find_all(id='newstext')
newsjson = {}
for i in range(0, len(daytexts)):
  newsjson[i] = {
    "date": daytexts[i].getText(),
    "content": newstexts[i].getText()
  }





@app.route('/api/noticeboard')
def noticeboard():
  return newsjson

@app.route('/')
def main():
  out_html = ''
  for item in newsjson:
    out_html += f'<span><strong>{newsjson[item]["date"]}:</strong> {newsjson[item]["content"]}</span><br><hr>'
  return render_template('index.html', board=out_html)


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
  req_url = f'https://modelsaber.com/api/v2/get.php?type={modeltype}&sort={sort}&filter={query}&start={page*25}&end={(page+1)*28}'
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
  url = f"https://beatsaver.com/api/search/text/0?q={request.args.get('name')}&minBpm={request.args.get('bpm')}&maxBpm={request.args.get('bpm')}"
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

