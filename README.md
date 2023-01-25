# nostrify
Core Lightning plugin that sends events to Nostr

Requires `nostril` for creating Nostr events and `websocat` for sending over web socket.

To start the plugin pass the `secret` and `relay` (optional: defaults to wss://nostr.klabo.blog) when calling, like this:
`lightning-cli -k plugin subcommand=start plugin=/path/to/nostrify.py secret='your nostr secret' relay='wss://nostr.klabo.blog'`

I'm pretty sure I'm the only user at this point. It's pretty basic. PRs are encouraged! If you'd like to tip me some sats my Lightning Address is: `joel@satoshis.lol`