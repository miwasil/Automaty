import pygame
import sys
from trafic_alg import *
import button
from tkinter.simpledialog import askinteger


def traffic_simulation(N, cell_size, density):
    pygame.init()

    matrix = make_road_matrix(N)
    spawners = SpawnersListObject()

    for i in range(N - 1):
        matrix[i, 10].neighbours.append(matrix[i + 1, 10])
    for i in range(N - 1):
        matrix[i + 1, 11].neighbours.append(matrix[i, 11])
    spawners.add_spawner(Spawner(matrix[0, 10], density))
    spawners.add_spawner(Spawner(matrix[N - 1, 11], density))

    for i in range(N - 1):
        matrix[11, i].neighbours.append(matrix[11, i + 1])
    for i in range(N - 1):
        matrix[10, i + 1].neighbours.append(matrix[10, i])
    spawners.add_spawner(Spawner(matrix[11, 0], density))
    spawners.add_spawner(Spawner(matrix[10, N - 1], density))

#druga droga
    for i in range(N - 1):
        matrix[i, 10+20].neighbours.append(matrix[i + 1, 10+20])
    for i in range(N - 1):
        matrix[i + 1, 11+20].neighbours.append(matrix[i, 11+20])
    spawners.add_spawner(Spawner(matrix[0, 10+20], density))
    spawners.add_spawner(Spawner(matrix[N - 1, 11+20], density))

    cars = []
    for i in spawners.list_of_spawners:
        print(i)

    crossroad1 = OmniPresentCrossroad()
    #all_signalization = SignalizationObjectList()


    crossroad1.add_entrance(matrix[6, 10])
    crossroad1.add_entrance(matrix[10, 15])
    crossroad1.add_entrance(matrix[15, 11])
    crossroad1.add_entrance(matrix[11, 6])
    crossroad1.add_light(OmniPresentCrossroad.Signalization(matrix[9, 10],cords=[9, 10], starting_state=False))
    crossroad1.add_light(OmniPresentCrossroad.Signalization(matrix[10, 12],cords=[10, 12], starting_state=True))
    crossroad1.add_light(OmniPresentCrossroad.Signalization(matrix[12, 11],cords=[12, 11], starting_state=False))
    crossroad1.add_light(OmniPresentCrossroad.Signalization(matrix[11, 9],cords=[11, 9], starting_state=True))

    crossroad1.add_exit(matrix[6, 11])
    crossroad1.add_exit(matrix[11, 15])
    crossroad1.add_exit(matrix[15, 10])
    crossroad1.add_exit(matrix[10, 6])

    crossroad1.create_paths()

    crossroad1.remove_path(matrix[6, 10], matrix[6, 11])
    crossroad1.remove_path(matrix[10, 15], matrix[11, 15])
    crossroad1.remove_path(matrix[15, 11], matrix[15, 10])
    crossroad1.remove_path(matrix[11, 6], matrix[10, 6])

    crossroad1.create_paths_and_vectors()
    crossroad1.create_entrance_object_list()
    crossroad1.create_my_roads()
    crossroad1.set_influence_area_for_lights_priority()
    crossroad1.create_unstuck(matrix)

    crossroad2 = OmniPresentCrossroad()
    crossroad2.add_entrance(matrix[6, 10+20])
    crossroad2.add_entrance(matrix[10, 15+20])
    crossroad2.add_entrance(matrix[15, 11+20])
    crossroad2.add_entrance(matrix[11, 6+20])
    crossroad2.add_exit(matrix[6, 11+20])
    crossroad2.add_exit(matrix[11, 15+20])
    crossroad2.add_exit(matrix[15, 10+20])
    crossroad2.add_exit(matrix[10, 6+20])

    crossroad2.create_paths()

    crossroad2.remove_path(matrix[6, 10+20], matrix[6, 11+20])
    crossroad2.remove_path(matrix[10, 15+20], matrix[11, 15+20])
    crossroad2.remove_path(matrix[15, 11+20], matrix[15, 10+20])
    crossroad2.remove_path(matrix[11, 6+20], matrix[10, 6+20])

    crossroad2.create_paths_and_vectors()
    crossroad2.create_entrance_object_list()
    crossroad2.create_my_roads()
    crossroad2.set_influence_area_for_lights_priority()
    crossroad2.create_unstuck(matrix)


    width, height = N * cell_size, N * cell_size
    window = pygame.display.set_mode((width + 400, height))
    pygame.display.set_caption("Road traffic simulator")

    black = (0, 0, 0)
    white = (200, 200, 200)
    grey = (50, 50, 50)
    yellow = (204, 204, 0)
    green = (204, 204, 255)
    red = (255, 0, 0)
    greenreal = (0, 255, 0)
    blue = (0, 0, 255)
    lightblue = (204, 219, 255)

    # Variable to track mouse state
    drawing = False

    continuos_sim = 0
    tick = 10
    press = 0

    draw_road = []

    for i in range(N):
        for j in range(N):
            if matrix[i, j].neighbours:
                if matrix[i, j] not in draw_road:
                    draw_road.append(matrix[i, j].cords)
                for neighbour in matrix[i, j].neighbours:
                    if neighbour not in draw_road:
                        draw_road.append(neighbour.cords)

    game_area = window.subsurface(pygame.Rect((0, 0, width, height)))

    simtype_img = pygame.image.load('texturepack/simtype_traffic.jpg').convert_alpha()
    clear_img = pygame.image.load('texturepack/clear_traffic.jpg').convert_alpha()
    menu_img = pygame.image.load('texturepack/menu.jpg').convert_alpha()
    density_img = pygame.image.load('texturepack/density_traffic.jpg').convert_alpha()

    button_width = 100
    button_height = 50
    button_margin = 10

    total_button_height = 4 * (button_height + button_margin)

    simulation_button = button.Button(width + button_margin, (height - total_button_height) // 2, simtype_img, 0.8)
    reset_button = button.Button(width + button_margin,
                                 (height - total_button_height) // 2 + (button_height + button_margin), clear_img, 0.8)
    density_button = button.Button(width + button_margin,
                                   (height - total_button_height) // 2 + 2 * (button_height + button_margin),
                                   density_img, 0.8)
    menu_button = button.Button(width + button_margin,
                                (height - total_button_height) // 2 + 3 * (button_height + button_margin), menu_img,
                                0.8)

    custom_font = pygame.font.Font("texturepack/RetroGaming.ttf", 19)

    clear_area_rect = pygame.Rect(width, 0, 400, height)
    pygame.draw.rect(window, lightblue, clear_area_rect)

    text_space = custom_font.render("Press SPACE to", True, black)
    text_space2 = custom_font.render("perform next step", True, black)

    text_space_rect = text_space.get_rect(
        topleft=(
            width + button_margin, button_margin * 2))

    text_space2_rect = text_space2.get_rect(
        topleft=(
            width + button_margin, button_margin * 4))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spawners.spawn_all(cars)
                crossroad1.give_orders()
                crossroad1.right_hand_rule()
                crossroad1.unstuck.unstuck()
                crossroad1.all_lights_cycle()
                crossroad2.give_orders()
                crossroad2.right_hand_rule()
                crossroad2.unstuck.unstuck()
                crossroad2.all_lights_cycle()
                cars = cars_go(cars)

            if simulation_button.draw(window) or (event.type == pygame.KEYDOWN and event.key == pygame.K_F10):
                continuos_sim = - continuos_sim + 1

            if reset_button.draw(window) or (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                for i in range(N):
                    for j in range(N):
                        matrix[i, j].has_car = 0
                # cars = new_alive_list(matrix, N)  # cos

            if menu_button.draw(window):
                return

            if density_button.draw(window):
                new_density = askinteger("Traffic denity (default: 3, min: 1, max: 50)",
                                         "Enter percentage of car frequency spawning:")
                pygame.quit()
                traffic_simulation(N, cell_size, new_density)

        if continuos_sim == 1:
            spawners.spawn_all(cars)
            crossroad1.give_orders()
            crossroad1.right_hand_rule()
            crossroad1.unstuck.unstuck()  # wolac przed swiatlami
            crossroad1.all_lights_cycle()
            crossroad2.give_orders()
            crossroad2.right_hand_rule()
            crossroad2.unstuck.unstuck()
            crossroad2.all_lights_cycle()
            cars = cars_go(cars)

        game_area.fill(green)

        for road_coords in draw_road:
            rect = pygame.Rect(road_coords[1] * cell_size, road_coords[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(window, grey, rect)

        for light_object in crossroad1.lights:
            if light_object.current_state == 1:
                rectl = pygame.Rect(light_object.cords[1] * cell_size, light_object.cords[0] * cell_size, cell_size, cell_size)
                pygame.draw.rect(window, greenreal, rectl)
            else:
                rectl = pygame.Rect(light_object.cords[1] * cell_size, light_object.cords[0] * cell_size, cell_size,
                                    cell_size)
                pygame.draw.rect(window, red, rectl)


        for i in range(N):
            for j in range(N):
                if matrix[i, j].has_car == 1:
                    # rect_outer = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    rect_inner = pygame.Rect(j * cell_size + 3, i * cell_size + 3, cell_size - 6, cell_size - 6)

                    # pygame.draw.rect(window, black, rect_outer)
                    pygame.draw.rect(window, white, rect_inner)

        window.blit(text_space, text_space_rect)
        window.blit(text_space2, text_space2_rect)
        # window.blit(text_input.get_surface(), (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        pygame.time.Clock().tick(tick)


# traffic_simulation(40, 20, 6)
