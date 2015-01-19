import argparse
import socket
import sys

from game import *
from brain import Brain
from tryhard import Tryhard

"""
Class to communicate with the engine and update the 'Game' class.
Based off the Player.py

Requires two more classes: Game and Brain.
Game is a class representing the state of the game and the players at a given
moment.
Brain is a holder class (a collection of static methods) that takes a given game
state and computes the best move.
"""

class Bot:
    def run(self,input_socket):
        """
        Get a file-object for reading packets from the socket.
        Using this ensures that you get exactly one packet per read.
        """
        f_in = input_socket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print 'Gameover, engine disconnected.'
                break

            msg = data.split()
            msg_type = msg[0]
            if msg_type == 'NEWGAME':
                # NEWGAME yourName opp1Name opp2Name stackSize bb numHands timeBank
                form = '3nnnn'
                [names,stack,bb,hands_max,timebank] = self.parse(msg[1:],form)
                self.game = Game(names,stack,bb,hands_max,timebank)
            
            elif msg_type == 'NEWHAND':
                print msg
                # NEWHAND handId seat holeCard1 holeCard2 [stackSizes] [playerNames] numActivePlayers [activePlayers] timeBank
                form = 'nn233n3n'
                [hands_idx,seat,hole,stacks,names,n_active,isActive,timebank] = self.parse(msg[1:],form)
                g = self.game
                g.hands_idx = hands_idx
                # Figure out ind2seat, isActive, & stacks for all players
                seating = [names.index(g.p[i].name) for i in range(3)] # Returns seats in index order
                g.ind2seat  = dict(zip([0,1,2],seating))
                g.seat2ind  = dict(zip(seating,[0,1,2]))
                for i in range(3):
                    g.p[i].seat = g.ind2seat[i]
                    g.p[i].stack = stacks[g.ind2seat[i]]
                    g.p[i].isActive = isActive[g.ind2seat[i]]

                # Clear villain history and make all villains 'In'
                g.historystr = 'H'
                g.action_on = 1
                for v in g.p[1:]:
                    v.isIn = True

            elif msg_type == "GETACTION":
                # GETACTION potSize numBoardCards [boardCards] [stackSizes] numActivePlayers [activePlayers] numLastActions [lastActions] numLegalActions [legalActions] timebank
                form = 'nl3n3lln'
                [pot,comm,stacks,n_active,isActive,historypak,legalpak,timebank] = self.parse(msg[1:],form)
                g = self.game
                # Update game state
                g.pot = pot
                g.comm = comm
                # Update stacks (ind2seat hasn't changed)
                for i in range(3):
                    g.p[i].stack = stacks[g.ind2seat[i]]
                    g.p[i].isActive = isActive[g.ind2seat[i]]

                # Update rest
                g.n_active = n_active
                g.timebank = timebank

                # Update legal moves
                g.call_amt = 0
                g.min_raise = 0 # If we can't raise, this will stay at 0
                g.max_raise = 0 # If we can't raise, this will stay at 0
                g.legal = map(lambda s: s.split(':'), legalpak)
                for m in g.legal:
                    if m[0] == 'CALL':
                        g.call_amt = float(m[1])
                    elif m[0] == 'CHECK':
                        g.call_amt = 0
                    elif m[0] == 'RAISE' or m[0] == 'BET':
                        g.min_raise = float(m[1])
                        g.max_raise = float(m[2])
                        g.validRB = m[0]

                # Update player move histories
                Tryhard.study(g,historypak)

                # Play poker!
                action = Brain.play(g)
                
                # Interpret the action and then send
                s.send(self.interpret(action))

            elif msg_type == "HANDOVER":
                # HANDOVER [stackSizes] numBoardCards [boardCards] numLastActions [lastActions] timeBank
                form = '3lln'
                [stacks,comm,historypak,timebank] = self.parse(msg[1:],form)
                g = self.game
                # Update game state
                g.timebank = timebank
                g.comm = comm
                # Update stacks
                for i in range(3):
                    g.p[i].stack = stacks[g.ind2seat[i]]
                
                # TBD: Do we want to update player profiles based on this history?
                # Maybe would look something like this?
                """Brain.retrospect(g)"""
                # Note we don't need to update pdfs

            elif msg_type == "KEYVALUE":
                # Here we would probably store villain traits for future games
                print 'I got a KEYVALUE packet. What do I do with it?'

            elif msg_type == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()
    def parse(self,msg,form):
        """
        Parse the data to update the game state given a format where 'l'
        represents a list, 's' represents a string, and 'n' represents a number.
        Passing a form with a number 'x' will assume a list of length x.
        Return a list that is parsed.
        """
        parsed = []
        i = 0 # Offset
        for f in form:
            if f == 's': # Parse a string
                parsed.append(msg[i])
                i += 1
            elif f == 'n': # Parse a number
                parsed.append(float(msg[i]))
                i += 1
            elif f == 'l': # Parse a list of unknown length
                parsed.append(msg[i+1:i+1+int(msg[i])])
                i += 1 + int(msg[i])
            else: # Parse a list of known length given by f
                parsed.append(msg[i:i+int(f)])
                i += int(f)
        return parsed # Read input
    def interpret(self,action):
        """
        Interpret the action to return a string that can be understood by the
        engine.

        If action is between min_raise and max_raise, bot will raise.
        If action is between call_amt and min_raise, bot will call.
        If action == 0 and call_amt == 0, bot will check.
        If action < call_amt, bot will fold.
        Otherwise, print an error.

        """
        g = self.game        
        print 'Comm Cards:    ' + str(g.comm) 
        print str(g.timebank)+ ' sec left.'
        print ''

        # use validRB to decide whether to RAISE or just BET
        if action > g.max_raise and g.max_raise != 0:
            print 'Raise too high.'
            return g.validRB+':'+str(g.max_raise)+'\n' # Cap the raise
        elif action >= g.min_raise and g.max_raise != 0:
            return g.validRB+':'+str(action)+'\n' # Perform raise
        elif action >= g.call_amt and g.call_amt != 0:
            return 'CALL:'+str(action)+'\n' # Perform call
        elif action == 0 and g.call_amt == 0:
            return 'CHECK\n' # Perform check
        elif action < g.call_amt:
            return 'FOLD\n' # Perform fold
        else:
            print 'Error: impossible action '+str(action)  # Return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.',
       add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost',
       help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int,
       help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print('Connecting to %s:%d' % (args.host, args.port))
    try:
       s = socket.create_connection((args.host, args.port))
    except socket.error as e:
       print('Error connecting! Aborting')
       exit()

    bot = Bot()
    bot.run(s)
