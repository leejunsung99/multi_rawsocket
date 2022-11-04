
from tkinter import OUTSIDE
from rawsocketpy import RawRequestHandler, RawAsyncServerCallback
import time
from rawsocketpy import get_hw, to_str, protocol_to_ethertype, to_bytes, to_int
from rawsocketpy import HashChaining
from multiprocessing import Process
import threading

H= HashChaining(17)
#dic={}
def callback(handler, server):
    print("Testing")
    handler.setup()
    handler.handle()
    handler.finish()

def User_name(packet,data):
    OUI = to_int(to_str(packet.src[1:3]))
    UUA = to_int(to_str(packet.src[3:5]))
    return H.set_name(OUI,UUA,msg=data)    

class LongTaskTest(RawRequestHandler):
    def handle(self):
        time.sleep(1)
        #print(self.packet)
        #print User Name
        data = self.packet.data.decode('utf-8')
        user = User_name(self.packet,data)
        #try:
        #    dic[user]+=data
        #except:
        #    dic[user]=data


        print(to_str(self.packet.src)+"-->"+ user)
        print(user+' send:  '+data)
        #print(H)

    def finish(self):
        print("End\n")

    def setup(self):
        print("Begin") 

def lets_start(interface):
    rs = RawAsyncServerCallback(interface, 0xEEFA, LongTaskTest, callback)
    rs.spin()    

def main():
    network = ['eth0', 'wlan0']
    procs = []
    for interface in network:
        proc = Process(target=lets_start, args=(interface, ))
        procs.append(proc)
        proc.start()

    #for interface in network:
    #    proc = threading(target=lets_start, args=(interface, ))
    #    procs.append(proc)
    #    proc.start()

    for proc in procs:
        proc.join()

if __name__ == '__main__':
    main()
