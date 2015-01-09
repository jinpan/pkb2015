import argparse
import socket
import sys


import lib


"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player(object):
    def __init__(self):
        self.game = None
        self.hand = None
        self.history = []

    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            print data

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            msg = data.split()
            msg_type = msg[0]
            if msg_type == "NEWGAME":
                self.game = lib.Game(*data.split()[1:])

            elif msg_type == "NEWHAND":
                card1 = data.split()[3]
                card2 = data.split()[4]

                self.game.hand = [card1, card2]
            elif msg_type == "GETACTION":
                self.getaction(msg)

            elif msg_type == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

    def getaction(self, msg):
        # GETACTION potSize numBoardCards [boardCards] [stackSizes] numActivePlayers [activePlayers] numLastActions [lastActions] numLegalActions [legalActions] timebank

        potSize = int(msg[1])
        nBoardCards = int(msg[2])
        boardCards = msg[3:3+nBoardCards]
        stackSizes = msg[3+nBoardCards:6+nBoardCards]

        numActivePlayersIdx = 6 + nBoardCards
        numActivePlayers = int(msg[numActivePlayersIdx])
        activePlayers = msg[1+numActivePlayersIdx:1+numActivePlayersIdx+numActivePlayers]

        numLastActionsIdx = 1 + numActivePlayersIdx + numActivePlayers
        numLastActions = int(msg[numLastActionsIdx])
        lastActions = msg[1+numLastActionsIdx:1+numLastActionsIdx+numLastActions]

        numLegalActionsIdx = 1 + numLastActionsIdx + numLastActions
        numLegalActions = int(msg[numLegalActionsIdx])
        legalActions = msg[1+numLegalActionsIdx:1+numLegalActionsIdx+numLegalActions]

        timeBankIdx = 1 + numLegalActionsIdx + numLegalActions
        timeBank = float(msg[timeBankIdx])

        hand = self.game.hand + boardCards
        score = lib.score(hand, 5-nBoardCards)

        if score < 1.2e6:
            s.send("CHECK\n")
        else:
            # try to raise
            raiseCmd = filter(lambda x: x.startswith('RAISE'), legalActions)
            if len(raiseCmd) == 1:
                _, upper = raiseCmd[0].split(':')[1:]
                s.send("RAISE:%s\n" % upper)
            else:
                s.send("CHECK\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.',
        add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost',
        help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int,
        help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
