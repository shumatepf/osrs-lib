# osrs-lib

## Introduction
A Python library for interfacing to public OSRS assets. This library makes use of concurrent HTTP requests via [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://docs.aiohttp.org/en/stable/).

### Installation
`pip install osrs-lib`


## Hiscores
> The Old School Runescape public API rate limits requests and the exact rate limit is speculated. See [Reddit thread for speculation](https://www.reddit.com/r/2007scape/comments/57ah3w/comment/d8qjlls/?utm_source=share&utm_medium=web2x&context=3). Confirmation on this information was denied form Jagex via support ticket.
> This library attempts to rate limit requests maxed at 100 instantaneous requests or 15 per minute. As this has not been confirmed by Jagex, keep in mind your IP may be temporarily blocked if you attempt to make bulk requests.

The `hiscores` module can be used to fetch a single user or bulk users [OSRS hiscores](https://secure.runescape.com/m=hiscore_oldschool/overall) data.

Get user(s) stats:

```
from osrs-lib import hiscores

username = ['Zezima']

stats = hiscores.get_stats(username)
```

Get username(s) via rank:

```
from osrs-lib import hiscores

rank = [100]

username = hiscores.get_usernames(rank)
```
