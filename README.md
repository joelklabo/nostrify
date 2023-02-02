# Nostrify
Core Lightning plugin that sends events to Nostr

Requires `nostril` for creating Nostr events and `websocat` for sending over web socket.

In your lightning config file set these values:
`nostr_secret=<your nostr private key>`
`nostr_relay=<your preferred relay to send events to>` (default is `wss://nostr.klabo.blog`)

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

I'm pretty sure I'm the only user at this point. It's pretty basic. PRs are encouraged! If you'd like to tip me some sats my Lightning Address is: `joel@satoshis.lol`
