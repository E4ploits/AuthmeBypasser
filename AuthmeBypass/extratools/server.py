import requests
import json

class MinecraftServerInfo:
    def __init__(self, server_address):
        self.server_address = server_address
        self.info = {}

    def get_server_info(self):
        try:
            response = requests.get(f"https://api.mcsrvstat.us/2/{self.server_address}", timeout=5)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

        try:
            data = response.json()
            self.info["online"] = data["online"]
            self.info["players"] = data["players"]["online"]
            self.info["max_players"] = data["players"]["max"]
            self.info["motd"] = data["motd"]["clean"]
            self.info["version"] = data["version"]
            self.info["protocol"] = data["protocol"]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None

        return self.info

    def print_server_info(self):
        if self.info:
            print(f"Server: {self.server_address}")
            print(f"Online: {self.info['online']}")
            print(f"Players: {self.info['players']}/{self.info['max_players']}")
            print(f"MOTD: {self.info['motd']}")
            print(f"Version: {self.info['version']}")
            print(f"Protocol: {self.info['protocol']}")
        else:
            print("Failed to retrieve server information.")

if __name__ == "__main__":
    server_address = input("Enter the Minecraft server address (e.g., example.com:25565): ")
    server_info = MinecraftServerInfo(server_address)
    server_info.get_server_info()
    server_info.print_server_info()
