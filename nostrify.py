#!/usr/bin/env python3

import os
from pyln.client import Plugin
from nostr.key import PrivateKey
from nostr_publisher import NostrPublisher

plugin = Plugin()

def handle_message(self, message):
    """ Handles a message from a Nostr Relay """
    nostrify_log(f"Received message: {message}")

def send_nostr_event(content):
    """ Sends `content` as a Nostr Event"""
    if os.environ.get('TEST_DEBUG') is not None:
        nostrify_log(content)
    else:
        plugin.publisher.publish_dm_content(content)

def nostrify_log(message):
    """ Logs a message to the plugin log """
    plugin.log(f"[Nostrify]: {message}")    

@plugin.init()
def init(options, configuration, **kwargs):
    """ Initializes the plugin """

    plugin.secret = plugin.rpc.makesecret(string='nostr')['secret']

    plugin.relays = options['nostr_relay']
    nostrify_log(f"set to use relays: {plugin.relays}")

    plugin.pubkey = options['nostr_pubkey']
    nostrify_log(f"set to use pubkey: {plugin.pubkey}")

    plugin.disabled_events = options['nostr_disable_event']
    nostrify_log(f"set to ignore events: {plugin.disabled_events}")

    if plugin.relays is None:
        nostrify_log(
            "must set at least one relay with the `nostr_relay` option")
        return

    if plugin.secret is None:
        nostrify_log("must pass a `secret` option for creating events")
        return

    if plugin.pubkey is None:
        nostrify_log("must set a pubkey with the `nostr_pubkey` option")
        return

    try:
        plugin.publisher = NostrPublisher(
            plugin.relays, plugin.secret, plugin.pubkey, handle_message)
    except Exception as publisher_exception:
        nostrify_log(
            "an error occurred while initializing the NostrPublisher:")
        nostrify_log(str(publisher_exception))
        return

    nostrify_log("plugin initialized")

# Subscriptions


