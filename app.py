from flask import Flask, render_template, request, redirect, url_for, Response
import subprocess
import os
import signal
import html
app = Flask(__name__)
arp_process = None  # Global reference to manage stopping
dos_process = None  # Global reference to manage DoS attack

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_attack():
    attack_type = request.form['attack']
    if attack_type == 'arp':
        return redirect(url_for('arp_form'))
    elif attack_type == 'dos':
        return redirect(url_for('dos_form'))
    return "Invalid attack type"

# ARP Attack routes (same as before)
@app.route('/arp_form')
def arp_form():
    return render_template('arp_form.html')

@app.route('/run_arp', methods=['POST'])
def run_arp():
    global arp_process
    ip1 = request.form['ip1']
    ip2 = request.form['ip2']
    interface = request.form['iface']

    arp_process = subprocess.Popen(
        ['python', 'ARP_spoofing.py', ip1, ip2, interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        errors='replace',
        bufsize=1,
        universal_newlines=True
    )

    with open('arp_pid.txt', 'w') as f:
        f.write(str(arp_process.pid))

    def generate():
        yield """
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; font-family: monospace; padding: 20px; }
                pre { background-color: #111; border-left: 4px solid #03a9f4; padding: 1rem; overflow-x: auto; max-height: 80vh; }
                a.stop { display: inline-block; margin-top: 20px; padding: 10px 20px; background-color: red; color: white; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h2>ARP Spoofing Output</h2>
            <pre>
        """

        for line in arp_process.stdout:
            cleaned_line = html.escape(line.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
            yield cleaned_line.replace("\n", "<br>")

        yield """
            </pre>
            <a class="stop" href="/stop_arp" target="_blank">Stop ARP Spoofing</a>
        </body>
        </html>
        """

    return Response(generate(), mimetype='text/html')

@app.route('/stop_arp')
def stop_arp():
    global arp_process
    try:
        if arp_process and arp_process.poll() is None:
            os.kill(arp_process.pid, signal.SIGTERM)
            return "<h2>ARP Spoofing Stopped Successfully!</h2>"
        else:
            return "<h3>No running ARP spoofing process found.</h3>"
    except Exception as e:
        return f"<h3>Error stopping spoofing: {e}</h3>"

# DoS Attack routes
dos_process = None  # Global reference

@app.route('/dos_form')
def dos_form():
    return render_template('dos_form.html')

@app.route('/run_dos', methods=['POST'])
def run_dos():
    global dos_process
    ip = request.form['ip']
    port = request.form['port']
    rate_limit = request.form['rate_limit']
    data_size = request.form['data_size']
    threads = request.form['threads']

    # Launch DoS script with command-line args
    dos_process = subprocess.Popen(
        ['python', 'Dos.py', ip, port, rate_limit, data_size, threads],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Save PID to file for future use (optional)
    with open('dos_pid.txt', 'w') as f:
        f.write(str(dos_process.pid))

    return """
    <html>
    <head>
        <title>DoS Attack</title>
        <style>
            body {
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
                font-family: Arial, sans-serif;
                color: white;
                text-align: center;
                padding: 50px;
            }
            a.stop {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #000;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h2>🚀 Initiating DoS Attack...</h2>
        <a class="stop" href="/stop_dos" target="_blank">🛑 Stop Attack</a>
    </body>
    </html>
    """

@app.route('/stop_dos')
def stop_dos():
    global dos_process
    try:
        if dos_process and dos_process.poll() is None:
            os.kill(dos_process.pid, signal.SIGTERM)
            return "<h2>✅ DoS Attack Stopped Successfully!</h2><a href='/'>Back</a>"
        else:
            return "<h3>No running DoS attack found.</h3>"
    except Exception as e:
        return f"<h3>Error stopping DoS attack: {e}</h3>"


if __name__ == '__main__':
    app.run(debug=True)
