from flask import Flask, render_template, request, redirect, url_for, Response
import subprocess
import os
import signal
import html
import decryptor
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
    mac1 = request.form['MAC1']
    ip2 = request.form['ip2']
    mac2 = request.form['MAC2']
    interface = request.form['iface']

    arp_process = subprocess.Popen(
        ['python', 'ARP_spoofing.py', ip1,mac1, ip2,mac2, interface],
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
            <a class="stop" href="/stop_arp">Stop ARP Spoofing</a>
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
            message = "✅ ARP Spoofing Stopped Successfully!"
        else:
            message = "⚠️ No running ARP spoofing process found."
    except Exception as e:
        message = f"❌ Error stopping spoofing: {e}"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ARP Spoofing Status</title>
        <style>
            body {{
                background: linear-gradient(135deg, #2c3e50, #4ca1af);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }}
            h2, h3 {{
                font-size: 1.8rem;
                text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                margin-bottom: 20px;
            }}
            .back-btn {{
                display: inline-block;
                margin-top: 20px;
                padding: 12px 24px;
                background-color: #00c853;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                box-shadow: 0 0 10px #00c853;
                transition: background-color 0.3s ease;
            }}
            .back-btn:hover {{
                background-color: #00e676;
            }}
        </style>
    </head>
    <body>
        <h2>{message}</h2>
        <a class="back-btn" href="/">⬅ Back to Home</a>
    </body>
    </html>
    """


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
        <a class="stop" href="/stop_dos">🛑 Stop Attack</a>
    </body>
    </html>
    """

@app.route('/stop_dos')
def stop_dos():
    global dos_process
    try:
        if dos_process and dos_process.poll() is None:
            os.kill(dos_process.pid, signal.SIGTERM)
            return """
            <html>
            <head>
                <title>DoS Attack Stopped</title>
                <style>
                    body {
                        background: linear-gradient(135deg, #0d253f, #1e4e79);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        color: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }

                    .container {
                        background: rgba(255, 255, 255, 0.1);
                        padding: 2rem;
                        border-radius: 12px;
                        box-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
                        backdrop-filter: blur(10px);
                        text-align: center;
                    }

                    h2 {
                        color: #00e5ff;
                        font-size: 2rem;
                        text-shadow: 0 0 6px #00e5ff;
                    }

                    p {
                        font-size: 1.2rem;
                        margin-top: 1rem;
                    }

                    a.back {
                        margin-top: 2rem;
                        padding: 12px 25px;
                        background-color: #0288d1;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                        transition: background-color 0.3s ease;
                    }

                    a.back:hover {
                        background-color: #03a9f4;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>✅ DoS Attack Stopped Successfully!</h2>
                    <p>The DoS attack has been successfully stopped. You can go back to the homepage or start another task.</p>
                    <a class="back" href="/">Back to Home</a>
                </div>
            </body>
            </html>
            """
        else:
            return """
            <html>
            <head>
                <title>No Attack Running</title>
                <style>
                    body {
                        background: linear-gradient(135deg, #0d253f, #1e4e79);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        color: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }

                    .container {
                        background: rgba(255, 255, 255, 0.1);
                        padding: 2rem;
                        border-radius: 12px;
                        box-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
                        backdrop-filter: blur(10px);
                        text-align: center;
                    }

                    h2 {
                        color: #ff4e50;
                        font-size: 2rem;
                        text-shadow: 0 0 6px #ff4e50;
                    }

                    p {
                        font-size: 1.2rem;
                        margin-top: 1rem;
                    }

                    a.back {
                        margin-top: 2rem;
                        padding: 12px 25px;
                        background-color: #0288d1;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                        transition: background-color 0.3s ease;
                    }

                    a.back:hover {
                        background-color: #03a9f4;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>❌ No Running DoS Attack Found</h2>
                    <p>It seems there is no active DoS attack to stop at the moment.</p>
                    <a class="back" href="/">Back to Home</a>
                </div>
            </body>
            </html>
            """
    except Exception as e:
        return """
        <html>
        <head>
            <title>Error Stopping DoS</title>
            <style>
                body {
                    background: linear-gradient(135deg, #0d253f, #1e4e79);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }

                .container {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 12px;
                    box-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
                    backdrop-filter: blur(10px);
                    text-align: center;
                }

                h2 {
                    color: #ff4e50;
                    font-size: 2rem;
                    text-shadow: 0 0 6px #ff4e50;
                }

                p {
                    font-size: 1.2rem;
                    margin-top: 1rem;
                }

                a.back {
                    margin-top: 2rem;
                    padding: 12px 25px;
                    background-color: #0288d1;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    transition: background-color 0.3s ease;
                }

                a.back:hover {
                    background-color: #03a9f4;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Error Stopping DoS Attack</h2>
                <p>There was an error while stopping the DoS attack: </p>
                <a class="back" href="/">Back to Home</a>
            </div>
        </body>
        </html>
        """

    

@app.route('/decode', methods=['GET'])
def decode():
    # methods = ['Caesar', 'XOR', 'Base64', 'ROT13', 'Hex', 'K-Word Wraparound', 'RSA']
    methods = ['Caesar', 'XOR', 'Base64', 'RSA']
    return render_template('decode.html', methods=methods)


@app.route('/decrypt_form', methods=['POST'])
def decrypt_form():
    method = request.form['method']
    return render_template('decrypt_form.html', method=method)

@app.route('/decrypt_result', methods=['POST'])
def decrypt_result():
    method = request.form['method']
    ciphertext = request.form['ciphertext']
    result = "Decryption method not found."

    try:
        if method == 'Caesar':
            shift = int(request.form['shift'])
            result = decryptor.caesar_decrypt(ciphertext, shift)

        elif method == 'XOR':
            key = request.form['key']
            result = decryptor.xor_decrypt(ciphertext, key)

        elif method == 'Base64':
            result = decryptor.base64_decrypt(ciphertext)

        elif method == 'ROT13':
            result = decryptor.rot13_decrypt(ciphertext)

        elif method == 'Hex':
            result = decryptor.hex_decrypt(ciphertext)

        elif method == 'K-Word Wraparound':
            keyword = request.form['keyword'].upper()
            result = decryptor.k_word_wraparound(ciphertext, keyword)

        elif method == 'RSA':
            d = request.form.get('d')
            n = request.form.get('n')
            e = request.form.get('e')

            d = int(d) if d else None
            n = int(n) if n else None
            e = int(e) if e else None

            result = decryptor.rsa_decrypt(ciphertext, d=d, n=n, e=e)

    except Exception as e:
        result = f"❌ Error: {e}"

    return render_template('decrypt_result.html', method=method, result=result)



if __name__ == '__main__':
    app.run(debug=True)
