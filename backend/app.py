from flask import Flask, render_template
import socket
from requests import get 
import speedtest   
import os
import uuid
from networkdevices import detect_devices


app = Flask(__name__)

def conn_status():
    status = "Disconnected"
    return_code = os.system("ping 8.8.8.8 -n 2")
    if return_code == 0:
        status = "Connected"
    else:
        status = "Disconnected"
    return status


def get_mac():
    mac = uuid.getnode()
    mac_addr = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_addr

def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    return ip

@app.route('/')
def index():
    return ("""
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Manager</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            text-align: center;
        }

        header {
            background-color: #3498db;
            color: #fff;
            padding: 20px;
        }

        section {
            margin: 20px;
        }

        footer {
            background-color: #333;
            color: #fff;
            # padding: 10px;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>

<body>
    <header>
        <h1>View Important Network Details</h1>
    </header> <br>
  <button style="background-color: #4caf50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;"><a href="http://127.0.0.1:5000/home" style="color: inherit; text-decoration: none;">Check Network Stats</a></button>


    <footer>
        All rights reserved.
    </footer>
</body>

</html>

""")

@app.route('/home')
def home():
    status = conn_status()
    print(status)
    mac = get_mac()
    if status == "Disconnected":
        return f"""
        <p><b style="color: #555;">Connection Status:</b> {status}</p>
    <p><b style="color: #555;">MAC of Interface:</b> {mac}</p>
    <p><b>Connect to a network for more options</b></p>
        """
    ip = get_ip()
    publicIp = get('https://api.ipify.org').content.decode('utf8')
    print("Home")
    return f"""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Basic Stats</title>
</head>

<body style="font-family: 'Arial', sans-serif; margin: 20px; padding: 20px; background-color: #f8f8f8;">

    <h1 style="color: #333; text-align: center;">Basic Stats</h1>

    <p><b style="color: #555;">Connection Status:</b> {status}</p>
    
    <p><b style="color: #555;">Local IP of the machine:</b> {ip}</p>

    <p><b style="color: #555;">Public IPv4 Address:</b> {publicIp}</p>
    
    <p><b style="color: #555;">MAC of Interface:</b> {mac}</p>

    <button style="background-color: #4caf50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
        <a href="speedcheck" style="color: white; text-decoration: none;" onclick="document.getElementById('ptag').innerHTML='Loading...'">Check Speed</a>
    </button>
    <p id="ptag"><p>
    <button style="background-color: #4caf50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
        <a href="/devices" style="color: white; text-decoration: none;" onclick="document.getElementById('ptag2').innerHTML='Loading...'">Scan Devices on Network</a>
    </button>
    <p id="ptag2"><p>
</body>

</html>
  

"""

@app.route('/speedcheck')
def speed():
    print("loading....")
    st = speedtest.Speedtest()
    download_speed = st.download()/1000000
    upload_speed = st.upload()/1000000
    return f"""
    <div style="text-align: center; padding: 20px; background-color: #f8f8f8;">
        <h2>Speed Test Results</h2>
        <p><b>Download Speed:</b> {download_speed} MB/s</p>
        <p><b>Upload Speed:</b> {upload_speed} MB/s</p>
    </div>
"""

@app.route('/devices')
def devices():
    print("/devices Endpoint Triggered...")
    ipsmac = detect_devices()
    print(ipsmac)
    return f"""
    <h3>Devices Found: </h3>
    { ipsmac }
"""

if __name__ == '__main__':
    app.run(debug=True)
