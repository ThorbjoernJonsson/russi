import socket
from _thread import *
import pickle
from game import Game
from Deck import *

server = "192.168.1.96"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(('', port))
    #s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId, deck):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data == "False":
                        game.not_redraw()
                    elif data == "score":
                        game.update_score()
                    elif data == "first":
                        game.update_curr_player(p)
                    elif data[0:4] == "flip":
                        print (data)
                        print (p)
                        game.flip_card(data, p)
                    elif data != 'get':
                        game.play(data, p)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2

    deck = Deck()
    for i in range(3):
        deck.Shuffle()

    if idCount % 2 == 1:
        games[gameId] = Game(gameId, deck)
        #deck = games[gameId].deck
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        deck = games[gameId].deck
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId, deck))
