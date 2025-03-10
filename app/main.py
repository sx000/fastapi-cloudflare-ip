from fastapi import FastAPI, Request
import ipaddress

app = FastAPI()

# Официальные IP Cloudflare
CLOUDFLARE_IP_RANGES = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
]

# Функция проверки, что IP - Cloudflare
def is_cloudflare_ip(ip):
    try:
        ip_addr = ipaddress.ip_address(ip)
        return any(ip_addr in ipaddress.ip_network(cidr) for cidr in CLOUDFLARE_IP_RANGES)
    except ValueError:
        return False

@app.get("/")
async def get_ip(request: Request):
    client_ip = request.client.host  # IP, с которого пришёл запрос
    cf_ip = request.headers.get("CF-Connecting-IP", "pizdec")  # Реальный IP пользователя через Cloudflare

    cf_check = is_cloudflare_ip(client_ip)  # Проверяем, действительно ли запрос идёт через Cloudflare

    return f"""
    <h2>IP Информация</h2>
    <pre>
    Client IP (request.client.host): {client_ip}
    CF-Connecting-IP: {cf_ip}
    Проверка Cloudflare: {"Да" if cf_check else "Нет"}
    </pre>
    """
