List of methods for HPSBOT
**************************

Send the text message to the channel
------------------------------------
async def sendText(self, message, channel_id, user_name, team_id)

Return if the Robot is Ready to play
------------------------------------
async def play(self, channel_id, user_name, team_id)

Calculate who is the winner between the Player and the bot
----------------------------------------------------------
async def calculate(self, channel_id, user_name, team_id, player_choice)

Paper was selected from player 
------------------------------
async def paper(self, channel_id, user_name, team_id)

Hammer was selected from player
-------------------------------
async def hammer(self, channel_id, user_name, team_id)

Scissors was selected from player
---------------------------------
async def scissors(self, channel_id, user_name, team_id)

Displays the help message to the channel
----------------------------------------
async def help(self, channel_id, user_name, team_id)

Connection to the Slackbot
--------------------------
async def connect(self)

Send an error message to the channel, if a bad input was entered
----------------------------------------------------------------
async def error(self, channel_id, user_name, team_id)

Message treatment
-----------------
async def process(self, message)