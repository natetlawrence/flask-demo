from flask import Flask, render_template, request, redirect
import numpy as np
import requests
import pandas as pd
from bokeh.plotting import figure, show, output_file, vplot

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/nprand')
def nprand():
  return str(np.random.rand())

@app.route('/index_lulu')
def index_lulu():
    return render_template('userinfo_lulu.html')

@app.route('/tickerplot')
def tickerplot():
  symbol = 'FB'
  field = u'Open'
  r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/{}.json'.format(symbol))
  rjson = r.json()
  if rjson.has_key('dataset'):
      dataset = r.json()['dataset']
  else:
      print 'Error retrieving Quandl data. That may not be a valid stock ticker symbol.'

  df = pd.DataFrame(dataset['data'],columns=dataset['column_names'])
  items = 30

  return '\n'.join(list(df['Adj. Open']))
  #p1 = figure(x_axis_type = "datetime")
  #p1.title = "Stock Opening Prices"
  #p1.grid.grid_line_alpha=0.3
  #p1.xaxis.axis_label = 'Date'
  #p1.yaxis.axis_label = 'Price'

  #p1.line(np.array(df['Date'],dtype=np.datetime64), df['Adj. Open'], color='#A6CEE3', legend=symbol)

  # output_file("stocks.html", title="readstockprice.py example")
  # show(vplot(p1))  

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
