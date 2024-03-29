class Player:
	"""
	This class represents a player in poker. It has attributes but no methods.
	"""
	def __init__(self,name,stack):
		self.name = name
		self.stack = stack
		self.isActive = True # Whether busted or not
		self.seat = 0 # Default seat is button
		self.hole = [] # This should only be needed by the hero
		self.isIn = True # Whether folded or not

		self.last_move = ''

class Villain(Player):
	"""
	This class represents a villain in poker. It has extra attributes which
	contains information on betting style etc. It may also have methods as part 
	of phase 1 of the brain.
	"""
	def __init__(self,name,stack):
		Player.__init__(self,name,stack)
		# TBD: Put villain traits here
		self.pf = 0.5 # Probability of folding

		# Note: 52 choose 2 = 1326
		self.pdf = [1/1326.]*1326 # PDF of hole cards
		self.cdf = map(lambda x: x/1326., xrange(1326)) # CDF of hole cards
		# Equity of hole cards (TBD: MAKE THIS THE UNIFORM PREFLOP EQUITY)
		self.equ = map(lambda x: x/1326., xrange(1326)) # Linear for now
		# Action pdf given hole cards P(A_n | C)
		self.act = [1/1326.]*1326 # Default is linear

		# Cutoffs are used to convert villain equity into villain pdfs.
		# Any equity the cutoff key range will result in the key's move.
		self.cutoffs = {
		'CHECKFOLD':[0,.5],
		'CALL': [.5,.8],
		'RAISE': [.8,1.],
		}

class Game:
	"""
	This class represents a single round of Poker. As the round progresses and
   	more cards are put on the table, the Game object updates.
   	"""
   	def __init__(self, names,stack,bb,hands_max,timebank):
   		# Create list of players (of which we are index 0)
   		self.p = [Player(names[0],stack),Villain(names[1],stack),Villain(names[2],stack)]
   		self.names = names
   		self.ind2seat = dict(zip([0,1,2],[0,1,2])) # Returns the seat given index
   		self.seat2ind = dict(zip([0,1,2],[0,1,2])) # Returns the index given seat
   		self.name2ind = dict(zip([x.name for x in self.p],[0,1,2])) # Returns index given name

   		# Set up the chips, table, & legal moves
   		self.pot = 0 # Pot size
   		self.comm = [] # List of community cards
   		self.bb = bb # Big blind value
   		self.legal = [] # List of legal moves
   		self.call_amt = 0 # Amount needed to call (if 0, hero can 'check')
   		self.min_raise = bb # Minimum raise
   		self.max_raise = bb+1 # Maximum raise
   		self.validRB = 'RAISE:' # Ignore this, just used to bet properly

   		# Set up history stuff
   		self.history = []
   		self.historystr = 'H'
   		self.action_on = 1 # Seat of player who is up to play (starts with SB)

   		# Set up the rest
   		self.timebank = timebank # Time left in all hands
   		self.hands_max = hands_max # Maximum number of hands engine will play
   		self.hands_idx = 1 # Current number of hands dealt
   		self.n_active = 3 # Number of currently active players (not busted)
