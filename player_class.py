import pygame, sys
from settings import *
### RL imports ###
from rl_settings import *
import numpy as np
import cv2
import pickle
###############
vec = pygame.math.Vector2

class player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        #print(self.grid_pos)

        # setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width//2-2)

        # Drawing the grid postion rect
        #pygame.draw.rect(self.app.screen, RED,
        #                 (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                 self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2,
        #                 self.app.cell_width, self.app.cell_height), 1)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2, (self.grid_pos.y * self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)
        #print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True

    def dead_end(self):
        if self.grid_pos == DEAD_END_POS:
            print("Dead End")
            # self.q_learning()
            pygame.quit()
            sys.exit()
        #else:
            #print("Safe!")

    def destination(self):
        if self.grid_pos == DESTINATION_POS:
            print("Destination reached!")
            pygame.quit()
            sys.exit()

    def action(self, choice):
        #if not choice:
         #   choice = np.random.randint(3)
        if choice == 0:
            self.move(vec(-1, 0))
        elif choice == 1:
            self.move(vec(1, 0))
        elif choice == 2:
            self.move(vec(0, -1))
        elif choice == 3:
            self.move(vec(0, 1))



########################################################################################################################


  # ######################### RL #######################################
    #


    if start_q_table is None:
        # initialize the q-table#
        q_table = {}
        for i in range(-SIZE + 1, SIZE):
            for ii in range(-SIZE + 1, SIZE):
                for iii in range(-SIZE + 1, SIZE):
                    for iiii in range(-SIZE + 1, SIZE):
                        q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]

    else:
        with open(start_q_table, "rb") as f:
            q_table = pickle.load(f)

    # print(q_table[((-9, -2), (0, -2))])



    def q_learning(self):

        #destination = (28, 5)
        epsilon = 0.1

        episode_rewards = []
    #
        for episode in range(episodes_count):
            self.app.playing_update()
            self.app.playing_draw()
            #player = App()

            player_pos = tuple(self.grid_pos)
            if episode % show_game_every == 0:
                print(f"on #{episode}, epsilon is {epsilon}")
                print(f"{show_game_every} ep mean: {np.mean(episode_rewards[-show_game_every:])}")
                show = True
            else:
                show = False
    #
            episode_reward = 0
            for i in range(2):
                sample = tuple(np.subtract(player_pos, DESTINATION_POS))
                sample2 = tuple(np.subtract(player_pos, DEAD_END_POS))
                obs = (tuple(int(i) for i in sample), tuple(int(i) for i in sample2))
                #obs = (tuple(np.subtract(player_pos, DESTINATION_POS)), tuple(np.subtract(player_pos, DEAD_END_POS)))
                #obs = math.sqrt(((player_pos[0]-DESTINATION_POS[0])**2)+((player_pos[1]-DESTINATION_POS[1])**2))
                #, self.grid_pos - dead_ends)
                #print(obs)
                if np.random.random() > epsilon:
                    # GET THE ACTION
                    motion = np.argmax(self.q_table[obs])
                else:
                    motion = np.random.randint(4)
                # Take the action!
                self.action(motion)
                #print(q_table)

    #

                if player_pos == DESTINATION_POS:
                    reward = DESTINATION_REWARD
                elif player_pos == DEAD_END_POS:
                    reward = -DEAD_END_PENALTY
                else:
                    reward = -MOVE_PENALTY

                sample3 = tuple(np.subtract(player_pos, DESTINATION_POS))
                sample4 = tuple(np.subtract(player_pos, DEAD_END_POS))
                new_obs = (tuple(int(i) for i in sample3), tuple(int(i) for i in sample4))
                #print(self.q_table[obs])
                max_future_q = np.max(self.q_table[new_obs])
                current_q = self.q_table[obs][motion]

                if reward == DESTINATION_REWARD:
                    new_q = DESTINATION_REWARD
                else:
                    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                self.q_table[obs][motion] = new_q
                print(self.q_table[obs])

                if show:
                    self.draw()
                    self.app.draw_grid()
                    #self.app.draw_text()
                    self.app.playing_draw()
    #

                if reward == DESTINATION_REWARD or reward == -DEAD_END_PENALTY:
                    if cv2.waitKey(500) & 0xFF == ord('q'):
                        break
                else:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    #
            episode_reward += reward
            if reward == DESTINATION_REWARD or reward == -DEAD_END_PENALTY:
                break
    #
        # print(episode_reward)
        episode_rewards.append(episode_reward)
        epsilon *= epsilon_decay

       

