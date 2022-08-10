# Changelog

<!--next-version-placeholder-->

## v0.2.1 (10/08/2022)

### Feature
- Added a parameter to update WaniKani item database when initialize the bot.

### Known Issues
- `/search` command throws error since the database structure is changed.

<!--next-version-placeholder-->

## v0.2.0 (09/08/2022)
Migrating Python API wrapper for Discord from [Disnake](https://github.com/DisnakeDev/disnake) to [Pycord](https://github.com/Pycord-Development/pycord).

### Feature
- Added WaniKani item database from [CrabigatorBot](https://github.com/saraqael-m/CrabigatorBot)'s saraqael repository.
- Added new `/search` command to get the detail of a specific WaniKani item.
- Added hello indicator when the bot is online.

### Change
- Change some output from previous commands.

<!--next-version-placeholder-->

## v0.1.0 (08/08/2022)
First release of `crabigator-bot` using [Disnake](https://github.com/DisnakeDev/disnake) library based on a [template](https://github.com/kkrypt0nn/Python-Discord-Bot-Template) from kkrypt0nn.

### Feature
- Added `/botinfo` command to get some information about the bot.
- Added `/wani` command to get the latency of the bot.
- Added `/shutdown` command to shutdown the bot from Discord server.