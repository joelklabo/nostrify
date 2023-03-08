from pyln.testing.fixtures import *

plugin_path = os.path.join(os.path.dirname(__file__), "nostrify.py")

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

#def test_your_plugin(node_factory, bitcoind):
#    l1 = node_factory.get_node(options=pluginopt)
#    s = l1.rpc.getinfo()
#    assert(s['network'] == 'regtest') # or whatever you want to test
