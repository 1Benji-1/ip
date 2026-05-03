from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)


def get_client_ip():
    ip = request.headers.get("x-forwarded-for", request.remote_addr)

    if ip:
        ip = ip.split(",")[0].strip()

    return ip


def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        return response.json()
    except requests.RequestException:
        return {}


@app.route("/")
def home():
    ip = get_client_ip()
    info = get_ip_info(ip)

    country = info.get("country_name", "No detectado")
    city = info.get("city", "No detectada")
    isp = info.get("org", "No detectado")

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Detector de IP</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }

            .card {
                background: white;
                padding: 25px;
                border: 1px solid #ddd;
                border-radius: 10px;
                width: 320px;
            }

            h1 {
                font-size: 22px;
                margin-bottom: 15px;
            }

            p {
                margin: 8px 0;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Datos aproximados</h1>
            <p><strong>IP:</strong> {{ ip }}</p>
            <p><strong>País:</strong> {{ country }}</p>
            <p><strong>Ciudad:</strong> {{ city }}</p>
            <p><strong>Proveedor:</strong> {{ isp }}</p>
        </div>
    </body>
    </html>
    """, ip=ip, country=country, city=city, isp=isp)


if __name__ == "__main__":
    app.run(debug=True)
