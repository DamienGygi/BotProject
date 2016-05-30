#Create by Damien Gygi and Raphaël Schaffo
#INF2 DLM A
#HE ARC année 2015-2016

"""Sample Rock Paper Scissors Slackbot"""
import asyncio
import json
import aiohttp
import random

from api import api_call
from config import DEBUG, TOKEN
from random import choice

class RPSBot:
    
    def __init__(self, token=TOKEN):
        self.token = token
        self.rtm = None
        self.api = {
		    "scissors":self.scissors,
		    "rock":self.rock,
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
           	
    async def rock(self, channel_id, user_name, team_id):
            """ Rock was selected from player """	
            return await self.calculate(channel_id, user_name, team_id,0)
							
    async def scissors(self, channel_id, user_name, team_id):
            """ Scissors was selected from player """	
            return await self.calculate(channel_id, user_name, team_id,2)	
			
    async def help(self, channel_id, user_name, team_id):
        """Displays the help message to the channel"""
        helpMessage = "Welcome to our RPSBot! \n" \
                      "This bot is here for you to have fun in your spare time. \n" \
                      "There is a list of commands : \n" \
                      " - play : is the bot ready to play. \n" \
                      " - paper : selected paper for game. \n" \
                      " - rock : selected rock for game. \n" \
                      " - scissors : selected scissors for game. \n" \
                      "Have fun !"
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
        error = "This command is not found. Use Help for list of commands"
        return await self.sendText(error, channel_id, user_name, team_id)
		
	#Function found on Github, created by CyrillManuel
    async def process(self, message):
        """ Message treatment""" 
        if message.get('type') == 'message':

            # Channel-related entries
            channel_id = message.get('channel')
            channel_name = await api_call('channels.info', 							 # gets the name of the channel for given id
                                          {'channel': message.get('channel')})  	 # doesn't work all the time

            # Team-related entries
            team_id = self.rtm['team']['id']  										 # gets id of the active team
            team_name = self.rtm['team']['name']  									 # gets name of the active team

            # User-related entries
            user_id = message.get('user')
            user_name = await api_call('users.info', 								 # gets user name based on id
                                       {'user': message.get('user')})

            # Self-related entries
            bot_id = self.rtm['self']['id']  										 # gets id of self, meaning the bot.
            bot_name = self.rtm['self']['name'] 									 # gets its name

            # message related entries
            message_text = message.get('text')

            # Splits message in half												 # Recipient on the left side, and the core text on the other.
            if (isinstance(message_text, str)):
                message_split = message_text.split(':', 1)  						 # Generate an exception if type is different than text.
                recipient = message_split[0].strip()

                if len(message_split) > 0 and recipient == '<@{0}>'.format(bot_id):  # If message is adressed to our bot
                    core_text = message_split[1].strip()
                    action = self.api.get(core_text) or self.error
                    print(await action(channel_id, user_name, team_id))

    
	
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(DEBUG)
    bot = RPSBot(TOKEN)
    loop.run_until_complete(bot.connect())
    loop.close()
