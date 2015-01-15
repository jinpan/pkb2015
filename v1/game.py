class Player:
	"""
	This class represents a player in poker. It has attributes but no methods.
	"""
	def __init__(self,name,stack):
		self.name = name
		self.stack = stack
		self.isActive = True
		self.seat = 1 # Default seat is button
		self.hole = [] # This should only be needed by the hero

class Villain(Player):
	"""
	This class represents a villain in poker. It has extra attributes which
	contains information on betting style etc. It may also have methods as part 
	of phase 1 of the brain.
	"""
	def __init__(self,name,stack):
		Player.__init__(self,name,stack)
		# TBD: Put interesting stylistic attributes here (like pdf)
		# Initialize with a uniform pdf (linear cdf)
		# 52 choose 2 = 1326
		self.cdf = list(map(lambda x: x/1326, range(1326)))

class Game:
	"""
	This class represents a single round of Poker. As the round progresses and
   	more cards are put on the table, the Game object updates.
   	"""
   	def __init__(self, names,stack,bb,hands_max,timebank):
   		# Create list of players (of which we are index 0)
   		self.names = names
   		print names
   		self.p = [Player(names[0],stack),Villain(names[1],stack),Villain(names[2],stack)]
   		self.seating = dict(zip([0,1,2],[0,1,2])) # Returns the seat given index
   		
   		# Set up the chips, table, & legal moves
   		self.pot = 0 # Pot size
   		self.comm = [] # List of community cards
   		self.bb = bb # Big blind value
   		self.legal = [] # List of legal moves
   		self.call_amt = 0 # Amount needed to call (if 0, hero can 'check')
   		self.min_raise = bb # Minimum raise
   		self.max_raise = bb+1 # Maximum raise

   		# Set up the rest
   		self.timebank = timebank # Time left
   		self.hands_max = hands_max # Maximum number of hands engine will play
   		self.hands_idx = 1 # Current number of hands dealt
   		self.n_active = 3 # Number of currently active players (not busted)
   		self.legal = '' # Legal possible actions
