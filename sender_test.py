from rawsocketpy import RawSocket , to_str
import time
from multiprocessing import Process
import threading

def send_msg(interface, network, performance, msg):
    sock = RawSocket(interface, 0xEEFA)
    if msg=='Discover':
        sock.send(msg)
        print('\n'+interface+' send: '+msg)
        packet = sock.recv()
        print("Discover-- "+interface+": "+to_str(packet.src))    
    elif msg == 'exit':
        sock.send(msg)
        print('\n'+interface+' send: '+msg)
    else:
        Dmsg = Divide_msg(interface, network, performance, msg)
        sock.send(Dmsg)
        print('\n'+interface+' send: '+Dmsg)

def Divide_msg(interface, network, performance, msg):
    for i in range(len(network)):
        if interface == network[i]:
            start = int(len(msg)*(sum(performance[:i])/sum(performance)))
            end = int(len(msg)*(sum(performance[:i+1])/sum(performance)))
            break
    Dmsg = msg[start:end]
    return Dmsg

def main():
    network = ['eth0', 'wlan0']
    performance = [50,50]

    while True:
        msg = input("\nEnter send message : ")
        procs = []
        for interface in network:
            proc = Process(target=send_msg, args=(interface, network, performance, msg ,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        if msg=='exit':
            print("\nExit message")
            break


if __name__ == '__main__':
    main()


