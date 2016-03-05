from flask import Flask, render_template, request, redirect
import numpy as np

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

if __name__ == '__main__':
  app.run(host='0.0.0.0')
