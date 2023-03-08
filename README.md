# Booklet
Monorepo of a super light order-book for pre-PMF exchanges.

The goals is to create the simplest MVP that'll break just beyond the point of Product-Market-Fit.

## PMF

Defining this is tough, but using dYdX/Deribit as a conservative threshold, we can come to these conclusions:
- @ 10,000 req/sec, response around 100ms 
- up to 4GB live order-book size
- up to 2000 traders per sec + ~5 highly-active market makers 
- Catch up to latest order-book state in <5 sec
- Ability to roll back if settlement layer reverts

Some other important atttributes:
- Chain / settlement agnostic
- KYC plug-in functionality
- An easy language that the whole team can contrubite in

## Architecture [In-Progress]

Language: Python
REST + WebSocket + Redis