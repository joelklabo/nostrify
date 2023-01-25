#!/usr/bin/env python3

# pylint: disable=consider-using-f-string

import os
from pyln.client import Plugin

plugin = Plugin()

def send_nostr_event(content):
    """ Sends `content` as a Nostr Event"""
    command = rf'nostril --envelope --sec "{plugin.secret}" --content "{content}" | websocat {plugin.relay} > /dev/null'
    plugin.log(command)
    os.system(command)


@plugin.init()
def init(options, configuration, plugin, **kwargs):
    """ Initializes the plugin """
   
    plugin.secret = plugin.get_option('secret')
    plugin.relay = plugin.get_option('relay')
    
    if plugin.secret is None:
        plugin.log("Must pass a `secret` option for creating events")
        return

    plugin.log("Plugin nostrify initialized")

@plugin.subscribe("channel_opened")
def on_channel_opened(plugin, channel_opened, **kwargs):
    """ Responds to channel_opened event """
    content = """
		Received channel_opened event with id: {id}
		funding msat: {funding_msat}	
		funding txid: {funding_txid}
		channel ready: {channel_ready}
	""".format(**channel_opened)
    send_nostr_event(content)


@plugin.subscribe("channel_open_failed")
def on_channel_open_failed(plugin, channel_open_failed, **kwargs):
    """ Responds to channel_open_failed event """
    content = """
	    Received channel_open_failed event for channel id: {channel_id}
	""".format(**channel_open_failed)
    send_nostr_event(content)


@plugin.subscribe("channel_state_changed")
def on_channel_state_changed(plugin, channel_state_changed, **kwargs):
    """ Responds to channel_state_changed event """
    content = """
	    Received channel_state_changed event for peer id: {peer_id}
	    channel id: {channel_id}
	    short channel id: {short_channel_id}
	    timestamp: {timestamp}
	    old state: {old_state}
	    new state: {new_state}
	    cause: {cause}
	    message: {message}
	""".format(**channel_state_changed)
    send_nostr_event(content)


@plugin.subscribe("connect")
def on_connect(plugin, id, address, **kwargs):
    """ Responds to connect event """
    content = f"""
        Received connect event for peer: {id}
    """
    send_nostr_event(content)


@plugin.subscribe("disconnect")
def on_disconnect(plugin, id, **kwargs):
    """ Responds to disconnect event """
    content = f"""
        Received disconnect event for peer: {id}
    """
    send_nostr_event(content)


@plugin.subscribe("invoice_payment")
def on_payment(plugin, invoice_payment, **kwargs):
    """ Responds to invoice_payment event """
    content = """
        Received invoice_payment event for label: {label}
        preimage: {preimage}
    """.format(**invoice_payment)
    send_nostr_event(content)


@plugin.subscribe("invoice_creation")
def on_invoice_creation(plugin, invoice_creation, **kwargs):
    """ Responds to invoice_creation event """
    #content = """
    #    Received invoice_creation event for label: {label}
    #    preimage: {preimage}
    #    amount: {msat}
    #""".format(**invoice_creation)
    send_nostr_event("hi")


@plugin.subscribe("warning")
def on_warning(plugin, warning, **kwargs):
    """ Responds to warning event """
    content = """
        Received warning event with level: {level}
        time: {time}
        source: {source}
        log: {log}
    """
    send_nostr_event(content)


@plugin.subscribe("forward_event")
def on_forward_event(plugin, forward_event, **kwargs):
    """ Responds to forward_event event """
    content = """
        Received a forward event with payment hash: {payment_hash}
        in channel: {in_channel}
        out channel: {out_channel}
        in msat: {in_msat}
        out msat: {out_msat}
        fee msat: {fee_msat}
        status: {status}
        received time: {received_time}
        resolved time: {resolved_time}
    """
    send_nostr_event(content)


@plugin.subscribe("sendpay_success")
def on_sendpay_success(plugin, sendpay_success, **kwargs):
    """ Responds to sendpay_success event """
    content = """
        Received a sendpay success event with id: {id}
        payment hash: {payment_hash}
        destination: {destination}
        amount msat: {amount_msat}
        amount sent msat: {amount_sent_msat}
        created at: {created_at}
        status: {status}
        payment preimage: {payment_preimage}
    """.format(**sendpay_success)
    send_nostr_event(content)


@plugin.subscribe("sendpay_failure")
def on_sendpay_failure(plugin, sendpay_failure, **kwargs):
    """ Responds to sendpay_success event """
    content = """
        Received a sendpay failure event with code: {code}
        message: {message}
        data: {data}
    """.format(**sendpay_failure)
    send_nostr_event(content)


@plugin.subscribe("coin_movement")
def on_coin_movement(plugin, coin_movement, **kwargs):
    """ Responds to coin_movement event """
    content = """
        Received a coin movement event with version: {version}
        node id: {node_id}
        type: {type}
        account id: {account_id}
        originating account: {originating_account}
        txid: {txid}
        utxo txid: {utxo_txid}
        vout: {vout}
        payment hash: {payment_hash}
        part id: {part_id}
        credit msat: {credit_msat}
        debit msat: {debit_msat}
        output msat: {output_msat}
        output count: {output_count}
        fee msat: {fee_msat}
        tags: {tags}
        blockheight: {blockheight}
        timestamp: {timestamp}
        coin type: {coin_type}
    """.format(**coin_movement)
    send_nostr_event(content)


@plugin.subscribe("balance_snapshot")
def on_balance_snapshot(plugin, balance_snapshots, **kwargs):
    """ Responds to coin_movement event """
    content = f"""
        Received a balance snapshot event: {balance_snapshots}
    """
    send_nostr_event(content)


@plugin.subscribe("openchannel_peer_sigs")
def on_openchannel_peer_sigs(plugin, openchannel_peer_sigs, **kwargs):
    """ Responds to openchannel_peer_sigs event """
    content = """
    Received a openchannel peer sigs event with channel id: {channel_id}
    signed psbt: {signed_psbt}
    """.format(**openchannel_peer_sigs)
    send_nostr_event(content)


@plugin.subscribe("shutdown")
def on_shutdown(plugin, **kwargs):
    """ Responds to shutdown event """
    send_nostr_event("Received a shutdown event")

plugin.add_option('secret', '', 'The nostr private key for authoring events')
plugin.add_option('relay', 'wss://nostr.klabo.blog', 'The relay you want to send events to (default: wss://nostr.klabo.blog')

plugin.run()
