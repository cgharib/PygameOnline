HOST = ''
PORT = 12800

import socket, sys
from threading import Thread
import pickle

class ThreadClient(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.connexion = conn
        self.resend = True
    def run(self):
        nom = self.getName()
        while 1:
            msgClient = self.connexion.recv(1024)
            try:
                msgClient = pickle.loads(msgClient)
            except:
                self.resend = False
            else:
                self.resend = True



            msgEnvoi = pickle.dumps(msgClient)

            if self.resend == True:
                for cle in conn_client:
                    if cle != nom:
                        conn_client[cle].send(msgEnvoi)


        self.connexion.close()
        del conn_client[nom]
        print("Client {} déconnecté.".format(nom))



mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("Echouééééééééééé")
    sys.exit()
print("Let's Gooooooo")
mySocket.listen(5)

conn_client = {}
while 1:
    connexion, adresse = mySocket.accept()
    th = ThreadClient(connexion)
    th.start()
    it = th.getName()
    conn_client[it] = connexion
    print("Client {0} connecté, adresse IP : {1}, port  : {2}".format(it, adresse[0], adresse[1]))
    connexion.send(b"Connecte.")