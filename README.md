# PKT Mining Monitor bot
Monitor your PKT miners with this Telegram bot.

The bot can send the user a message each day at a fixed time with some mining statistics. It shows the balance of the PKT address, mining income yesterday, 7 days and 30 days ago. It can show the amount of unconsolidated transactions and tells you if you need to fold your coins again.

## Screenshot

![Screenshot of the PKT Mining Monitor bot](/docs/screenshot1.png?raw=true)

## Available commands

* `/start` Displays a welcome message.
* `/add_address <address>` Adds a PKT address to your list.
* `/remove_address <address>` Removes a PKT address from your list.
* `/list_addresses` View the PKT addresses on your list.
* `/set_time <time>` Set the time of the subscription message.
* `/set_timezone <timezone>` Set the timezone for the time of the message.
* `/subscribe` Start/update the subscription.
* `/stop` Stop the subscription.
* `/help` Shows this list.

## How to run it?

For now, you cannot use the bot I created yet. But you can run it yourself:

* Create your own bot by talking to Telegram's [BotFather](https://t.me/botfather) and get the API token of your bot.
* Install Python if you don't have it yet.
* Install the required [Python Telegram bot](https://python-telegram-bot.org/) library by running `pip install python-telegram-bot`. (You may need to use `pip3`.)
* Install the required [Python dotenv](https://pypi.org/project/python-dotenv/) library by running `pip install python-dotenv`. (You may need to use `pip3`.)
* Put your bot API token in a file called `.env`, in this format: `PKT_MINING_BOT_TOKEN = "<your bot's API token goes here>"`.
* Run the bot with `python main.py`.
* Talk to the bot :)

## How it gets the data

The bot uses the [PKT explorer backend API v1](https://github.com/pkt-cash/pkt-explorer-backend/blob/master/docs/apiv1.md). If you run this software yourself, you can connect it to your own block explorer.

Example call:
`https://explorer.pkt.cash/api/v1/PKT/pkt/address/pkt1q6hqsqhqdgqfd8t3xwgceulu7k9d9w5t2amath0qxyfjlvl3s3u4sjza2g2`

Output:
```
{
	"unconfirmedReceived": "0",
	"confirmedReceived": "303822882552892309",
	"balance": "98040804557295380",
	"spending": "0",
	"spent": "85006797353036390",
	"burned": "120775280642560539",
	"recvCount": 558,
	"mineCount": 371921,
	"spentCount": 98517,
	"balanceCount": 132653,
	"mined24": "1017057152397603"
}
```

## To-do

- Percentage statistics, compare daily income to previous values
- Nice graphs?
- Many other things...

## License

MIT