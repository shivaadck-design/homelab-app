from flask import Flask
import datetime
import socket
import MySQLdb

app = Flask(__name__)

def get_db():
    return MySQLdb.connect(
        host="mysql-db",
        user="homelab",
        password="homelab123",
        database="homelabdb"
    )

@app.route('/')
def home():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT message, created_at FROM messages ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        db.close()
        messages = "".join([f'<div class="info"><label>{r[1]}</label> {r[0]}</div>' for r in rows])
    except Exception as e:
        messages = f'<div class="info">Database connecting... {str(e)}</div>'

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask + MySQL App</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }}
            .card {{ background: white; padding: 30px; border-radius: 8px; max-width: 600px; margin: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #1d3557; }}
            .info {{ background: #e8f4f8; padding: 10px; border-radius: 4px; margin: 10px 0; }}
            label {{ font-weight: bold; color: #457b9d; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Flask + MySQL on Docker!</h1>
            <div class="info"><label>Hostname:</label> {socket.gethostname()}</div>
            <div class="info"><label>Time:</label> {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</div>
            <h2>Messages from Database:</h2>
            {messages}
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
