import socket
import concurrent.futures
import requests

def scan_port(ip: str, port: int, timeout: int = 1) -> int:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return port if result == 0 else None
    except Exception:
        return None

def port_scan(target: str, start_port: int, end_port: int, threads: int = 100) -> list:
    open_ports = []
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        return []
        
    ports_to_scan = range(start_port, end_port + 1)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports_to_scan}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
                
    return sorted(open_ports)

def get_ip_info(ip: str) -> dict:
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None
