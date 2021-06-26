from pygame.math import Vector2 as vec

#screen settings
WIDTH, HEIGHT = 650, 650
FPS = 24
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

#color setting
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

#FONT SETTINGS
START_TEXT_SIZE = 17
START_FONT = 'arial black'

#player setting
# PLAYER_START_POS = vec(8, 28)
PLAYER_START_POS = vec(7, 3)

#dead-end setting
#DEAD_END_POS = [(4, 3), (25, 10), (3, 22), (24, 26)]
# DEAD_END_POS = (3, 22)
DEAD_END_POS = (1, 1)

#destination setting
# DESTINATION_POS = (28, 5)
DESTINATION_POS = (9, 1)


DEST_VEC = vec(28, 5)



