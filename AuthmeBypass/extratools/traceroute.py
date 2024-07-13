import sys
from scapy.all import IP, ICMP, sr1

class Traceroute:
    def __init__(self, destination, max_hops=30, timeout=1):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout

    def perform_traceroute(self):
        for ttl in range(1, self.max_hops + 1):
            packet = IP(dst=self.destination, ttl=ttl) / ICMP()
            response = sr1(packet, timeout=self.timeout, verbose=0)

            if response:
                ip_address = response.src
                print(f"{ttl}. {ip_address}")
            else:
                print(f"{ttl}. *")

            if response and ip_address == self.destination:
                break

if __name__ == "__main__":
    destination = input("Enter the destination IP address: ")
    traceroute = Traceroute(destination)
    traceroute.perform_traceroute()
