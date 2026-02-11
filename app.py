from flask import Flask, request,render_template_string
import sqlite3
from datetime import datetime

app=Flask(__name__)

#---DATABASE SETUP---
def init_db():
  conn=sqlite3.connect('Marathonic.db')
  c=conn.cursor()
  c.execute("CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,runner TEXT,miles REAL,time TEXT)")
  conn.commit()
  conn.close()

#---THE WEBPAGE(HTML)---
@app.route('/')
def index():
  conn=sqlite3.connect('Marathonic.db')
  c=conn.cursor()
  # Get all runs,newest first
  c.execute("SELECT runner,miles,date FROM runs ORDER BY id DESC")
  runs=c.fetchall()

  #Calculate Leaderboard Totals
  totals ={}
  for run in runs:
    name=run[0]
    dist=run[1]
    totals[name]=totals.get(name,0)+dist

  conn.close()

  # The Hacker-Themed Interface
  html="""
  <!DOCTYPE html>
  <html>
  <head>
    <title>MARATHONIC // SYSTEM</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
      body { font-family:'Courier New',monospace; background-color:#0d0d0d; color;#00ff41; text-align:
center; padding: 10px;}
      h1 {border-bottom 2px solid #00ff41;display:inline-block;text-transform:uppercase;
letter-spacing:2px;}
      .container{max-width:600px;margin:0 auto;}

      /*CARDS*/
      .card {background:#1a1a1a;border:1px solid #333;padding:15px;margin-bottom: 15px;
border-radius: 4px; box-shadow:0 0 15px rgba(0,255,65,0.05);}
      h3{background:#1E90FF; color:#000; display: inline-block;padding: 2px 8px; margin-top 0;
font-size:0.9em;}

      /*INPUTS*/
      input{background:#000; border:1px solid #1E90FF; color:#fff; padding:12px; width:90%; margin:90%; margin:
5px 0; font-family:inherit; font-size:21px;}
      button{background:#; color:1E90ff; border:none; padding:15px; width:95%; font-weight:bold; cursor:pointer; font-size:1.1em; text-transform:uppercase;
margin-top:10px;}

      /*DATA ROWS*/
      .stat-row{display:flex; justify-content:space-between; font-size:1.2em; padding:8px 0;
border-bottom: 1px dashed #333;}
      .log-row{font-size:0.8em; color:#888; text-align:left; padding:5px 0; border-bottom:1px solid #222;}
      .highlight{color:#fff; font-weight:bold;}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Marathonic_v1</h1>

      <div class="card">
        <h3>>>SYSTEM STATUS:ONLINE</h3>
        {% for name,total in totals.items() %}
        <div class="stat-row">
          <span>{{name}}</span>
          <span class="highlight">{{"%.1f"|format(total)}}mi</span>
        </div>
        {%endfor%}
      </div>

      <div class="card">
        <h3>>> INGEST DATA</h3>
        <form action="/log_manual" method="post">
          <input type="text" name="runner" placeholder="OPERATOR NAME" required>
          <input type="number" step="0.1" name="miles" placeholder="DISTANCE(MILES)" required>
          <button type="submit">UPLOAD</button>
        </form>
      </div>

      <div class="card">
        <h3>>>RECENT LOGS</h3>
        {%for run in runs%}
        <div class="log-row">
          >[{{run[2]}}]<b>{{run[0]}}</b>:{{run[1]}}mi
        </div>
        {%endfor%}
      </div>
    </div>
  </body>
  </html>
  """

  return render_template_string(html,runs=runs,totals=totals)

# --- API FOR IPHONE SHORTCUTS ----
@app.route('/api/log',methods=['POST'])
def log_api():
  data=request.json
  runner=data.get('runner')
  miles=data.get('miles')

  if not runner or not miles:
     return{"status":"error"},400

  conn=sqlite3.connect('Marathonic.db')
  c=conn.cursor()
  c.execute("INSERT INTO runs (date,runner,miles,time)VALUES(?,?,?,?)",
       (datatime.now().strftime("%Y-%m-%d %H:%M"),runner,miles,"Auto"))
  conn.commit()
  conn.close()
  return{"status":"success","message":f"Logged{miles}for{runner}"}

# --- MANUAL LOGGING ROUTE ---
@app.route('/log_manual',methods=['POST'])
def log_manual():
  runner=request.form.get('runner')
  miles=request.form.get('miles')
  
#---SECURITY CHECK---
  if not runner or not miles:
      return "ERROR:Missing Data",400
    
  try:
    f_miles=float(miles)
    if f_miles<=0 or f_miles>100:
      return "ERROR:Invalid Distance(Must be 0-100)",400
  except ValueError:
    return "ERROR:Miles must be a number",400
    #---------------------
    

  conn=sqlite3.connect('Marathonic.db')
  c=conn.cursor()
  c.execute("INSERT INTO runs(date,runner,miles,time) VALUES(?,?,?,?)",
       (datetime.now().strftime("%Y-%m-%d %H:%M"),runner,miles,"Manual"))
  conn.commit()
  conn.close()
  return '<meta http-equiv="refresh" content="0; url=/">'

if __name__=='__main__':
  init_db()
  # Host 0.0.0.0 allows other devices on your wifi to see it
  app.run(host='0.0.0.0',port=5000)
