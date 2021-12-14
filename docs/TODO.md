### Developer TODOs

#### Deployment
- [x] Set up `semantic-release` for automatically versioning and tagging from commit messages
- [x] Set up `setuptools_scm` to automatically version the python package from git tags
- [x] Set up `twine publish` command in Makefile, and include in requirements.dev.txt 
- [x] Rename bot and refactor
- [x] Add to pypi (Already added to test.pypi)
- [x] Add [[Github Actions]] for pypi
- [x] Add [[Github Actions]] for [docker hub](https://medium.com/rockedscience/docker-ci-cd-pipeline-with-github-actions-6d4cd1731030)
- [x] Add docs to DockerHub (even just a backlink to github would do)

#### Bot Development
- [ ] Add emojis to rates embeds
- [ ] Add docs explaining current auto-publishing functionality
- [x] Add more debugging code
- [x] Auto-publishing in announcement channels
- [x] Rework `rates.py` to make use of RatesStatus and RatesDiff
server
- [ ] Add delay between change detection and sending embed, where another check is performed after delay

#### Low Priority / Next Release
- [x] Add ability to post other server rates. Rather than just using the `dynamicconfig.ini` endpoint, perhaps add a parameter that takes in a list of endpoints, ex. `["pc_smalltribes_dynamicconfig.ini", "xbox_smalltribes_dynamiconfig.ini"]`. Alternatively, combine all rates into a table that gets added to the embed.
- [ ] Rework bans.py to make use of bans models
- [ ] Reformat ban summary output
- [ ] Make `bans.py` edit the embed rather than sending a new one
- [ ] Add auto-publish/no publish as a parameter for each cog, perhaps `auto-publish-channels = [<chan_ID1>, <chan_ID1>]`
- [ ] In-game server notifications posted to Discord channels
- [x] Convert to use `setup.cfg` instead of `setup.py`
- [x] Add `old_rates` and `current_rates` to `RatesDiff` so `self.current_rates` could be used instead of `to_embed` 
- [x] Allow for `old_rates=old` and `new_rates=new` to be passed into `RatesStatus.to_diff()`  
- [ ] Add ability to provide custom rates URL
- [ ] Add a check that will explicitly state that a certain platform's rates have changed if they differ from the rates of the same game mode on other platforms
