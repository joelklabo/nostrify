import ssl
from nostr.event import Event, EncryptedDirectMessage
from nostr.key import PrivateKey
from nostr.relay_manager import RelayManager

class NostrPublisher:
	def __init__(self, relays, private_key_str):
		self.relays = relays
		self.private_key = private_key = PrivateKey(bytes.fromhex(private_key_str))
		self.relay_manager = RelayManager()
		for relay in self.relays:
			self.relay_manager.add_relay(relay)
		self.relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})

	def publish_event(self, event):
		self.private_key.sign_event(event)
		self.relay_manager.publish_event(event)
	
	def publish_content(self, content):
		event = Event(content)
		self.private_key.sign_event(event)
		self.relay_manager.publish_event(event)
	
	def publish_dm_content(self, content):
		dm = EncryptedDirectMessage(
		  recipient_pubkey="2f4fa408d85b962d1fe717daae148a4c98424ab2e10c7dd11927e101ed3257b2",
		  cleartext_content=content
		)
		self.private_key.sign_event(dm)
		self.relay_manager.publish_event(dm)

#publisher = NostrPublisher(["wss://nostr.klabo.blog"], "45e237f0a302a7f5835137716341d5bd9019a86342ed7bd5d57c6e4fde98a47d")
#event = Event("Hello Nostr")
#publisher.publish_event(event)
#time.sleep(1.25)
#dm = EncryptedDirectMessage(
#  recipient_pubkey="2f4fa408d85b962d1fe717daae148a4c98424ab2e10c7dd11927e101ed3257b2",
#  cleartext_content="Secret message!"
#)
#publisher.publish_event(dm)
#time.sleep(1.25)