from random import choice
textFromBot = input("Want play with me ?")
if textFromBot=='Yes':
			coup = ("ROCK", "PAPER", "SCISSORS")
			print("\n------------------------------------")
			print("Rock - Paper - Scissors")
			print("------------------------------------\n")
		 
			a = int(input("Make your choice:\n0: Rock\n1: Paper\n2: Scissors\n-> "))
			b = choice(range(3))
		 
			print("\nYOU:{} VS {}:BOT".format(coup[a], coup[b]))
			if a == b:
				print("TIE\n")
			elif (a>b and b+1==a) or (a<b and a+b==2):
				print("YON WIN\n")
			else:
				print("YOU'RE LOSER\n")
