# Stateless chatroom (high volume takeover) proof of concept

After my coffee this morning, I felt curious about Server Sent Events (SSE - the new-to-me idea that I was mentioning at the start of our conversation)
 and how implementing that with the stateless high volume takeover chatroom design I came up with at the end of our chat would sorta look like. 
By no means is this solution intended to be complete or even the best idea - heck I've come up with a bunch of other alternatives while just going about my day yesterday!
With this, I'm simply trying to show some base level possibility of the idea - we'd have to scale this up/out a bit and do some more calculations to figure out the load specifics.

NOTE: This was my first time using a few technologies here (Bottle, SSE, Gevent) so apologies if there's some less-then-ideal practices in here :)


## What's not included
- Any routing logic
- Auth
- Tests
- invalidating SSE connections as new high-load chatrooms are requested (HTTP/1.1 has very low limits on active connections, but HTTP/2 solves this issue)
- the low volume solution with websockets
- switchover logic to go from low volume to high volume and back
- cleaning up kafka topics when no longer needed (there's a very real limit to partitions in a cluster due to zookeeper [that will go away soon](https://www.confluent.io/blog/kafka-without-zookeeper-a-sneak-peek/#scaling-up) when kafka ditches ZK)
- etc.


## How to run
The intention here is to just show you how this code would look. If you need a hand setting up the containers to test this, please DM me - I can write a docker compose file for you in a jiffy!  Personally, I connected to some pre-existing kafka/postgres containers I have on my machine that made this proof of concept quick and painless.
