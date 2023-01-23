# nostrify
Core Lightning plugin that sends events to Nostr

Requires `nostril` for creating Nostr events and `websocat` for sending over web socket.

Once plugin is installed call these two methods on `lightning-cli` to configure:

`set-nostr-key` sets the (private) key for authoring Nostr events.

```
lightning-cli set-nostr-key 123456
```

`set-nostr-relay` sets the relay to send the events to:

```
lightning-cli set-nostr-relay wss://nostr.some.relay
```

I'm pretty sure I'm the only user at this point. It's pretty basic. PRs are encouraged! If you'd like to tip me some sats my Lightning Address is: `joel@satoshis.lol`