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
  if query is None:
    req_url = f"https://api.beatsaver.com/search/text/{page}?sortOrder={sort}"
  else:
    req_url = f"https://api.beatsaver.com/search/text/{page}?q={query}&sortOrder={sort}"
  print(req_url)
  return requests.get(req_url).json()


@app.route('/api/models')
def apimodels():
	notType = request.args.get('type') 
	id = request.args.get('id')
	if id:
		r = requests.get("https://modelsaber.com/api/v2/get.php?type="+notType).json()
		return r[id]
	else:
		return requests.get("https://modelsaber.com/api/v2/get.php?start=1&end=25&type="+notType).text

	
@app.route('/maps')
def maps():
  return render_template('maps.html')

@app.route('/models')
def models():
  return render_template('models.html')

@app.route('/testing')
def testing():
  return render_template('testing.html')
  
app.run(host='0.0.0.0', port=8080)

