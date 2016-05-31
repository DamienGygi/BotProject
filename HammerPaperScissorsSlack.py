#Create by Damien Gygi and Raphaël Schaffo
#INF2 DLM A
#HE ARC année 2015-2016

"""Sample Hammer Paper Scissors Slackbot"""
import asyncio
import json
import aiohttp
import random

from api import api_call
from config import DEBUG, TOKEN
from random import choice

class HPSBot:
    
    def __init__(self, token=TOKEN):
        self.token = token
        self.rtm = None
        self.api = {
		    "scissors":self.scissors,
		    "hammer":self.hammer,
		    "paper":self.paper,
            "play": self.play,
            "help": self.help
        }
		
    async def sendText(self, message, channel_id, user_name, team_id):
        """Send the text message to the channel"""
        return await api_call('chat.postMessage', {"type": "message",
                                                   "channel": channel_id,
                                                   "text": "<@{0}> {1}".format(user_name["user"]["name"], message),
                                                   "team": team_id})

    async def play(self, channel_id, user_name, team_id):
        """Return if the Robot is Ready to play """
        return await self.sendText('The Robot is ready to play !', channel_id, user_name, team_id)
	
    async def calculate(self, channel_id, user_name, team_id, player_choice):
            """Calculate who is the winner between the Player and the bot"""
            bot_choice = choice(range(3))
            possibilities = ("hammer", "spiral_note_pad", "scissors")
            if player_choice== bot_choice:
                return await self.sendText("\nYou chose: :{}: and the bot chose: :{}:, it's a tie".format(possibilities[player_choice], possibilities[bot_choice]), channel_id, user_name, team_id)
            elif (player_choice>bot_choice and bot_choice+1==player_choice) or (player_choice<bot_choice and player_choice+bot_choice==2):
                return await self.sendText("\nYou chose: :{}: and the bot chose: :{}:, so you win".format(possibilities[player_choice], possibilities[bot_choice]), channel_id, user_name, team_id)
            else:
                return await self.sendText("\nYou chose: :{}: and the bot chose: :{}:, so you lose".format(possibilities[player_choice], possibilities[bot_choice]), channel_id, user_name, team_id)
				
    async def paper(self, channel_id, user_name, team_id):
            """ Paper was selected from player """
            return await self.calculate(channel_id, user_name, team_id,1)
           	
    async def hammer(self, channel_id, user_name, team_id):
            """ Hammer was selected from player """	
            return await self.calculate(channel_id, user_name, team_id,0)
							
    async def scissors(self, channel_id, user_name, team_id):
            """ Scissors was selected from player """	
            return await self.calculate(channel_id, user_name, team_id,2)	
			
    async def help(self, channel_id, user_name, team_id):
        """Displays the help message to the channel"""
        helpMessage = "Welcome to our HammerPaperScissors Slack Bot! \n" \
                      "This bot was created for your spare time \n" \
                      "Here is a list of all existing commands: \n" \
                      " - play : is the bot ready to play. \n" \
                      " - paper : select paper for the next game. \n" \
                      " - hammer : select hammer for the next game. \n" \
                      " - scissors : select scissors for the next game. \n" \
					  " You can also use Hammer, Paper, Scissors emojis to play \n" \
                      "Have fun ! "
        return await self.sendText(helpMessage, channel_id, user_name, team_id)

    async def connect(self):
        """Connection to the Slackbot"""
        self.rtm = await api_call('rtm.start')
        assert self.rtm['ok'], self.rtm['error']

        with aiohttp.ClientSession() as client:
            async with client.ws_connect(self.rtm["url"]) as ws:
                async for msg in ws:
                    assert msg.tp == aiohttp.MsgType.text
                    message = json.loads(msg.data)
                    asyncio.ensure_future(self.process(message))	
		
    async def error(self, channel_id, user_name, team_id):
        """Send an error message to the channel, if a bad input was entered"""
        error = ":warning: This command is not found. Use the help for more infos about HPSBot."
        return await self.sendText(error, channel_id, user_name, team_id)
	

    async def process(self, message):
        """ Message treatment""" 
        if message.get('type') == 'message':

            # Channel ID
            channel_id = message.get('channel')
			
            # Team ID
            team_id = self.rtm['team']['id']  										 

            # User ID and Name
            user_id = message.get('user')
            user_name = await api_call('users.info',{'user': message.get('user')})

            # Bot ID (self ID)
            bot_id = self.rtm['self']['id'] 
			
            # Message
            message_text = message.get('text')

            # Get content from Message												 
            if (isinstance(message_text, str)):
                message_split = message_text.split(':', 1)  						 
                recipient = message_split[0].strip()
                # If the recipient for this message is your bot
                if len(message_split) > 0 and recipient == '<@{0}>'.format(bot_id):  
                    core_text = message_split[1].strip()
                    if core_text.startswith(":") and core_text.endswith(":"):
                        core_text=core_text[1:-1]
                        if core_text=="spiral_note_pad":
                            core_text="paper"
                    action = self.api.get(core_text) or self.error
                    print(await action(channel_id, user_name, team_id))

    
	
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(DEBUG)
    bot = HPSBot(TOKEN)
    loop.run_until_complete(bot.connect())
    loop.close()
