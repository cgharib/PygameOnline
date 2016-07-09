import socket, sys
import pickle
from threading import Thread
import pygame

host = "localhost"
port = 12800

class ReceptionMessage(Thread):
    def __init__(self, co):
        Thread.__init__(self)
        self.connexion = co

    def run(self):
        while 1:
            msg_recu = self.connexion.recv(1024)
            try:
                msg_recu = pickle.loads(msg_recu)
                affichage.pos_perso2 = msg_recu
            except:
                pass

class Affichage:
    def __init__(self):
        self.perso = pygame.Surface((32, 32))
        self.perso.fill((255, 0, 0))
        self.pos_perso = self.perso.get_rect()
        self.screen = pygame.display.set_mode((640, 480))
        self.perso2 = pygame.Surface((32, 32))
        self.perso2.fill((0, 255, 0))


    def deplacer(self, direction):
        if direction == "bas":
            self.pos_perso = self.pos_perso.move(0, 3)
        if direction == "haut":
            self.pos_perso = self.pos_perso.move(0, -3)
        if direction == "gauche":
            self.pos_perso = self.pos_perso.move(-3, 0)
        if direction == "droite":
            self.pos_perso = self.pos_perso.move(3, 0)

    def afficher(self):
        self.screen.fill((255, 255, 255))
        try:
            self.screen.blit(self.perso2, self.pos_perso2)
        except:
            self.screen.blit(self.perso2, (0, 0))
        self.screen.blit(self.perso, self.pos_perso)
        pygame.display.flip()


class EnvoiMessage(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.connexion = conn

    def run(self):
        while 1:
            msg_envoi = pickle.dumps(affichage.pos_perso)
            self.connexion.send(msg_envoi)


connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print("Echouééééé")
    sys.exit()
print("Connexion établiiiiiiiiiiie.")

th1 = EnvoiMessage(connexion)
th2 = ReceptionMessage(connexion)
affichage = Affichage()

th1.start()
th2.start()

pygame.key.set_repeat(10)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                affichage.deplacer("bas")
            if event.key == pygame.K_UP:
                affichage.deplacer("haut")
            if event.key == pygame.K_RIGHT:
                affichage.deplacer("droite")
            if event.key == pygame.K_LEFT:
                affichage.deplacer("gauche")
    affichage.afficher()



