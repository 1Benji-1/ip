import os
from flask import Flask, request, render_template_string
import requests
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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


def save_ip_log(ip, country, city, isp):
    user_agent = request.headers.get("user-agent", "No detectado")

    data = {
        "ip": ip,
        "country": country,
        "city": city,
        "isp": isp,
        "user_agent": user_agent
    }

    supabase.table("ip_logs").insert(data).execute()


@app.route("/")
def home():
    ip = get_client_ip()
    info = get_ip_info(ip)

    country = info.get("country_name", "No detectado")
    city = info.get("city", "No detectada")
    isp = info.get("org", "No detectado")

    save_ip_log(ip, country, city, isp)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Detector de IP</title>
    </head>
    <body>
        <h1>Datos aproximados</h1>
        <p><strong>IP:</strong> {{ ip }}</p>
        <p><strong>País:</strong> {{ country }}</p>
        <p><strong>Ciudad:</strong> {{ city }}</p>
        <p><strong>Proveedor:</strong> {{ isp }}</p>
    </body>
    </html>
    """, ip=ip, country=country, city=city, isp=isp)


if __name__ == "__main__":
    app.run(debug=True)
