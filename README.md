[![CI Tests](https://github.com/joelklabo/nostrify/actions/workflows/ci.yml/badge.svg)](https://github.com/joelklabo/nostrify/actions/workflows/ci.yml)

Tested on Bitcoin Core `24.0.1`, `23.1`
Core Lightning `master`, `23.02`, `22.11.1`

# Nostrify
Core Lightning plugin that sends events to Nostr (**requires CLN 22**)

# Quickstart

Requires [`nostril`](https://github.com/jb55/nostril/tree/master) for creating Nostr events and [`websocat`](https://github.com/vi/websocat) for sending over web socket.

By default `Nostrify` uses `lightning-cli makesecret string=nostr` to generate a Nostr key for you. This generates a psuedorandom secret based off of your `HSM_secret`.

See the documentation for `makesecret` [here](https://lightning.readthedocs.io/lightning-makesecret.7.html?highlight=makesecret)

The relay defaults to `wss://nostr.klabo.blog`.

## How to see your events after starting the plugin

1. Run `lightning-cli makesecret string=nostr` this will return the Nostr secret of your plugin:
```bash
$ lightning-cli makesecret string=nostr
{
   "secret": "d8e6c7x....8cbcfe"
}
```

2. If you have a tool to convert that to a pubkey you can just follow it with your main Nostr account.
3. If you don't you can log in with it https://snort.social, you should see events, and the client should show you what the public key is so you can follow it.
4. If you didn't set a custom relay, all events are sent to `wss://nostr.klabo.blog` so you'll need to subscribe to that
5. That should be it. If that's not working please log a bug

### Example after logging into https://snort.social :
<img width="870" alt="image" src="https://user-images.githubusercontent.com/264977/224822474-3e077bb9-a11c-4269-afd4-8a2121a9a033.png">


### Optional last step

Follow me on nostr `npub19a86gzxctwtz68l8zld2u9y2fjvyyj4juyx8m5geylssrmfj27eqs22ckt` and send me a Zap or tip at `joel@klabo.blog` 🤙

# Setting a Custom Relay

In your lightning config file set this value:
`relay=<your preferred relay to send events to>` (default is `wss://nostr.klabo.blog`)

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

# Contribute

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

I'm pretty sure I'm the only user at this point. It's pretty basic. PRs are encouraged! If you'd like to tip me some sats my Lightning Address is: `joel@klabo.blog`
