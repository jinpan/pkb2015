import argparse
import socket
import sys

from game import Game
from bot import Bot

"""
Class to communicate with the engine and update the 'Game' class.
Based off the Player.py

Requires two more classes: Game and Bot.
Game is a class representing the state of the game and the players at a given
moment.
Bot is a holder class (a collection of static methods) that takes a given game
state and computes the best move.
"""

class Bot:
	def __init__(self):
		# This is the game state that the bot updates.
		self.game = Game(2) # 2 villains

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

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            self.parse(data)

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            word = data.split()[0]
            if word == "GETACTION":
                # This is where we have to actually do things
                # Pass the game to the bot and determine the action
                action = Bot.play(self.game)
                # Interpret the action and then send.
                s.send(self.interpret(action))
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()
       def parse(self,data):
       	"""
       	Parse the data to update the game state.
       	"""
       	pass
       def interpret(self,action):
       	"""
       	Interpret the action to return a string that can be understood by the
       	engine.
       	"""
       	pass
       	