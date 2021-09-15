from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def main():
  return render_template('index.html')


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
  req_url = f'https://modelsaber.com/api/v2/get.php?type={modeltype}&sort={sort}&filter={query}&start={page*25}&end={(page+1)*25}'
  print(req_url)
  r = requests.get(req_url)
  return r.json()


	
@app.route('/maps')
def maps():
  return render_template('maps.html')

@app.route('/models')
def models():
  return render_template('models.html')

@app.route('/testing')
def testing():
  return render_template('testing.html')

@app.route('/info')
def info():
  return render_template('info.html')

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

