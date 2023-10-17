import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('localhost', 3030))
s.listen(1)
while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    if not data:
        continue
    t = data.decode('utf-8')
    print(t)
    #если запрос на обновление, то отправляем текущую версию файла
    #conn.sendall((t[:6] + ', слушаю вас').encode('utf-8'))
conn.close()