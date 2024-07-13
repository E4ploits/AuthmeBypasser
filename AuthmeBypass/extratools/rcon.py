import socket

class MinecraftRCON:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def authenticate(self):
        self.send_packet(3, self.password)
        response = self.recv_packet()
        if response[0] != 2:
            raise Exception("Authentication failed")

    def send_packet(self, id, data):
        packet = bytearray()
        packet.extend((id).to_bytes(4, byteorder="little"))
        packet.extend((len(data)).to_bytes(2, byteorder="little"))
        packet.extend(data.encode())
        packet.extend((0).to_bytes(1, byteorder="little"))
        self.socket.send(packet)

    def recv_packet(self):
        id_bytes = self.socket.recv(4)
        id = int.from_bytes(id_bytes, byteorder="little")
        length_bytes = self.socket.recv(2)
        length = int.from_bytes(length_bytes, byteorder="little")
        data = self.socket.recv(length).decode()
        self.socket.recv(1)  # Receive the null terminator
        return id, data

    def execute_command(self, command):
        self.send_packet(2, command)
        response = self.recv_packet()
        return response[1]

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    host = input("Enter the Minecraft server host: ")
    port = int(input("Enter the Minecraft server RCON port: "))
    password = input("Enter the Minecraft server RCON password: ")

    rcon = MinecraftRCON(host, port, password)
    rcon.connect()
    rcon.authenticate()

    while True:
        command = input("Enter a command (or 'exit' to quit): ")
        if command.lower() == "exit":
            break
        response = rcon.execute_command(command)
        print(response)

    rcon.close()
