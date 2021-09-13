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
	if sort == "plays":
		return requests.get("https://api.beatsaver.com/maps/plays/"+page).text
	elif sort == "latest":
		return requests.get("https://api.beatsaver.com/maps/latest").text


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

  
app.run(host='0.0.0.0', port=8080)

