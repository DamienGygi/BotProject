def run():
	import HammerPaperScissorsSlack
	import asyncio
	DEBUG = True

	loop = asyncio.get_event_loop()
	loop.set_debug(DEBUG)
	bot = HammerPaperScissorsSlack.HPSBot()
	loop.run_until_complete(bot.connect())
	loop.close()
