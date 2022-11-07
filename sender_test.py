from rawsocketpy import RawSocket , to_str
import time
from multiprocessing import Process
import threading
import os

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

def find_network():
    stream = os.popen('ifconfig -s').read().split('\n')
    network = []
    for i in range(len(stream)-1):
        re = stream[i].split(' ')
        #In Resberry
        if re[0]=='Iface' or re[0]=='lo':
            continue
        network.append(re[0])
    return network

def net_pf(network):
    performance = []
    for i in range(len(network)):
        performance.append(50)
    return performance

def main():
    network = find_network()
    performance = net_pf(network)

    #first Discover server MAC Address
    procs = []
    for interface in network:
        proc = Process(target=send_msg, args=(interface, network, performance, 'Discover' ,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

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


