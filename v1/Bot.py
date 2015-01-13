import argparse
import socket
import sys

# from game import Game
# from brain import Brain

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
        f_in = inputsocket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print('Gameover, engine disconnected.')
                break

            msg = data.split()
            msg_type = msg[0]
            if msg_type == 'NEWGAME':
                # NEWGAME yourName opp1Name opp2Name stackSize bb numHands timeBank
                form = '3nnnn'
                [names,stack,bb,hands_max,timebank] = self.parse(msg[1:],form)
                self.game = Game(names,stack,bb,hands_max,timebank)
            
            elif msg_type == 'NEWHAND':
                # NEWHAND handId seat holeCard1 holeCard2 [stackSizes] [playerNames] numActivePlayers [activePlayers] timeBank
                form = 'nn233n3n'
                [hands_idx,seat,hole,stacks,names,n_active,isActive,timebank] = self.parse(msg[1:],form)
                self.game = g
                g.hands_idx = hands_idx
                # Figure out seating, isActive, & stacks for all players
                g.seating = [names.index(g.p[i].name) for i in range(3)] # Returns seats in index order
                for i in range(3):
                    g.p[i].seat = g.seating[i]
                    g.p[i].stack = stacks[g.seating[i]]
                    g.p[i].isActive = isActive[g.seating[i]]

            elif msg_type == "GETACTION":
                # GETACTION potSize numBoardCards [boardCards] [stackSizes] numActivePlayers [activePlayers] numLastActions [lastActions] numLegalActions [legalActions] timebank
                form = 'nl3n3lln'
                [pot,comm,stacks,n_active,isActive,history,legalstr,timebank] = self.parse(msg[1:],form)
                self.game = g
                # Update game state
                g.pot = pot
                g.comm = comm
                # Update stacks (seating hasn't changed)
                for i in range(3):
                    g.p[i].stack = stacks[g.seating[i]]
                    g.p[i].isActive = isActive[g.seating[i]]
                # Update rest
                g.n_active = n_active
                g.timebank = timebank

                # Update legal moves
                g.legal = list(map(lambda s: s.split(':'), legalstr.split(',')))
                for m in g.legal:
                    if m[0] == 'CALL'
                        g.call_amt = m[1]
                    elif m[0] == 'CHECK'
                        g.call_amt = 0
                    elif m[0] == 'RAISE' or m[0] == 'BET':
                        g.min_raise = m[1]
                        g.max_raise = m[2]

                # TBD: Use phase 1 of the brain to update pmfs of villains
                # TBD: Use phase 2 of the brain to determine best action

                # Maybe would look something like this?
                """action = Brain.play(g,history)"""
                # For now, lets make the bot only check/fold
                action = 0

                # Interpret the action and then send
                s.send(self.interpret(action))
            elif msg_type == "HANDOVER":
                # HANDOVER [stackSizes] numBoardCards [boardCards] numLastActions [lastActions] timeBank
                form = '3lln'
                [stacks,comm,history,timebank] = self.parse(msg[1:],form)
                self.game = g
                # Update game state
                g.timebank = timeBank
                g.comm = comm
                # Update stacks
                for i in range(3):
                    g.p[i].stack = stacks[g.seating[i]]
                
                # TBD: Do we want to update player profiles based on this history?
                # Maybe would look something like this?
                """Brain.update_profiles(g,history)"""
                # Note we don't need to update pdfs

            elif msg_type == "KEYVALUE":
                # Here we would probably store villain traits for future games
                print('I got a KEYVALUE packet. What do I do with it?')

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
        return parsed
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
        self.game = g
        if action > g.max_raise:
            print('Raise too high.')
            return 'RAISE:'+str(g.max_raise)+'\n' # Cap the raise
        elif action >= g.min_raise:
            return 'RAISE:'+str(action)+'\n' # Perform raise
        elif action >= g.call_amt and g.call_amt != 0:
            return 'CALL:'+str(action)+'\n' # Perform call
        elif action == 0 and g.call_amt == 0:
            return 'CHECK\n' # Perform check
        elif action < g.call_amt:
            return 'FOLD\n' # Perform fold
        else:
            print('Error: impossible action '+str(action))

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
