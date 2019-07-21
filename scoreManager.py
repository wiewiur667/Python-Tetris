import time
class ScoreManager:
    currentScore = 0
    currentMultiplier = 1
    maxMultiplier = 0
    multiplierTimeout = 0
    multiplierTimeoutClock = 0
    lineValue = 0

    def __init__(self, multiplierTimeout):
        self.multiplierTimeout = multiplierTimeout

    def __update_multiplier(self):
        if(self.currentMultiplier <= self.maxScoreMultiplier):
            if(self.multiplierTimeout > 0):
                self.currentMultiplier = self.scoreMultiplier * 2
            else:
                self.currentMultiplier = 1

    def updateScore(self, score):
        self.currentScore = self.currentScore + score * (self.currentMultiplier)
        