from machine import Pin, PWM
from hbridge_mod import HBridge
fm = HBridge(Pin(4), Pin(5), pwm=PWM)
sm = HBridge(Pin(2), Pin(0), pwm=PWM)

import socket

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print("listening on", addr)

def process_data(d):
    actions = {
    'q':fm.forward,
    'w':fm.stop,
    'e':fm.backward,
    'a':sm.forward,
    's':sm.stop,
    'd':sm.backward}
    for char in data:
        if char in actions:
            actions[char]()

while True:
    cl, a = s.accept()
    print("client {} accepted".format(a))
    while True:
        data = cl.recv(5)
        if data:
            data = str(data, 'utf8').rstrip('\n')
            process_data(data)
            cl.send(data)
        else:
            print("")
            break
