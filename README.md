# WidenBot

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=eb2eb2fc76ce&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

WidenBot is a private music bot for Discord.

## Setup Guide

**Disclaimers:**

**WidenBot is introverted, and not intended to be a plug-and-play music bot that can be added to a server in a couple of clicks. It requires some manual setup, and hosting is up to you. For an out-of-the-box experience, the WidenBot team recommends [CakeyBot](https://cakey.bot/), or Tanner Gabriel's [discord-bot](https://github.com/TannerGabriel/discord-bot) repo as alternatives to this project.**

**A single instance of WidenBot cannot serve more than one server at a time. This is by design; WidenBot just wants to hang out with you and your friends, no one else.**

WidenBot consists of three components:

- A discord bot, configured via the Discord developer portal
- The server ([Lavalink](https://github.com/lavalink-devs/Lavalink)), a standalone Java application
- The client (WidenBot), a .NET service

### Part 1: Dependencies

- Python 3
- .NET SDK 7 or newer
- JRE 17 or newer (OpenJDK recommended)

Make sure the outputs of `python --version`, `dotnet --list-sdks`, and `java --version` each look correct before continuing.

### Part 2: Discord Bot

1. Go to the Discord Developer Portal, login as the Discord account should own the bot, and create a new application

2. Within the Bot settings:

   a. Disable "Public Bot" (optional, but recommended)

   b. Enable "Server Members Intent" and "Message Content Intent"

   c. Click the "Reset Token" button and save the resulting token for later

3. Within the OAuth settings:

   a. Add a redirect for `https://discord.com` (Under "General" sub-category)

   b. Generate an invite URL with the `bot` scope, and the following bot permissions:

   - Read Messages/View Channels
   - Send Messages
   - Manage Messages
   - Add Reactions
   - Use Slash Commands
   - Connect
   - Speak

4. Use the generated URL to invite the bot to a server of your choice

5. In Discord, right-click on the server you invited the bot to, select "Copy Server ID", and paste the server ID somewhere for later

### Part 3: WidenBot

1. Clone this repository

2. Copy the contents of `config.template.json` into a new file called `config.json`

3. Provide the bot token from step 2c above as the value for `DiscordBotToken`

4. Provide the server ID from step 6 above as the value for `DiscordServerID`

5. Using a Google account that you have access to, enter the email + password combo into `YoutubeEmail` and `YouTubePassword` respectively

6. From the root of the repository, execute `python3 setup.py`

7. Change to the `Lavalink` directory and execute `java -jar Lavalink.jar`. On first run, inspect the output. If you see any log messages about failing OAuth to Google / Youtube, follow the instructions in the log message, you may need to grant permissions to YouTube. This OAuth portion should be a one-time step per WidenBot setup.

8. Once the Lavalink output looks good, open another terminal window in the `WidenBot` directory, and execute `dotnet run -c Release`.

9. Done! The bot user you invited should now be online, and slash commands should be available.

## TODO

- More commands: skip, pause and resume
- Better default volume on join
- Leave when voice channel empty
- Handle Spotify / other sources, handle playlists
- SponsorBlock plugin
