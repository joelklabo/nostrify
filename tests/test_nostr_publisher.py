import unittest
import time
from nostr.key import PrivateKey
# Assuming the NostrPublisher class is in a file called nostr_publisher.py
from nostr_publisher import NostrPublisher


class TestReceiver:
    def handle_event(self, event):
        print(f"Received event: {event}")


class TestNostrPublisher(unittest.TestCase):
    def setUp(self):
        # Generate private keys for sender and recipient
        sender_private_key = PrivateKey()
        recipient_private_key = PrivateKey()

        # Get public keys
        self.sender_pubkey = sender_private_key.public_key.hex()
        self.recipient_pubkey = recipient_private_key.public_key.hex()

        # Set up relays
        relays = ["wss://nostr.klabo.blog"]

        # Create Receiver instance
        self.receiver = TestReceiver()

        # Create NostrPublisher instances for sender and recipient
        self.sender = NostrPublisher(
            relays, sender_private_key.hex(), self.recipient_pubkey, self.receiver)
        self.recipient = NostrPublisher(
            relays, recipient_private_key.hex(), self.sender_pubkey, self.receiver)

        time.sleep(3)
        print("Finished setting up")

    def test_send_receive_dm(self):
        content = "Hello, this is a test message."

        # Send a direct message from sender to recipient
        self.sender.publish_dm_content(content)

        # Give the message some time to propagate through the network
        time.sleep(3)

        # Check if the recipient has received the message
        received_message = None
        while self.recipient.relay_manager.message_pool.has_events():
            event_msg = self.recipient.relay_manager.message_pool.get_event()
            decrypted_content = self.recipient.decrypt_dm_message(event_msg)
            print(decrypted_content)
            if decrypted_content == content:
                received_message = decrypted_content
                break

        self.assertEqual(received_message, content)


if __name__ == "__main__":
    unittest.main()
