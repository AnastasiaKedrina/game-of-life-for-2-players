import pygame
from copy import deepcopy
import sys
from pygame.locals import (
    K_p,
    K_c,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)


pygame.init()
pygame.display.set_caption('Game of life')

cell_size = 30 # размер ячеек
W, H = 30, 20 # количество ячеек
field_width, field_height = W*cell_size, H*cell_size
resolution = field_width, field_height+110

def print_field(field):
    # для вывода в консоль
    for i in field:
        print(i)

def change_life_cell(current_field, x, y):
    # логика игры
    first_count, second_count = 0, 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j][i]==1:
                first_count += 1
            if current_field[j][i]==2:
                second_count += 1

    if current_field[y][x]==1:
        first_count -= 1
        if first_count == 2 or first_count == 3:
            return 1
        # return 0
    else:
        if first_count == 3:
            return 1
        # return 0

    if current_field[y][x]==2:
        second_count -= 1
        if second_count == 2 or second_count == 3:
            return 2
        return 0
    else:
        if second_count == 3:
            return 2
        return 0


# пустые поля
next_field = [[0 for i in range(W)] for j in range(H)]
current_field = [[0 for i in range(W)] for j in range(H)]

# координаты клеток для прорисовки
positions=[]
for i in range(H):
    a=[]
    for j in range(W):
        a.append([j*cell_size, i*cell_size])
    positions.append(a)
# print(positions)


black = pygame.Color('black')
white = pygame.Color('white')
bg_color = pygame.Color('#C4DBE2')
line_color = white
border_color = white

# словари игроков
first_player = {'num':1,
                'color':pygame.Color('#A945C7'),
                'hover_color':pygame.Color('#C491D3')}
second_player = {'num':2,
                'color':pygame.Color('#5B97D5'),
                'hover_color':pygame.Color('#9EC4EA')}

cursor_cell = (-cell_size, -cell_size) 
one_round_steps = 30 # количество шагов за один запуск
all_steps = 1 # счетчик шагов
current_player = first_player # текущий игрок
one_round_cells = 20 # количество клеток на игрока за один ход
current_player_cells = 0 # счетчик клеток за ход
speed = 8


# текст
big_font=pygame.font.SysFont('Helvetica', 45, bold=True)
mid_font=pygame.font.SysFont('Helvetica', 25, bold=True)
small_font=pygame.font.SysFont('Helvetica', 15, bold=True)

text_title = big_font.render('Игра Жизнь', 1, white)
text_first_player = mid_font.render('Ход первого игрока', 1, first_player['color'])
text_second_player = mid_font.render('Ход второго игрока', 1, second_player['color'])
text_next_player = mid_font.render(f'Передать ход', 1, black)
text_start = mid_font.render('Начать симуляцию', 1, black)
text_stop = mid_font.render('Симуляция запущена', 1, black)
text_steps = small_font.render(f'Шагов на один раунд: {one_round_steps}', 1, white)
text_check_win = mid_font.render('Кто побеждает?', 1, white)
text_first_win = mid_font.render('Первый игрок!', 1, first_player['color'])
text_second_win = mid_font.render('Второй игрок!', 1, second_player['color'])
text_no_win = mid_font.render('Ничья!', 1, black)


