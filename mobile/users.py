import uuid

class User:
	def __init__(self, access_token):
		self.access_token = access_token
		self.key = str(uuid.uuid4())
		self.secret = None
		self.event = None
		self.visitor_token = None
