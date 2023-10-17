import socket
import time

#виды команд:
#user open "file"
#user close
#user save "new name"
#user update
#user delete range
#user insert index text

#Ждем пока пользователь откроет файл
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 3030))
s.sendall('user open file'.encode('utf-8'))
data = s.recv(1024)
print(data.decode('utf-8'))
time.sleep(2)
s.close()

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 3030))
    #если с интерфейса идет какая-то команда, делаем ее,
    #иначе отправляем запрос на обновление

    #если close, то break
    s.sendall('cmd'.encode('utf-8'))
    data = s.recv(1024)
    print(data.decode('utf-8'))
    time.sleep(2)
    s.close()
