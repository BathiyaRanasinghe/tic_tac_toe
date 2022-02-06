# Tic Tac Toe v1


import pygame


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Tic Tac Toe')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        # Call to the class method to set the surface for the Tile objects
        # <name of the class>.<name of the class method>()
        Tile.set_surface(self.surface)
        self.board = []
        self.create_board()
        self.player_1 = 'X'
        self.player_2 = 'O'
        self.turn = self.player_1
        
    def create_board(self):
        width = self.surface.get_width()//3
        height = self.surface.get_height()//3
        for row_index in range(0,3):
            row = []
            for col_index in range (0,3):
                x = width * col_index
                y = height * row_index
                tile = Tile(x, y, width, height)
                row.append(tile)
            self.board.append(row)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos)
        
    def handle_mouse_up(self, position):
        # position is the (x,y) location of the click and is of type tuple
        for row in self.board:
            for tile in row:
                if tile.select(position, self.turn) == True: # click inside an unoccupied tile
                    self.change_turn()
                        
    def change_turn(self):
        if self.turn == self.player_1:
            self.turn = self.player_2
        else:
            self.turn = self.player_1

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        # draw the grid
        for row in self.board:
            for tile in row:
                tile.draw()
       
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        pass

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        pass


class Tile:
    # Class attributes are attributes that are same for all Tile object
    surface = None
    border_width = 3
    border_color = pygame.Color('white')
    font_size = 133
    
    @classmethod
    # A class method is used to set or change the value of a class attribute
    def set_surface(cls, surface_from_Game):
        # cls is a parameter gets bound to the name of the class which is a Tile
        # -surface_from_Game get bound to the object the argument self.surface is bound to
        cls.surface = surface_from_Game
    # Instance Methods                 
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.content = ''
        self.flashing = False
        
    def draw(self):        
        if self.flashing == True:
            # draw white rectangle
            pygame.draw.rect(Tile.surface, Tile.border_color, self.rect)
            self.flashing = False
        else:
            # a black rectangle with 3 pixel white border
            pygame.draw.rect(Tile.surface, Tile.border_color, self.rect, Tile.border_width)
            self.draw_content()
            
    def draw_content(self):
        # size, color, location 
        font = pygame.font.SysFont('', Tile.font_size)
        # render the font object
        text_box = font.render(self.content, True, Tile.border_color)
        # location - top left corner of the text_box
        text_box_width = text_box.get_width()
        text_box_height = text_box.get_height()
        d_x = (self.rect.width - text_box_width)//2
        d_y = (self.rect.height - text_box_height)//2
        x = self.rect.x + d_x
        y = self.rect.y + d_y
        Tile.surface.blit(text_box, (x,y))
        
    def select(self, position, current_player):
        valid_click = False
        if self.rect.collidepoint(position):
            if self.content == '':
                self.content = current_player
                valid_click = True
            else:
                self.flashing = True
        return valid_click

main()