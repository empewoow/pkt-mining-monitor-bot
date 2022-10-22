# PKT Miner Monitor bot
Monitor your PKT miner with this Telegram bot.

The bot can send the user a message each day at a fixed time with some mining statistics. It shows the balance of the PKT address, mining income yesterday, 7 days and 30 days ago. It can show the amount of unconsolidated transactions and tells you if you need to fold your coins again.

## Screenshot

![Screenshot of the PKT Miner Monitor bot](/docs/screenshot1.png?raw=true)

## How to run it?

For now, you cannot use the bot I created yet. But you can run it yourself:

* Create your own bot by talking to Telegram's [BotFather](https://t.me/botfather).
* Install Python if you don't have it yet.
* Install the required [Python Telegram bot](https://python-telegram-bot.org/) library by running `pip install python-telegram-bot`. (You may need to use `pip3`.)
* Configure some settings in the `constants.py` file.
* Run the bot with `python main.py`.
* Talk to the bot and say the `/start` command.

## How it get's the data

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
- Multiple users
- Multiple PKT addresses
- Nice graphs?
- Many other things...

## License

MIT