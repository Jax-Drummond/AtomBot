# DiscordBot

A python discord bot

## How to use

1. Clone the repo
2. Rename config-example.py to config.py
3. Place your own bot token into config.py
4. There is no need to touch DEV_TOKEN unless you know what you're doing
5. Keep Environment as 'PROD' unless using DEV_TOKEN then use 'DEV'
6. Run `pip install -r requirements.txt`
7. Run bot.py
8. Profit

## Optional Config

+ `CLIENT_KEY_PTERO`, `APP_KEY_PTERO` and `BASE_URL` are for if you want to use commands pertaining to pterodactyl
+ `CF_CLIENT_ID` and `CF_CLIENT_SECRET` are also for Ptero if you have the panel behind Cloudflare