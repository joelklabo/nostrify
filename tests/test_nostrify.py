from pyln.testing.fixtures import *

test_path = os.path.dirname(__file__)
plugin_path = os.path.join(test_path, '..', 'src', 'plugin.py')

def test_nostrify_starts(node_factory):
    l1 = node_factory.get_node()
    # Test dynamically
    l1.rpc.plugin_start(plugin_path)
    l1.daemon.wait_for_log("Plugin nostrify initialized")
    l1.rpc.plugin_stop(plugin_path)
    l1.rpc.plugin_start(plugin_path)
    l1.daemon.wait_for_log("Plugin nostrify initialized")
    l1.stop()
    # Then statically
    l1.daemon.opts["plugin"] = plugin_path
    l1.start()
    # Start at 0 and 're-await' the two inits above. Otherwise this is flaky.
    l1.daemon.logsearch_start = 0
    l1.daemon.wait_for_logs(["Plugin nostrify initialized",
                             "Plugin nostrify initialized",
                             "Plugin nostrify initialized"])
    l1.rpc.plugin_stop(plugin_path)

def test_connect_event_is_observed(node_factory):
    l1_opts = {
        "plugin": plugin_path,
    }

    l1, l2 = node_factory.line_graph(2, opts={'plugin': plugin_path}, wait_for_announce=True)

    l1.daemon.wait_for_log("Received connect event for peer: {}".format(l2.info["id"]))

def test_channel_opened_event_is_observed(node_factory):
    l1_opts = {
        "plugin": plugin_path,
    }
    l1 = node_factory.get_node(options=l1_opts)
    l2 = node_factory.get_node()
    node_factory.join_nodes([l1, l2], fundamount=10**6, wait_for_announce=True)

    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    l1.daemon.wait_for_log("Received connect event for peer: {}".format(l2.info["id"]))
    l1.rpc.fundchannel(l2.info["id"], 10**6)

    l1.daemon.wait_for_log("Received channel_opened event with id: {}".format(l2.info["id"]))
