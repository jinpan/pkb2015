import argparse
import socket
import sys


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
            msg_type = data.split()[0]
            if msg_type == "NEWGAME":
                self.game = Game(*data.split()[1:])
            elif msg_type == "NEWHAND":
                card1 = data.split()[3]
                card2 = data.split()[4]
                self.hand = Hand()
                self.hand.addCard(Card.new(card1))
                self.hand.addCard(Card.new(card2))
            elif msg_type == "GETACTION":
                # Currently CHECK on every move. You'll want to change this.
                s.send("CHECK\n")
            elif msg_type == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

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
