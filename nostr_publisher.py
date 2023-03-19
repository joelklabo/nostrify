import ssl
from nostr.event import Event, EncryptedDirectMessage
from nostr.key import PrivateKey
from nostr.relay_manager import RelayManager

class NostrPublisher:
	def __init__(self, relays, private_key_str, recipient_pubkey):
		self.relays = relays
		self.private_key = private_key = PrivateKey(bytes.fromhex(private_key_str))
		self.recipient_pubkey = recipient_pubkey
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
		  recipient_pubkey=self.recipient_pubkey,
		  cleartext_content=content
		)
		self.private_key.sign_event(dm)
		self.relay_manager.publish_event(dm)
		