@plugin.subscribe("channel_opened")
def on_channel_opened(channel_opened, **kwargs):
    """ Responds to channel_opened event """
    content = f"""Received channel_opened event with id: {channel_opened.get('id', 'unknown')}
    funding msat: {channel_opened.get('funding_msat', 'unknown')}
    funding txid: {channel_opened.get('funding_txid', 'unknown')}
    channel ready: {channel_opened.get('channel_ready', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("channel_open_failed")
def on_channel_open_failed(channel_open_failed, **kwargs):
    """ Responds to channel_open_failed event """
    content = f"""Received channel_open_failed event for channel id: {channel_open_failed.get('channel_id', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("channel_state_changed")
def on_channel_state_changed(channel_state_changed, **kwargs):
    """ Responds to channel_state_changed event """
    content = f"""Received channel_state_changed event for peer id: {channel_state_changed.get('peer_id', 'unknown')}
    channel id: {channel_state_changed.get('channel_id', 'unknown')}
    short channel id: {channel_state_changed.get('short_channel_id', 'unknown')}
    timestamp: {channel_state_changed.get('timestamp', 'unknown')}
    old state: {channel_state_changed.get('old_state', 'unknown')}
    new state: {channel_state_changed.get('new_state', 'unknown')}
    cause: {channel_state_changed.get('cause', 'unknown')}
    message: {channel_state_changed.get('message', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("connect")
def on_connect(id, address, **kwargs):
    """ Responds to connect event """

    if "connect" in plugin.disabled_events:
        return

    content = f"Received connect event for peer: {id}"
    send_nostr_event(content)


@plugin.subscribe("disconnect")
def on_disconnect(id, **kwargs):
    """ Responds to disconnect event """

    if "disconnect" in plugin.disabled_events:
        return

    content = f"Received disconnect event for peer: {id}"
    send_nostr_event(content)


@plugin.subscribe("invoice_payment")
def on_payment(invoice_payment, **kwargs):
    """ Responds to invoice_payment event """
    content = f"""Received invoice_payment event for label: {invoice_payment.get('label', 'unknown')}
    preimage: {invoice_payment.get('preimage', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("invoice_creation")
def on_invoice_creation(invoice_creation, **kwargs):
    """ Responds to invoice_creation event """
    content = f"""Received invoice_creation event for label: {invoice_creation.get('label', 'unknown')}
    preimage: {invoice_creation.get('preimage', 'unknown')}
    amount: {invoice_creation.get('msat', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("warning")
def on_warning(warning, **kwargs):
    """ Responds to warning event """
    content = f"""Received warning event with level: {warning.get('level', 'unknown')}
    time: {warning.get('time', 'unknown')}
    source: {warning.get('source', 'unknown')}
    log: {warning.get('log', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("forward_event")
def on_forward_event(forward_event, **kwargs):
    """ Responds to forward_event event """

    status = forward_event.get('status', 'unknown')

    if status == "offered" and "forward_offered" in plugin.disabled_events:
        return

    if status == "failed" and "forward_failed" in plugin.disabled_events:
        return

    if status == "settled" and "forward_settled" in plugin.disabled_events:
        return

    content = f"""Received a forward event with payment hash: {forward_event.get('payment_hash', 'unknown')}
    in channel: {forward_event.get('in_channel', 'unknown')}
    out channel: {forward_event.get('out_channel', 'unknown')}
    in msat: {forward_event.get('in_msat', 'unknown')}
    out msat: {forward_event.get('out_msat', 'unknown')}
    fee msat: {forward_event.get('fee_msat', 'unknown')}
    status: {forward_event.get('status', 'unknown')}
    received time: {forward_event.get('received_time', 'unknown')}
    resolved time: {forward_event.get('resolved_time', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("sendpay_success")
def on_sendpay_success(sendpay_success, **kwargs):
    """ Responds to sendpay_success event """
    content = f"""Received a sendpay success event with id: {sendpay_success.get('id', 'unknown')}
    payment hash: {sendpay_success.get('payment_hash', 'unknown')}
    destination: {sendpay_success.get('destination', 'unknown')}
    amount msat: {sendpay_success.get('amount_msat', 'unknown')}
    amount sent msat: {sendpay_success.get('amount_sent_msat', 'unknown')}
    created at: {sendpay_success.get('created_at', 'unknown')}
    status: {sendpay_success.get('status', 'unknown')}
    payment preimage: {sendpay_success.get('payment_preimage', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("sendpay_failure")
def on_sendpay_failure(sendpay_failure, **kwargs):
    """ Responds to sendpay_success event """
    content = f"""Received a sendpay failure event with code: {sendpay_failure['code']}
    message: {sendpay_failure['message']}
    data: {sendpay_failure['data']}"""
    send_nostr_event(content)


@plugin.subscribe("coin_movement")
def on_coin_movement(coin_movement, **kwargs):
    """ Responds to coin_movement event """
    content = f"""Received a coin movement event with version: {coin_movement.get('version', 'unknown')}
    node id: {coin_movement.get('node_id', 'unknown')}
    type: {coin_movement.get('type', 'unknown')}
    account id: {coin_movement.get('account_id', 'unknown')}
    originating account: {coin_movement.get('originating_account', 'unknown')}
    txid: {coin_movement.get('txid', 'unknown')}
    utxo txid: {coin_movement.get('utxo_txid', 'unknown')}
    vout: {coin_movement.get('vout', 'unknown')}
    payment hash: {coin_movement.get('payment_hash', 'unknown')}
    part id: {coin_movement.get('part_id', 'unknown')}
    credit msat: {coin_movement.get('credit_msat', 'unknown')}
    debit msat: {coin_movement.get('debit_msat', 'unknown')}
    output msat: {coin_movement.get('output_msat', 'unknown')}
    output count: {coin_movement.get('output_count', 'unknown')}
    fee msat: {coin_movement.get('fee_msat', 'unknown')}
    tags: {coin_movement.get('tags', 'unknown')}
    blockheight: {coin_movement.get('blockheight', 'unknown')}
    timestamp: {coin_movement.get('timestamp', 'unknown')}
    coin type: {coin_movement.get('coin_type', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("openchannel_peer_sigs")
def on_openchannel_peer_sigs(openchannel_peer_sigs, **kwargs):
    """ Responds to openchannel_peer_sigs event """
    content = f"""Received an openchannel peer sigs event with channel id: {openchannel_peer_sigs.get('channel_id', 'unknown')}
    signed psbt: {openchannel_peer_sigs.get('signed_psbt', 'unknown')}"""
    send_nostr_event(content)


@plugin.subscribe("shutdown")
def on_shutdown(**kwargs):
    """ Responds to shutdown event """
    send_nostr_event("Received a shutdown event")

# Methods


@plugin.method("nostrifypubkey")
def nostrifypubkey(plugin):
    """ Returns the node's pubkey """
    private_key = PrivateKey(bytes.fromhex(plugin.secret))
    public_key = f"{private_key.public_key.bech32()}"
    nostrify_log(f"returning public_key: {public_key}")
    return public_key

# Options


plugin.add_option('nostr_relay',
                  description="The relay you want to send events to",
                  default=[],
                  multi=True,
                  opt_type='string')

plugin.add_option('nostr_pubkey',
                  default='',
                  description='The Nostr pubkey you want to send events to',
                  opt_type='string')

plugin.add_option('nostr_disable_event',
                  description='The CLN events you do NOT want to receive on Nostr (default will send all events)',
                  default=[],
                  multi=True,
                  opt_type='string')
plugin.run()
