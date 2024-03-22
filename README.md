# DiscordBot

A python discord bot

## How to use

1. Clone the repo via `git clone https://github.com/NotAtomicBomb/AtomBot`
2. Rename config-example.py to config.py
3. Place your own bot token into config.py
4. There is no need to touch DEV_TOKEN unless you know what you're doing
5. Keep Environment as 'PROD' unless using DEV_TOKEN then use 'DEV'
6. Run `pip install -r requirements.txt`
7. Download MySQL
8. Change config.py DB username and password to your MySQL password
9. Create a schema called `atombot`
10. Run bot.py
11. Profit

## Optional Config

+ `CLIENT_KEY_PTERO`, `APP_KEY_PTERO` and `BASE_URL` are for if you want to use commands pertaining to pterodactyl
+ `CF_CLIENT_ID` and `CF_CLIENT_SECRET` are also for Ptero if you have the panel behind Cloudflare


## Reason for LICENSE chosen
I chose the BSD 3-Clause "New" or "Revised" license because it allows people to use the code in this repo in commercial use, to modify it, distribute, and or use it privately. However, this license does state that there is 
limited liability and that no warranty will be provided. It also states that the license and copyright notice needs to be included with this licensed material.
