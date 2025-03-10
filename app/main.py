from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import ipaddress

app = FastAPI()

CLOUDFLARE_IP_RANGES = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
]
# todo: add logging
def is_cloudflare_ip(ip):
    try:
        ip_addr = ipaddress.ip_address(ip)
        return any(ip_addr in ipaddress.ip_network(cidr) for cidr in CLOUDFLARE_IP_RANGES)
    except ValueError:
        return False

@app.get("/")
async def get_ip(request: Request):
    # Основные данные
    client_ip = request.client.host
    cf_ip = request.headers.get("CF-Connecting-IP", "Not provided")
    cf_check = is_cloudflare_ip(client_ip)
    
    # Все заголовки
    headers = dict(request.headers.items())
    
    # Формируем ответ
    response_data = {
        "ip_info": {
            "client_ip": client_ip,
            "cf_connecting_ip": cf_ip,
            "is_cloudflare_proxy": cf_check
        },
        "headers": headers,
        "cloudflare_ranges": CLOUDFLARE_IP_RANGES
    }
    
    return JSONResponse(content=response_data)