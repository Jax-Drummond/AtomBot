# AtomBot

A Python Discord bot

## How to Use

1. Clone the repository using `git clone https://github.com/NotAtomicBomb/AtomBot`
2. Rename `config-example.py` to `config.py`
3. Place your own bot token into `config.py`
4. There is no need to modify `DEV_TOKEN` unless you are testing, in which case set it to 'DEV'
5. Keep the `Environment` variable as 'PROD' unless using `DEV_TOKEN`, in which case set it to 'DEV'
6. Install required dependencies using `pip install -r requirements.txt`
7. Download and install MySQL from [here](https://dev.mysql.com/downloads/mysql/)
8. Update the MySQL username and password in `config.py` to your MySQL credentials
9. Create a schema called `atombot` in your MySQL database
10. Run `bot.py`
11. Profit!

## Optional Configuration

- `CLIENT_KEY_PTERO`, `APP_KEY_PTERO`, and `BASE_URL` are used for commands related to Pterodactyl.
- `CF_CLIENT_ID` and `CF_CLIENT_SECRET` are also for Pterodactyl if the panel is behind Cloudflare.

## Reason for Chosen License

I chose the BSD 3-Clause "New" or "Revised" license because it permits commercial use, modification, distribution, and private usage of the code. However, it provides limited liability and no warranty. It also requires the license and copyright notice to be included with the licensed material.

## Troubleshooting

- If you encounter any issues during setup, feel free to open an issue on GitHub.