life = False
surface = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            # нажатия на клавиатуру
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_p:
                # "p" чтобы запустить симуляцию
                life=True
            if event.key == K_c:
                # "c" чтобы передать ход второму игроку
                if not(life):
                    current_player=second_player
                    current_player_cells=0

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    cursor = pygame.mouse.get_pos()
    surface.fill(bg_color)
    
    # текст
    surface.blit(text_title, (25, 570))
    text_all_steps = small_font.render(f'Всего шагов: {all_steps-1}', 1, white)
    text_cells = mid_font.render(f'Осталось ячеек: {one_round_cells-current_player_cells}', 1, current_player['color'])
    surface.blit(text_all_steps, (325, 585))
    surface.blit(text_steps, (325, 605))

    # текст текущего игрока
    if not(life):
        surface.blit(text_cells, (325, 620))
        if current_player['num']==1:
            surface.blit(text_first_player, (25, 620))
            pygame.draw.rect(surface, first_player['hover_color'], pygame.Rect(20, 660, 220, 35))
            surface.blit(text_next_player, (25, 660))
        else:
            surface.blit(text_second_player, (25, 620))
        
    # текст запуск симуляции
    x, y = 300, 615
    pygame.draw.rect(surface, first_player['hover_color'], pygame.Rect(x, 660, 320, 35))
    if not life:
        surface.blit(text_start, (40+x, 660))
        pygame.draw.polygon(surface, black, [[15+x, 50+y], [30+x, 60+y], [15+x, 70+y]])
    else:
        surface.blit(text_stop, (40+x, 660))
        pygame.draw.rect(surface, black, (15+x, 50+y, 5, 20))
        pygame.draw.rect(surface, black, (25+x, 50+y, 5, 20))

    # начать симулияцию - нажатие
    if cursor[0] > 250 and cursor[0] < 560:
        if cursor[1] > 650 and cursor[1] < 700:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0]:
                life = True

    # передать ход
    if cursor[0] > 25 and cursor[0] < 210:
        if cursor[1] > 650 and cursor[1] < 700:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0]:
                current_player_cells=0
                current_player = second_player

    
    # проверить победителя    
    first_cells = sum([i.count(1) for i in current_field])
    second_cells = sum([i.count(2) for i in current_field])
    text_first_cells = small_font.render(f'Первый игрок: {first_cells}', 1, white)  
    text_second_cells = small_font.render(f'Второй игрок: {second_cells}', 1, white)        
    pygame.draw.rect(surface, second_player['hover_color'], pygame.Rect(630, 585, 240, 45))
    surface.blit(text_check_win, (645, 590))
    if cursor[0] > 630 and cursor[0] < 630+240:
        if cursor[1] > 585 and cursor[1] < 585+45:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if first_cells>second_cells:
                surface.blit(text_first_win, (645, 635))
            elif first_cells<second_cells:
                surface.blit(text_second_win, (645, 635))
            elif first_cells==second_cells:
                surface.blit(text_no_win, (645, 635))
            surface.blit(text_first_cells, (645, 665))
            surface.blit(text_second_cells, (645, 680))

    
    # отрисовка игрового поля и процесса игры
    border = 4
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            if current_field[y][x]==1:
                # клетки первого игрока
                pygame.draw.rect(surface, first_player['hover_color'], (x * cell_size , y * cell_size, 
                                                    cell_size, cell_size))
                pygame.draw.rect(surface, first_player['color'], (x * cell_size + border, y * cell_size + border, 
                                                    cell_size - border*2, cell_size - border*2))
            if current_field[y][x]==2:
                # клетки второго игрока
                pygame.draw.rect(surface, second_player['hover_color'], (x * cell_size , y * cell_size, 
                                                    cell_size, cell_size))
                pygame.draw.rect(surface, second_player['color'], (x * cell_size + border, y * cell_size + border, 
                                                    cell_size - border*2, cell_size - border*2))
            if life: 
                # отрисовка запущенной игры
                next_field[y][x] = change_life_cell(current_field, x, y)
    if life:
        current_field = deepcopy(next_field)

    # нажатие на поле
    for row in positions:
        for pos in row:
            if cursor[0] > pos[0] and cursor[0] < pos[0]+cell_size:
                if cursor[1] > pos[1] and cursor[1] < pos[1]+cell_size:
                    if (pos[0]!=0 and pos[1]!=0) and (pos[0]!=field_width-cell_size and pos[1]!=field_height-cell_size):
                        if not(life):
                            cursor_cell = pos # меняются коориднаты клетки, на котороую наведен курсор
                            x, y = pos[1]/cell_size, pos[0]/cell_size
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            if pygame.mouse.get_pressed()[0]: # нажатие на левую кнопку мыши - добавить клетку
                                if one_round_cells>current_player_cells: 
                                    # если на ход не кончилось число клеток
                                    if current_field[int(x)][int(y)]==0:
                                        current_field[int(x)][int(y)]=current_player['num'] # в массив поля добавляется клетка
                                        current_player_cells+=1
                            
                            if pygame.mouse.get_pressed()[2]: # нажатие на правую кнопку мыши - стереть клетку
                                if current_field[int(x)][int(y)]==current_player['num']:
                                    current_field[int(x)][int(y)]=0
                                    current_player_cells-=1



    if not(life):
        # наведение курсора на клетки
        pygame.draw.rect(surface, current_player['hover_color'], pygame.Rect(*cursor_cell, cell_size, cell_size))

    if all_steps%one_round_steps==0 and all_steps!=0:
        # прерывание симуляции после заданного числа шагов
        life = False
        all_steps+=1
    
    # отрисовка линий поля
    [pygame.draw.line(surface, line_color, (x, cell_size), (x, field_height-cell_size)) for x in range(0, field_width, cell_size)]
    [pygame.draw.line(surface, line_color, (cell_size, y), (field_width-cell_size, y)) for y in range(0, field_height, cell_size)]
    
    if life:
        fps=speed
        all_steps+=1
        current_player_cells=0
        current_player=first_player
    else:
        fps = 30
    pygame.display.flip()
    clock.tick(fps)
