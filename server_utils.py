import socket

def get_server_descriptor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect(('127.0.0.1', 25565))
    data = bytes.fromhex('FE')
    sock.send(data)
    rcv = sock.recv(500)

    motd_msg = ''
    for i in range(len(rcv)):
        if rcv[i] == 0 or i == 0 or i == 2:
            continue
        if i > 2:
            motd_msg += chr(rcv[i])

    result = motd_msg.split('§')
    if len(result) == 3:
        return result
    else:
        return None
