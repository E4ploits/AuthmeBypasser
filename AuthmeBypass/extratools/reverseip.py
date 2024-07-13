import requests

class ReverseIP:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.info = {}

    def lookup(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip_address}", timeout=5)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

        try:
            data = response.json()
            self.info["country"] = data["country"]
            self.info["region"] = data["regionName"]
            self.info["city"] = data["city"]
            self.info["isp"] = data["isp"]
            self.info["org"] = data["org"]
            self.info["as"] = data["as"]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None

        return self.info

    def print_lookup(self):
        if self.info:
            print(f"IP Address: {self.ip_address}")
            print(f"Country: {self.info['country']}")
            print(f"Region: {self.info['region']}")
            print(f"City: {self.info['city']}")
            print(f"ISP: {self.info['isp']}")
            print(f"Organization: {self.info['org']}")
            print(f"AS: {self.info['as']}")
        else:
            print("Failed to perform reverse IP lookup.")

if __name__ == "__main__":
    ip_address = input("Enter the IP address: ")
    reverse_ip = ReverseIP(ip_address)
    reverse_ip.lookup()
    reverse_ip.print_lookup()
