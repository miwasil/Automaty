from tkinter.simpledialog import askinteger

import pygame
import sys
import numpy
from game_of_life_alg import omnipresent_perception, next_matrix, ar_insert
from photo_refactor import black_and_white
import button
import tkinter as tk
from tkinter import filedialog

def game_of_life_simulation(N, cell_size, scale_width, scale_height):

    pygame.init()

    width, height = N * cell_size, N * cell_size
    button_window_width = width * 0.4
    window = pygame.display.set_mode((width + button_window_width, height))
    pygame.display.set_caption("Game Of Life")

    black = (0, 0, 0)
    white = (200, 200, 200)
    grey = (169, 169, 169)
    red = (255, 0, 0)

    game_area = window.subsurface(pygame.Rect((0, 0, width, height)))

    initial_board = black_and_white("3.jpg", N)

    simtype_img = pygame.image.load('texturepack/simtype_life.jpg').convert_alpha()
    resize_img = pygame.image.load('texturepack/resize_life.jpg').convert_alpha()
    plus_img = pygame.image.load('texturepack/plus_life.jpg').convert_alpha()
    minus_img = pygame.image.load('texturepack/minus_life.jpg').convert_alpha()
    picture_img = pygame.image.load('texturepack/picture_life.jpg').convert_alpha()
    clear_img = pygame.image.load('texturepack/clear_life.jpg').convert_alpha()
    menu_img = pygame.image.load('texturepack/menu.jpg').convert_alpha()

    button_width = 100 * scale_width
    button_height = 50 * scale_height
    button_margin = 20 * scale_height

    total_button_height = 8 * (button_height + button_margin)
    button_scale = 0.8 * (scale_height + scale_width)/2

    simulation_button = button.Button(width + button_margin, (height - total_button_height) // 2, simtype_img, button_scale)
    minus_button = button.Button(width + button_margin, (height - total_button_height) // 2 + (button_height + button_margin), minus_img, button_scale)
    plus_button = button.Button(width + button_margin, (height - total_button_height) // 2 + 2 * (button_height + button_margin), plus_img, button_scale)
    reset_button = button.Button(width + button_margin, (height - total_button_height) // 2 + 3 * (button_height + button_margin), clear_img, button_scale)
    resize_button = button.Button(width + button_margin, (height - total_button_height) // 2 + 4 * (button_height + button_margin), resize_img, button_scale)
    picture_button = button.Button(width + button_margin, (height - total_button_height) // 2 + 5 * (button_height + button_margin), picture_img, button_scale)
    menu_button = button.Button(width + button_margin,
                                (height - total_button_height) // 2 + 6 * (button_height + button_margin), menu_img,
                                button_scale)

    font_size = int(25 * (scale_height + scale_width)/2)
    custom_font = pygame.font.Font("texturepack/RetroGaming.ttf", font_size)

    matrix = initial_board
    data = omnipresent_perception()
    dead_or_alive = data[0]
    arr = data[1]

    drawing = False

    continuos_sim = 0
    tick = 40

    live_cells_count = numpy.sum(matrix)

    generation_count = 0
    clear_area_rect = pygame.Rect(width, 0, 400, height)
    pygame.draw.rect(window, white, clear_area_rect)

    text_space = custom_font.render("Press SPACE to", True, black)
    text_space2 = custom_font.render("perform next step", True, black)

    text_space_rect = text_space.get_rect(
        topleft=(
        width + button_margin, button_margin*2))

    text_space2_rect = text_space2.get_rect(
        topleft=(
            width + button_margin, button_margin * 4))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if 0 < x < width and height > y > 0:
                        drawing = True
                        x, y = event.pos
                        col = x // cell_size % N
                        row = y // cell_size % N
                        matrix[row, col] = 1

            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = event.pos
                if 0 < x < width and height > y > 0:
                    col = x // cell_size % N
                    row = y // cell_size % N
                    matrix[row, col] = 1

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False



            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                matrix = next_matrix(matrix, N, dead_or_alive, arr)
                generation_count += 1

            if reset_button.draw(window) or (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                matrix[:,:] = 0
                generation_count = 0

            if minus_button.draw(window) or (event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS):
                if tick > 6:
                    tick = tick - 5
                print(tick)

            if plus_button.draw(window) or (event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS):
                if tick < 75:
                    tick = tick + 5
                print(tick)

            if simulation_button.draw(window) or (event.type == pygame.KEYDOWN and event.key == pygame.K_F10):
                continuos_sim = -continuos_sim + 1

            if resize_button.draw(window):
                new_cell_size = askinteger("Resize", "Enter new cell size:")
                new_N = askinteger("Resize", "Enter new number of cells:")
                original_width, original_height = 1000, 1000
                new_width, new_height = new_N * new_cell_size, new_N * new_cell_size
                scale_width = new_width / original_width
                scale_height = new_height / original_height
                pygame.quit()
                game_of_life_simulation(new_N, new_cell_size, scale_width, scale_height)

            if menu_button.draw(window):
                return

            if picture_button.draw(window):
                generation_count = 0
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Choose a photo",
                                                       filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
                if file_path:
                    initial_board = black_and_white(file_path, N)
                    matrix = initial_board


        if continuos_sim == 1:
            matrix = next_matrix(matrix, N, dead_or_alive, arr)
            generation_count += 1

        game_area.fill(white)

        live_cells_count = 0

        for i in range(N):
            for j in range(N):
                if matrix[i, j] == 1:
                    rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(window, black, rect)
                    live_cells_count = live_cells_count + 1

        for i in range(N + 1):
            pygame.draw.line(window, grey, (i * cell_size, 0), (i * cell_size, height), 1)
            pygame.draw.line(window, grey, (0, i * cell_size), (width, i * cell_size), 1)

        text_area_rect = pygame.Rect(width + button_margin, (height - total_button_height) // 2 + total_button_height,
                                     400 - 2 * button_margin,
                                     height - (height - total_button_height) // 2 - total_button_height)
        pygame.draw.rect(window, white, text_area_rect)

        # Move writings just beyond the buttons
        text_cells = custom_font.render(f'Live cells: {live_cells_count}', True, black)
        text_generation = custom_font.render(f'Generation: {generation_count}', True, black)

        # Adjust positions based on button placement
        text_cells_rect = text_cells.get_rect(
            topleft=(width + button_margin, (height - total_button_height) // 2 + total_button_height))
        text_generation_rect = text_generation.get_rect(
            topleft=(width + button_margin, (height - total_button_height) // 2 + total_button_height + button_height + button_margin))

        window.blit(text_space, text_space_rect)
        window.blit(text_space2, text_space2_rect)

        window.blit(text_cells, text_cells_rect)
        window.blit(text_generation, text_generation_rect)

        pygame.display.flip()

        pygame.time.Clock().tick(tick)

#game_of_life_simulation(100, 10,1,1)