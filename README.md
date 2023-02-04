# Nostrify
Core Lightning plugin that sends events to Nostr

# Quickstart

Requires [`nostril`](https://github.com/jb55/nostril/tree/master) for creating Nostr events and [`websocat`](https://github.com/vi/websocat) for sending over web socket.

By default `Nostrify` uses `lightning-cli makesecret string=nostr` to generate a Nostr key for you. This generates a psuedorandom secret based off of your `HSM_secret`.

See the documentation for `makesecret` [here](https://lightning.readthedocs.io/lightning-makesecret.7.html?highlight=makesecret)

The relay defaults to `wss://nostr.klabo.blog`.

# Setting a Custom Relay

In your lightning config file set this value:
`nostr_relay=<your preferred relay to send events to>` (default is `wss://nostr.klabo.blog`)

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

# Contribute

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

I'm pretty sure I'm the only user at this point. It's pretty basic. PRs are encouraged! If you'd like to tip me some sats my Lightning Address is: `joel@satoshis.lol`
