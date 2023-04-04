import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EncryptedDirectMessage, EventKind
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey
from nostr.relay_manager import RelayManager

class NostrPublisher:
	def __init__(self, relays, private_key_str, recipient_pubkey):
		self.relays = relays
		self.private_key = PrivateKey(bytes.fromhex(private_key_str))
		self.recipient_pubkey = recipient_pubkey
		self.relay_manager = RelayManager()
	
		# Add relays
		for relay in self.relays:
			self.relay_manager.add_relay(relay)

		# Subscribe to direct messages
		filters = Filters([Filter(authors=[self.recipient_pubkey], kinds=[EventKind.DIRECT_MESSAGE])])
		subscription_id = "nostrify:" + self.recipient_pubkey
		request = [ClientMessageType.REQUEST, subscription_id]
		request.extend(filters.to_json_array())
		self.relay_manager.add_subscription(subscription_id, filters)
		self.relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
		time.sleep(1.25)
		message = json.dumps(request)
		self.relay_manager.publish_message(message)
		time.sleep(1.25)

		while self.relay_manager.message_pool.has_events():
			event_msg = self.relay_manager.message_pool.get_event()
			print("Received event: " + str(event_msg))

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

		