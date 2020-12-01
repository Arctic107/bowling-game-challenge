import argparse

###
# Class Game
###
class Game:
    # The SCORE of the game starts at 0
    SCORE = 0
    # The current frame. Starts at 0 and goes until 9 (10th frame)
    FRAME_NUMBER = 0

    ###
    # Method play_game
    # Input: None
    # Output: The final score of the game as an integer
    # Description: Plays a game of bowling expecting a string with a valid game of bowl throws in it.
    #              The logic is: A strike(X) allows 2 bonus throws.
    #              A spare (/) allows 1 bonus throw
    #              A frame, except the 10th frame, allows for 2 throws to bowl down 10 pins
    #              A non-marked frame (no X or /) is the sum of the total pins downed in 2 throws
    #              The 10th frame allows for a third throw or a total of 3 strikes
    ###
    
    def play_game(self):
        # Iterate through each of the frames in the game
        for frame in self.frames:
            if self.DEBUG_MODE == 1:
                print('Frame: {} frame value: {} Score: {}'.format(self.FRAME_NUMBER,frame,self.SCORE))
            
            # Check if the current frame is the 10th frame and if there is a third throw. Else, treat everything like a regular frame until the 10th frame
            if self.FRAME_NUMBER == self.MAX_FRAME and len(frame) == self.TENTH_FRAME_MAX:
                if frame[self.CURRENT_THROW].upper() == self.STRIKE_VALUE:
                    if frame[self.BONUS_THROW_1].upper() == self.STRIKE_VALUE:
                        if frame[self.BONUS_THROW_2].upper() == self.STRIKE_VALUE:
                            self.SCORE += self.TURKEY_FRAME
                        else:
                            self.SCORE += self.DOUBLE_FRAME + int(frame[self.BONUS_THROW_2])
                    else:
                        if frame[self.BONUS_THROW_2].upper() == self.SPARE_VALUE:
                            self.SCORE += self.DOUBLE_FRAME
                        else:
                            self.SCORE += int(frame[self.BONUS_THROW_1]) + int(frame[self.BONUS_THROW_2])
                else:
                    self.SCORE += int(frame[self.CURRENT_THROW])
                    if frame[self.BONUS_THROW_2] == self.SPARE_VALUE:
                        self.SCORE += self.DOUBLE_FRAME
                    else:
                        self.SCORE += int(frame[self.BONUS_THROW_1]) + int(frame[self.BONUS_THROW_2])
            elif self.FRAME_NUMBER > self.MAX_FRAME:
                break
            else:
                if frame[self.CURRENT_THROW].upper() == self.STRIKE_VALUE:
                    if self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.CURRENT_THROW].upper() == self.STRIKE_VALUE:
                        if self.FRAME_NUMBER + self.BONUS_THROW_1 >= self.MAX_FRAME:
                            if self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.BONUS_THROW_1].upper() == self.STRIKE_VALUE:
                                self.SCORE += self.TURKEY_FRAME
                            else:
                                self.SCORE += self.DOUBLE_FRAME + int(self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.BONUS_THROW_1])
                        else:
                            if self.frames[self.FRAME_NUMBER + self.BONUS_THROW_2][self.CURRENT_THROW].upper() == self.STRIKE_VALUE:
                                self.SCORE += self.TURKEY_FRAME
                            else:
                                self.SCORE += self.DOUBLE_FRAME + int(self.frames[self.FRAME_NUMBER + self.BONUS_THROW_2][self.CURRENT_THROW])
                    elif self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.BONUS_THROW_1] == self.SPARE_VALUE:
                        self.SCORE += self.DOUBLE_FRAME
                    else:
                        self.SCORE += self.MARK_FRAME + int(self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.CURRENT_THROW]) + int(self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.BONUS_THROW_1])
                else:
                    self.SCORE += int(frame[self.CURRENT_THROW])
                    if frame[self.BONUS_THROW_1] == self.SPARE_VALUE:
                        if self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.CURRENT_THROW].upper() == self.STRIKE_VALUE:
                            self.SCORE += self.DOUBLE_FRAME
                        else:
                            self.SCORE += (self.MARK_FRAME-int(frame[self.CURRENT_THROW])) + int(self.frames[self.FRAME_NUMBER + self.BONUS_THROW_1][self.CURRENT_THROW])
                    else:
                        self.SCORE += int(frame[self.BONUS_THROW_1])

            # Increment the current frame by the FRAME_INCREMENTOR value
            self.FRAME_NUMBER += self.FRAME_INCREMENTOR
        
        return self.SCORE
        
    ###
    # Method reset_score
    # Input: None
    # Output: None
    # Description: Reset the score of the game to 0
    ###
    def reset_score(self,starting_score=0):
        self.score = starting_score
        
    def __init__(self):
        # Set debug mode (1 = ON and 0 = OFF)
        self.DEBUG_MODE = 0
        # The number of self.frames to move ahead by
        self.FRAME_INCREMENTOR = 1
        # The maximum frame is 9 (10th frame)
        self.MAX_FRAME = 9
        # The maximum number of throws in the 10th frame
        self.TENTH_FRAME_MAX = 3
        # The current throw
        self.CURRENT_THROW = 0
        # The first Bonus throw
        self.BONUS_THROW_1 = 1
        # The second Bonus throw
        self.BONUS_THROW_2 = 2
        # Turkey is 3 strikes in a row
        self.TURKEY_FRAME = 30
        # Double is 2 strikes in a row or a strike and a spare
        self.DOUBLE_FRAME = 20
        # Mark is the value of all of the pins in the lane
        self.MARK_FRAME = 10
        # A Strike is an X
        self.STRIKE_VALUE = 'X'
        # A Spare is a /
        self.SPARE_VALUE = '/'
		

parser = argparse.ArgumentParser(description='Play a game of bowling given a string of bowling values')
parser.add_argument('game_string',metavar='g',help='A string of valid bowling throws separated by dashes (-). Ex: 45-54-36-27-09-63-81-18-90-72')
parser.add_argument('-d','--debug_mode',type=int,default=0,help='Debug mode (0 is OFF and 1 is ON)')
args = parser.parse_args()

game = Game()
game.DEBUG_MODE = args.debug_mode
game.frames = args.game_string.split('-')
game.reset_score()
score = game.play_game()
print('The score of the game was: {}'.format(score))
