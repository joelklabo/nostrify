import os
from pyln.testing.fixtures import *

test_path = os.path.dirname(__file__)
plugin_path = os.path.join(test_path, '..', 'src', 'nostrify.py')

def test_nostrify_starts(node_factory):
    """ Tests that nostrify starts dynamically and statically """
    node_1 = node_factory.get_node()
    # Test dynamically
    node_1.rpc.plugin_start(plugin_path)
    node_1.daemon.wait_for_log("Plugin nostrify initialized")
    node_1.rpc.plugin_stop(plugin_path)
    node_1.rpc.plugin_start(plugin_path)
    node_1.daemon.wait_for_log("Plugin nostrify initialized")
    node_1.stop()
    # Then statically
    node_1.daemon.opts["plugin"] = plugin_path
    node_1.start()
    # Start at 0 and 're-await' the two inits above. Otherwise this is flaky.
    node_1.daemon.logsearch_start = 0
    node_1.daemon.wait_for_logs(["Plugin nostrify initialized",
                             "Plugin nostrify initialized",
                             "Plugin nostrify initialized"])
    node_1.rpc.plugin_stop(plugin_path)

def test_secret_exists(node_factory):
    """ Tests that a secret is available to nostrify """
    node_1 = node_factory.get_node(options={'plugin': plugin_path})

    assert not node_1.daemon.is_in_log("Must pass a `secret` option for creating events")

def test_relay_is_settable(node_factory):
    """ Tests that a relay can be set """
    fake_relay = 'wss://fake.relay.com'
    opts = {
        'plugin': plugin_path,
        'relay': fake_relay,
        'dev-fast-gossip': True,
    }
    node_1 = node_factory.get_node(options=opts)

    assert node_1.daemon.is_in_log(fake_relay)
    assert not node_1.daemon.is_in_log("wss://nostr.klabo.blog")

def test_connect_event_is_observed(node_factory):
    """ Tests that a connect event is observed """

    opts = {
        'plugin': plugin_path,
        'dev-fast-gossip': True
    }
    
    node_1, node_2 = node_factory.line_graph(2, options=opts, wait_for_announce=True)

    assert not node_1.daemon.is_in_log("KeyError")

    assert node_1.daemon.is_in_log(f"Received connect event for peer: {node_2.info['id']}")

def test_channel_opened_event_is_observed(node_factory):
    """ Tests that a channel open event is observed """
    
    opts = {
        'plugin': plugin_path,
        'dev-fast-gossip': True
    }
   
    node_1 = node_factory.get_node(options=opts)
    node_2 = node_factory.get_node(options=opts)
    
    node_factory.join_nodes([node_1, node_2], fundamount=10**6, wait_for_announce=True)

    assert not node_1.daemon.is_in_log("KeyError")

    assert node_1.daemon.is_in_log(f"Received channel_state_changed event for peer id: {node_2.info['id']}")
    assert node_1.daemon.is_in_log(f"Received connect event for peer: {node_2.info['id']}")
    assert node_2.daemon.is_in_log(f"Received channel_opened event with id: {node_1.info['id']}")