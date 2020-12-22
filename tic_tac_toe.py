import curses

class Game:
    def __init__(self):
        #Curses vars (display only)
        self.screen = curses.initscr()
        self.screen.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.x_color = curses.color_pair(2)
        self.o_color = curses.color_pair(3)
        self.default_color = curses.color_pair(1)
        self.winner_color = curses.color_pair(4)
        #Game vars
        self.grid = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.player = 1;
        self.game_over = False

    def draw_grid(self):
        #!!!DO NOT ALTER GRID!!! without adjusting x/y counter variables
        line1 = "   |   |   "
        line2 = "___|___|___"
        line3 = "   |   |   "
        line4 = "___|___|___"
        line5 = "   |   |   "
        line6 = "   |   |   "
        gridLines = [line1, line2, line3, line4, line5, line6]
        #Draw Grid
        for line in range(len(gridLines)):
            self.screen.addstr(line, 0, gridLines[line])
        self.screen.refresh()
        xcounter = 1
        ycounter = 0
        winner_squares = self.check_for_winner()
        for square in range(len(self.grid)):
            #Determine color
            if self.grid[square] == 'X' and square +1 not in winner_squares:
                color = self.x_color
            elif self.grid[square] == 'O' and square +1 not in winner_squares:
                color = self.o_color
            elif square +1 in  winner_squares:
                color = self.winner_color
            else:
                color = self.default_color
            #Place in grid
            self.screen.addstr(ycounter, xcounter, self.grid[square], color)
            if xcounter == 9:
                xcounter = 1
                ycounter += 2
            else:
                xcounter += 4

    def pick_square(self):
        loop = True
        while loop == True:
            self.screen.addstr(7, 1, "Choose an unoccupied cell:")
            #Clear response area
            self.screen.move(8, 1)
            self.screen.clrtoeol()
            #Get response
            response = self.screen.getstr(8, 1).decode('utf-8')
            #Add symbol to grid selection based on player number
            if response in self.grid and response != 'X' and response != 'O':
                symbol = ''
                if self.player == 1:
                    symbol = 'X'
                else:
                    symbol = 'O'
                self.grid[self.grid.index(response)] = symbol
                loop = False

    def check_for_winner(self):
        #All possible winning combinations listed
        horizontals = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        verticals = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        diagonals = [[1, 5, 9], [3, 5, 7]]
        win_conditions = [horizontals, verticals, diagonals]
        for direction in range(len(win_conditions)):
            for combination in range(len(win_conditions[direction])):
                #Checks if all symbols in current combination match
                if self.grid[win_conditions[direction][combination][0]-1]==self.grid[win_conditions[direction][combination][1]-1] and self.grid[win_conditions[direction][combination][0]-1]==self.grid[win_conditions[direction][combination][2]-1]:
                    self.game_over = True
                    #Returns winning combination for coloring purposes
                    return win_conditions[direction][combination]
        #Check if no winner and all squares occupied
        if self.check_for_cats_game() == True:
            self.game_over = True
        #If no winner, return blank array
        return []

    def check_for_cats_game(self):
        for num in range(1, 10):
            #If any squares have a number 1-9, the game is not over
            if str(num) in self.grid:
                return False
        #If all squares have a symbol and there is no winner, cats game is True
        return True

    def game(self):
        #Initialize grid of numbers 1-9
        self.draw_grid()
        while self.game_over == False:
            self.pick_square()
            self.draw_grid()
            #Switch whose turn it is
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1
            #Display Game Over Text if game ends
            if self.game_over == True:
                self.screen.move(7, 1)
                self.screen.clrtoeol()
                self.screen.addstr(7, 1, "Game Over!")
                self.play_again()

    def play_again(self):
        loop = True
        while loop == True:
            #Clear lines of previous texts/responses
            self.screen.move(8, 1)
            self.screen.clrtoeol()
            self.screen.move(9, 1)
            self.screen.clrtoeol()
            self.screen.addstr(8, 1, "Play again? (Y/N)")
            #Get response
            response = self.screen.getstr(9, 1).decode('utf-8')
            if response.upper() == 'Y': #Reset Game
                loop = False
                self.reset_game()
            elif response.upper() == 'N': #End Game
                loop = False
                self.screen.addstr(10, 1, "Thanks for playing!")
                response = self.screen.getstr(11, 1).decode('utf-8')

    def reset_game(self):
        #Reset all game vars to their initial state
        self.game_over = False
        self.player = 1
        self.grid = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        #Clear screen of previous texts and start the game
        self.screen.clear()
        self.game()


#PLAY!
game = Game()
game.game()