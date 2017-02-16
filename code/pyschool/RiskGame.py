'''
In the Risk board game, 
there is the situation where the attacker rolls 3 dice while the defender rolls 2 dice. 
To determine the outcome, the highest die of each player is compared, 
followed by the next highest die. For each case, 
the attacker's die has to be higher than that of the defender to win. 
The loser will lose 1 army in each case.
Examples
    >>> RiskGame([1,2,6], [1, 5])
    'Defender loses 2 armies.'
    >>> RiskGame([6,2,6], [6, 6])
    'Attacker loses 2 armies.'
    >>> RiskGame([1,4,1], [1, 2])
    'Attacker loses 1 army and defender loses 1 army.'
'''

def RiskGame(attacker, defender):
        attacker.sort(reverse=True)
        defender.sort(reverse=True)
        atta = attacker
        defe = defender
        atta_lose = 0
        defe_lose = 0

        for i in range(0,2):
            if atta[i] > defe[i]:
                defe_lose += 1
            else:
                atta_lose += 1

        print ('atta_lose ', atta_lose)
        print ('defe_lose ', defe_lose)

if __name__ == '__main__':
    RiskGame([1,2,6], [1, 5])
    RiskGame([6,2,6], [6, 6])
    

def RiskGame(attacker, defender): 
	attacker.sort(reverse=True)
	defender.sort(reverse=True)
	atta = attacker
	defe = defender
	defe_lose = 0
	atta_lose = 0	
	for i in range(0,2):
		if atta[i] > defe[i]:
		# defender lose 1 army
			defe_lose += 1
		else:
		# attacker lose 1 army
			atta_lose += 1			
			
	if atta_lose > 0 and defe_lose > 0:
		return 'Attacher loses %d army and defender loses %d army.' % atta_lose defe_lose		
			
	