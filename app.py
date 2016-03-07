from flask import Flask, render_template, request, redirect
import numpy as np
import requests
import pandas as pd
from bokeh.plotting import figure, save, output_file, vplot

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
  return redirect('/tickersubmit')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/nprand')
def nprand():
  return str(np.random.rand())

@app.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
    nquestions=5
    if request.method == 'GET':
        return render_template('userinfo_lulu.html',num=nquestions)
    else:
        #request was a POST
        app.vars['name'] = request.form['name_lulu']
        app.vars['age'] = request.form['age_lulu']

        f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'w')
        f.write('Name: %s\n'%(app.vars['name']))
        f.write('Age: %s\n\n'%(app.vars['age']))
        f.close()

        return 'request.method was not a GET!'

@app.route('/tickersubmit',methods=['GET','POST'])
def tickersubmit():
  if request.method == 'GET':
    return render_template('tickerplot_input.html')
  else:
    app.vars['tickersymbol'] = request.form['ticker_name']
    return redirect('/tickerplot')
    #return app.vars['tickersymbol']

@app.route('/tickerplot')
def tickerplot():
  symbol = app.vars['tickersymbol']
  # symbol = 'FB'
  field = u'Open'
  r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/{}.json'.format(symbol))
  rjson = r.json()
  if rjson.has_key('dataset'):
      dataset = r.json()['dataset']
  else:
      print 'Error retrieving Quandl data. That may not be a valid stock ticker symbol.'

  df = pd.DataFrame(dataset['data'],columns=dataset['column_names'])
  items = 30

  #return '\n'.join(df['Adj. Open'][0:30].astype(str))
  p1 = figure(x_axis_type = "datetime")
  p1.title = "Stock Opening Prices"
  p1.grid.grid_line_alpha=0.3
  p1.xaxis.axis_label = 'Date'
  p1.yaxis.axis_label = 'Price'

  p1.line(np.array(df['Date'],dtype=np.datetime64), df['Adj. Open'], color='#A6CEE3', legend=symbol)

  output_file("templates/stocks.html", title="readstockprice.py example")
  save(vplot(p1)) 
  #return render_template('stocks.html')
  with open('templates/stocks.html') as file:
    return file.read()

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
