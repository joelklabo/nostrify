# Use [nostr-control](https://github.com/joelklabo/nostr-control) Instead, this is no longer maintained.

[![CI Tests](https://github.com/joelklabo/nostrify/actions/workflows/ci.yml/badge.svg)](https://github.com/joelklabo/nostrify/actions/workflows/ci.yml)

Tested on Bitcoin Core `24.0.1`, `23.1`
Core Lightning `master`, `23.02`, `22.11.1`

# Nostrify
Core Lightning plugin that sends events to Nostr

# Quickstart

Clone this repo into your `/plugins` folder. You'll need to run `pip3 install -r requirements.txt`

By default `Nostrify` uses `lightning-cli makesecret string=nostr` to generate a Nostr key for you. This generates a psuedorandom secret based off of your `HSM_secret`.

See the documentation for `makesecret` [here](https://lightning.readthedocs.io/lightning-makesecret.7.html?highlight=makesecret)

To find the pubkey of your node run:
```bash
$ lightning-cli nostrifypubkey
"npub1sqqres47s8x9ztva4nn525j5w72l23tvw0rh04t49h3gg5xccq7spvtqzs"
```

## Required Settings (`nostr_relay`, `nostr_pubkey`)

`Nostrify` sends events as DMs. To receive events as an encrypted DM you must set a pubkey in your config file.

You will also need to set some relays with the `nostr_relay` option, you can set multiple if you like. For example:

```
# Nostrify
nostr_relay=wss://nostr.klabo.blog
nostr_relay=wss://relay.damus.io
nostr_pubkey=2f4fa408d85b962d1fe717daae148a4c98424ab2e10c7dd11927e101ed3257b2
```

## Disabling Events

You can disable certain events from being sent by setting `nostr_disable_event` (you can set this multiple times). For example if you wanted to disable connection events and forwards that didn't succeed you could add this to your config file:

Events you can disable:
- connect
- disconnect
- forward_offered
- forward_failed

```
nostr_disable_event=connect
nostr_disable_event=disconnect
nostr_disable_event=forward_offered
nostr_disable_event=forward_failed
```

If there are others you want to disable open and issue and I'll try and add them.

### Example of Nostrify messages in Damus DM:

![IMG_537E93ECED3E-1](https://user-images.githubusercontent.com/264977/226097495-f598913c-9a82-4654-a802-aacb8bd315a9.jpeg)

### Optional last step

Follow me on nostr `npub19a86gzxctwtz68l8zld2u9y2fjvyyj4juyx8m5geylssrmfj27eqs22ckt` and send me a Zap or tip at `joel@klabo.blog` 🤙

# Contribute

If you find a bug or have feature requests file an issue. PRs are also welcomed 🤙
