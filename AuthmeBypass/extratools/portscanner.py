import socket
import threading

class PortScanner:
    def __init__(self, host, start_port, end_port):
        self.host = host
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((self.host, port))
            if result == 0:
                self.open_ports.append(port)
            sock.close()
        except socket.gaierror:
            print(f"Hostname {self.host} could not be resolved.")
        except socket.error:
            print(f"Couldn't connect to server {self.host}")

    def scan_ports(self):
        threads = []
        for port in range(self.start_port, self.end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    host = input("Enter the Minecraft server hostname or IP address: ")
    port_range = input("Enter the port range (e.g., 25565 or 25565-25569 or 25565 25569): ")

    if '-' in port_range:
        start_port, end_port = map(int, port_range.split('-'))
    elif ' ' in port_range:
        start_port, end_port = map(int, port_range.split())
    else:
        start_port = end_port = int(port_range)

    scanner = PortScanner(host, start_port, end_port)
    scanner.scan_ports()

    if scanner.open_ports:
        print(f"Open ports on {host}: {', '.join(map(str, scanner.open_ports))}")
    else:
        print(f"No open ports found on {host} in the range {start_port}-{end_port}")
