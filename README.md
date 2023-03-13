[![CI Tests](https://github.com/joelklabo/nostrify/actions/workflows/ci.yml/badge.svg)](https://github.com/joelklabo/nostrify/actions/workflows/ci.yml)

# Nostrify
Core Lightning plugin that sends events to Nostr (**requires CLN 22**)

# Quickstart

Requires [`nostril`](https://github.com/jb55/nostril/tree/master) for creating Nostr events and [`websocat`](https://github.com/vi/websocat) for sending over web socket.

By default `Nostrify` uses `lightning-cli makesecret string=nostr` to generate a Nostr key for you. This generates a psuedorandom secret based off of your `HSM_secret`.

See the documentation for `makesecret` [here](https://lightning.readthedocs.io/lightning-makesecret.7.html?highlight=makesecret)

The relay defaults to `wss://nostr.klabo.blog`.

## Important settings

In your `.lightning/config` you SHOULD set a relay to send your events to, and a recipient if you want events sent as a DM:

Example:
```
nostr_relay=wss://nostr.klabo.blog
nostr_dm_recipient=2f4fa408d85b962d1fe717daae148a4c98424ab2e10c7dd11927e101ed3257b2 (HEX not npub for now)
```

If you don't set these the relays will default to `wss://nosrt.klabo.blog` and events will be sent publicly.

## How to see your events after starting the plugin

### If you are not sending DMs

1. Run `lightning-cli makesecret string=nostr` this will return the Nostr secret of your plugin:
```bash
$ lightning-cli makesecret string=nostr
{
   "secret": "d8e6c7x....8cbcfe"
}
```

2. If you have a tool to convert that to a pubkey you can just follow it with your main Nostr account.
3. If you don't you can log in with it somewhere, you should see events, and the client should show you what the public key is so you can follow it.
4. If you didn't set a custom relay, all events are sent to `wss://nostr.klabo.blog` so you'll need to subscribe to that.
5. That should be it. If that's not working please log a bug

## If you are sending DMs

1. You should just see them in your client.

### Optional last step

Follow me on nostr `npub19a86gzxctwtz68l8zld2u9y2fjvyyj4juyx8m5geylssrmfj27eqs22ckt` and send me a Zap or tip at `joel@klabo.blog` 🤙

# Setting a Custom Relay

In your lightning config file set this value:
`relay=<your preferred relay to send events to>` (default is `wss://nostr.klabo.blog`)

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

# Contribute

Then start `lightningd` with the Nostrify plugin. `lightningd` must be restarted to get access to config values.

I'm pretty sure I'm the only user at this point. It's pretty basic. PRs are encouraged! If you'd like to tip me some sats my Lightning Address is: `joel@klabo.blog`
