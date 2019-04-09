from flask import Flask, render_template, request
import pandas, requests, json
import os
from werkzeug import secure_filename
app = Flask(__name__)

def my_function(file):
    df = pandas.read_csv(file)
    i = 0
    f = open("newdata.csv", "w")
    email=[]
    score=[]
    domain=[]
    for i in range(50):
        response = requests.get("https://api.hunter.io/v2/email-finder?company="+df['Company'][i]+"&full_name="+df['First Name'][i]+"+"+df['Last Name'][i]+"&api_key=69627572b4be56acc2632b128fa5e9e48a3d7022")
        ef = pandas.read_json(response.content)
        email.append(ef['data']['email'])
        domain.append(ef['data']['domain'])
        score.append(ef['data']['score'])
        if(email[i]!=None):
          f.write(str(email[i])+"--")
          f.write(str(domain[i])+"--")
          f.write(str(score[i])+"\n")
    os.remove(file)
    return render_template('results.html', email=email, score=score)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return my_function(f.filename)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/extract')
def my_link():
  return my_function()

if __name__ == '__main__':
  app.run(debug=True)