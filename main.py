
import pygame as pg
import random as rnd
import copy
import time
from dataclasses import dataclass

# tetromino cho cac chu cai
tetrominos = [
                [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # o
                [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # I
                [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0],  # J
                [0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # L
                [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # s
                [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # z
                [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0],  # T
             ]

@dataclass
class tetromino():
    tetro : list
    row : int=0
    column : int =3

    def show(self, te_surf):
        for n, colort in enumerate(self.tetro):
            if colort>0:
                x= (self.column+n%4) * sq_size
                y= (self.row+n//4) * sq_size
                te_surf.blit(te_img[colort],(x,y))

    def show_next(self):
        for n, colort in enumerate(self.tetro):
            if colort>0:
                x = x_show + (n % 4) * sq_size
                y = y_show + (n // 4) * sq_size
                screen.blit(te_img[colort], (x, y))

    def check(self,r,c):
        for n,colort in enumerate(self.tetro):
            if colort>0:
                rs=r+n//4
                cs=c+n%4
                if cs<0 or rs >=rows or cs>=columns or grid[rs *columns+cs]>0:
                    return False
        return True

    def update(self, r, c):
        if self.check(self.row+r,self.column+c):
            self.row += r
            self.column += c
            return True
        return False

    def rotate(self):
        savetetro = self.tetro.copy()
        for n,colort in enumerate(savetetro):
            self.tetro[(2-(n%4))*4+(n//4)]=colort
        if self.check(self.row,self.column)==False:
            self.tetro=savetetro.copy()

##################


def object_on_grid_line(character):
    for n , colort in enumerate(character.tetro):
        if colort>0:
            grid[(character.row+n//4)*columns+(character.column+n%4)]=colort


def delete_all_filled_row():
    deleted_rows = 0
    for row in range(rows):
        for column in range(columns):
            if grid[row*columns+column]==0:
                break
        else:
            del grid[row*columns :row*columns+columns]
            grid[0:0] = [0]*columns
            deleted_rows +=1
    return int(100*deleted_rows*(deleted_rows+1)/2)


def end_game():
    for column in range(columns,columns*2):
        if grid[column]!=0:
            return True
    return False


def create_button(btn_string):
    btn_text = btn_string
    for i in range(len(btn_text)):
        btn_text[i] = btn_text_font.render(btn_string[i], False, (255, 143, 143))

    # draw button
    for i in range(len(btn_text)):
        screen.blit(btn1_img[0], (btn_left, btn_top[i]))
        screen.blit(btn_text[i], (btn_left + ui_size * 0.3, btn_top[i] + ui_size * 0.2))
    return btn_text


def check_button(button_function):
    mouse_pos = pg.mouse.get_pos()
    if btn_left < mouse_pos[0] < btn_right:
        for i in range(len(button_function)):
            if btn_top[i] < mouse_pos[1] < btn_bot[i]:
                return button_function[i]
    return 0



def button_effect(btn_text):
    mouse_pos = pg.mouse.get_pos()
    if btn_left < mouse_pos[0] < btn_right:
        for i in range(len(btn_text)):
            if btn_top[i] < mouse_pos[1] < btn_bot[i]:
                screen.blit(btn1_img[1], (btn_left, btn_top[i]))
            else:
                screen.blit(btn1_img[0], (btn_left, btn_top[i]))
            screen.blit(btn_text[i], (btn_left + ui_size * 0.3, btn_top[i] + ui_size * 0.2))
    else:
        for i in range(len(btn_text)):
            screen.blit(btn1_img[0], (btn_left, btn_top[i]))
            screen.blit(btn_text[i], (btn_left + ui_size * 0.3, btn_top[i] + ui_size * 0.2))


def pause_button_effect(pausebtn_pos):
    mouse_pos = pg.mouse.get_pos()
    if pausebtn_pos[0] < mouse_pos[0] < pausebtn_pos[2]:
        if pausebtn_pos[1] < mouse_pos[1] < pausebtn_pos[3]:
            screen.blit(btn2_img[1], (430, 380))
        else: screen.blit(btn2_img[0], (430, 380))
    else: screen.blit(btn2_img[0], (430, 380))


##########################


def set_btn_pos(top, num):
    for i in range(num):
        btn_top[i] = int(ui_size * (top + i * 1.5))
        btn_bot[i] = int(ui_size * (top + i * 1.5 + 1))


########################## Scenes ##########################


def game_over_ui(current_score, difficulty):
    for i in range(10):
        if current_score > int(high_score_data[difficulty][i*2+1]):
            r = game_over_ui1()
            if r == 0:
                return "Main menu"
            else:
                for j in range(9, i, -1):  # --------------------------- ADD NEW HIGH SCORE -----------------------------
                    high_score_data[difficulty][j*2] = high_score_data[difficulty][(j-1)*2]
                    high_score_data[difficulty][j*2+1] = high_score_data[difficulty][(j-1)*2+1]
                high_score_data[difficulty][i*2] = r
                high_score_data[difficulty][i*2+1] = str(current_score)
                f = open(f"Data/{difficulty}.hscr", "w")
                for rec in high_score_data[difficulty]:
                    f.write(rec+"\n")
                f.close()
                print("Save high score complete")
                return "Main menu"
    return game_over_ui2(current_score)


def game_over_ui1():
    set_btn_pos(5.5, 2)
    screen.blit(board2_img, ((screen_width - board2_size[0]) // 2, ui_size * 0.33))
    text = pg.font.SysFont('Comic Sans MS', int(ui_size / 1.5)).render("GAME OVER", False, (0, 0, 160))
    screen.blit(text, (screen_width / 2 - ui_size * 2, ui_size * 0.7))
    text = pg.font.SysFont('Comic Sans MS', int(ui_size / 2)).render("New high score!", False, (0, 125, 255))
    screen.blit(text, (screen_width / 2 - ui_size * 1.8, ui_size * 2.1))
    text = font1.render("Enter your name:", False, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - ui_size * 2.5, ui_size * 3.4))
    screen.blit(textbar_img, ((screen_width - textbar_size[0]) // 2, ui_size * 3.9))
    # button
    btn_text = create_button(['     OK     ', 'Main menu'])
    s = ''

    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.KEYDOWN:  # Typing from keyboard
                k = ev.key
                if len(s) < 16:
                    if pg.K_a <= k <= pg.K_z or pg.K_0 <= k <= pg.K_9 or k == pg.K_PERIOD or k == pg.K_MINUS:
                        s += pg.key.name(k).upper()
                if k == pg.K_BACKSPACE:
                    s = s[:-1]
                screen.blit(textbar_img, ((screen_width - textbar_size[0]) // 2, ui_size * 3.9))
                screen.blit(type_font.render(s, False, (0, 0, 0)), (screen_width / 2 - ui_size * 2.42, ui_size * 4.1))
            if ev.type == pg.MOUSEBUTTONDOWN:
                r = check_button([1, 2])
                if r == 1:
                    return s
                if r == 2:
                    return 0
            if ev.type == pg.QUIT:
                pg.quit()
                exit()
        pg.display.flip()


def game_over_ui2(current_score):
    set_btn_pos(5, 2)
    screen.blit(board2_img, ((screen_width - board2_size[0]) // 2, ui_size * 0.33))
    text = pg.font.SysFont('Comic Sans MS', int(ui_size / 1.5)).render("GAME OVER", False, (0, 0, 160))
    screen.blit(text, (screen_width / 2 - ui_size * 2, ui_size * 0.8))
    text = pg.font.SysFont('Comic Sans MS', int(ui_size / 2)).render("Score: "+str(current_score), False, (0, 125, 255))
    screen.blit(text, (screen_width / 2 - ui_size * 1.4, ui_size * 2.8))
    # button
    btn_text = create_button(['Play again', 'Main menu'])

    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.MOUSEBUTTONDOWN:
                r = check_button([1, 2])
                if r == 1:
                    return "New game"
                if r == 2:
                    return "Main menu"
            if ev.type == pg.QUIT:
                return "Exit game"
        pg.display.flip()

def select_difficulty():
    set_btn_pos(3.2, 3)
    screen.blit(board2_img, ((screen_width - board2_size[0]) // 2, ui_size * 0.33))
    text = pg.font.SysFont('Comic Sans MS', int(ui_size / 1.9)).render("SELECT DIFFICULTY", False, (0, 0, 160))
    screen.blit(text, (screen_width/2-ui_size*2.7, ui_size * 1))
    btn_text = create_button(['    Easy    ', '   Normal   ', '    Hard    '])

    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.MOUSEBUTTONDOWN:
                d = check_button([1, 2, 3])
                if 1 <= d <= 3:
                    return d-1
            if ev.type == pg.QUIT:
                pg.quit()
                exit()
        pg.display.flip()


def load_game():
    set_btn_pos(5.5, 2)
    screen.blit(board2_img, ((screen_width-board2_size[0])//2, ui_size*0.33))
    text = big_font.render("LOAD GAME", False, (0, 0, 160))
    screen.blit(text, (screen_width/2-ui_size*2, ui_size * 0.8))
    text = font1.render("Enter file name:", False, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - ui_size * 2.5, ui_size * 2.7))
    screen.blit(textbar_img, ((screen_width - textbar_size[0]) // 2, ui_size * 3.2))
    error_text = font1.render("*Can't read file!", False, (255, 0, 0))
    # button
    btn_text = create_button(['Load game', 'Main menu'])
    s = ''
    dat = []
    err = False

    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.KEYDOWN:
                k = ev.key
                if len(s) < 16:
                    if pg.K_a <= k <= pg.K_z or pg.K_0 <= k <= pg.K_9 or k == pg.K_PERIOD or k == pg.K_MINUS:
                        s += pg.key.name(k).upper()
                if k == pg.K_BACKSPACE:
                    s = s[:-1]
                screen.blit(textbar_img, ((screen_width - textbar_size[0]) // 2, ui_size * 3.2))
                screen.blit(type_font.render(s, False, (0, 0, 0)), (screen_width / 2 - ui_size * 2.42, ui_size * 3.4))
            if ev.type == pg.MOUSEBUTTONDOWN:
                r = check_button([1,2])
                if r == 1:
                    try:
                        f = open(f"Data/{s}.dat", "r")
                    except FileNotFoundError:
                        err = True
                        break
                    dat = f.readlines()  # ----------------------------- LOAD GAME -------------------------------------
                    if len(dat) != 8:
                        err = True
                        f.close()
                        break
                    for i in (1,2,4,5,6):
                        dat[i] = int(dat[i][:-1])
                    dat[7] += "."
                    for i in (0,3,7):
                        dat[i] = list(dat[i][:-1])
                        for j in range(len(dat[i])):
                            dat[i][j] = int(dat[i][j])
                    f.close()
                    return dat
                if r == 2:
                    return 0
            if ev.type == pg.QUIT:
                pg.quit()
                exit()
        if err:
            screen.blit(error_text, (screen_width / 2 - ui_size * 2.5, ui_size * 4.1))
        pg.display.flip()


def save_game():
    set_btn_pos(5.5, 2)
    screen.blit(board2_img, ((screen_width-board2_size[0])//2, ui_size*0.33))
    text = pg.font.SysFont('Comic Sans MS', int(ui_size / 1.5)).render("SAVE GAME", False, (0, 0, 160))
    screen.blit(text,(screen_width/2-ui_size*2, ui_size * 0.8))
    text = font1.render("Enter file name:", False, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - ui_size * 2.5, ui_size * 2.7))
    screen.blit(textbar_img, ((screen_width - textbar_size[0]) // 2, ui_size * 3.2))
    # button
    btn_text = create_button(['Save game', '    Back    '])
    s = ''

    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.KEYDOWN:
                k = ev.key
                if len(s) < 16:
                    if pg.K_a <= k <= pg.K_z or pg.K_0 <= k <= pg.K_9 or k == pg.K_PERIOD or k == pg.K_MINUS:
                        s += pg.key.name(k).upper()
                if k == pg.K_BACKSPACE:
                    s = s[:-1]
                screen.blit(textbar_img, ((screen_width - textbar_size[0]) // 2, ui_size * 3.2))
                screen.blit(type_font.render(s, False, (0, 0, 0)), (screen_width / 2 - ui_size * 2.42, ui_size * 3.4))
            if ev.type == pg.MOUSEBUTTONDOWN:
                r = check_button([1, 2])
                if r == 1:
                    return s
                if r == 2:
                    return 0
            if ev.type == pg.QUIT:
                return "Exit game"
        pg.display.flip()


def high_score_ui(difficulty):  # 0 = easy, 1 = normal, 2 = hard
    set_btn_pos(7.2, 1)
    x_column1 = screen_width / 2 - ui_size * 0.9
    x_column2 = screen_width / 2 + ui_size * 1.9
    screen.blit(board2_img, ((screen_width - board2_size[0]) // 2, ui_size*0.33))
    myfont2 = pg.font.SysFont('Consolas', int (ui_size / 3))
    highscore_text = big_font.render("HIGH SCORE", False, (0, 0, 160))
    screen.blit(highscore_text, (screen_width / 2 - ui_size * 2.2, ui_size * 0.8))
    name_text = font1.render("Name", False, (0, 125, 255))
    screen.blit(name_text, (x_column1 - ui_size * 0.4 , ui_size * 2.1))
    score_text = font1.render("Score", False, (0, 125, 255))
    screen.blit(score_text, (x_column2 - ui_size * 0.5, ui_size * 2.1))

    #line & button
    pg.draw.line(screen, (0, 0, 0), (screen_width/2-ui_size*2.6, ui_size*2.6),
                                    (screen_width/2+ui_size*2.6, ui_size*2.6), 3)
    pg.draw.line(screen, (0, 0, 0), (screen_width/2+ui_size*1, ui_size*2.1),
                                    (screen_width/2+ui_size*1, ui_size*6.7), 3)
    btn_text = create_button(['    Back    '])

    name, high_score = [], []

    for i in range(len(high_score_data[difficulty])//2):
        name.append(high_score_data[difficulty][i*2])
        high_score.append(high_score_data[difficulty][i*2+1])

    for i in range(len(name)):
        screen.blit(myfont2.render(name[i], False, (0, 0, 0)),
                                                (x_column1 - ui_size*0.09*len(name[i]), ui_size * (2.75 + i*0.4)))
        screen.blit(myfont2.render(high_score[i], False, (0, 0, 0)),
                                                (x_column2 - ui_size*0.1*len(high_score[i]), ui_size * (2.75 + i*0.4)))

    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                return "Exit game"
            if ev.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if btn_left < mouse_pos[0] < btn_right:
                    if btn_top[0] < mouse_pos[1] < btn_bot[0]:
                        return "Main menu"
        pg.display.flip()


def main_menu():
    gamename_text = pg.font.SysFont('Comic Sans MS', int(ui_size)).render('Tetris', False, (255, 50, 50))
    set_btn_pos(2.5, 4)
    # button
    btn_text = create_button(['New game', 'Load game', 'High score', '    Exit   '])

    # game name
    screen.blit(gamename_text, (screen_width // 2 - int(ui_size * 1.5), int(ui_size * 0.5)))
    while True:
        button_effect(btn_text)
        for ev in pg.event.get():
            if ev.type == pg.MOUSEBUTTONDOWN:
                r = check_button(["New game", "Load game", "High score", "Exit game"])
                if r != 0:
                    return r
            if ev.type == pg.QUIT:
                return "Exit game"
        pg.display.flip()

def game_ui_init():
    set_btn_pos(2.5, 3)
    screen.blit(border, (10, 10))
    # text
    myfont = pg.font.SysFont('Comic Sans MS', 35)
    myfont3 = pg.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Next', False, (0, 255, 255))
    textsurface3 = myfont3.render('Score: ', False, (0, 255, 255))
    screen.blit(textsurface, (x_show + 20, y_show - 60))  # "Next"
    pg.draw.rect(screen, (0, 255, 0), (x_show - 10, y_show - 10, sq_size * 4 + 20, sq_size * 4 + 20), 2)
    screen.blit(textsurface3, (405, 250))  # "Score"
    screen.blit(btn2_img[0], (430, 380))  # Pause button


def game(character, next_show, speed, score, grid, difficulty):
    te_surf = screen.subsurface((40, 40, sq_size * columns, sq_size * rows))

    myfont3 = pg.font.SysFont('Comic Sans MS', 30)
    #textsurface5 = myfont3.render('End game', False, (0, 255, 255))

    # button
    pausebtn_pos = [430,380,530,480]
    btn_text = create_button([' Continue ', 'Save game', 'Main menu'])
    screen.fill((0, 0, 0))

    # tao su kien thoi gian roi
    tetromino_dowm = pg.USEREVENT + 1
    # speedup = pg.USEREVENT +2
    pg.time.set_timer(tetromino_dowm, speed)
    # pg.time.set_timer(speedup,500)
    # pg.key.set_repeat(1,100)##...............
    ##
    # pg.key.set_repeat(0, 1000)
    game_ui_init()

    while True:
        kt = end_game()
        pause_button_effect(pausebtn_pos)
        pg.time.delay(80)
        textsurface4 = myfont3.render(f'{score}', False, (0, 255, 255))

        if kt == False:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    return "Exit game"
                if ev.type == tetromino_dowm:
                    if not character.update(1, 0):  # new tetromino
                        pg.time.set_timer(tetromino_dowm, 0)  # stop temporarily
                        speed = int(speed * 0.99+0.3)  # => min speed = 30
                        print(speed)
                        object_on_grid_line(character)
                        character = next_show
                        next = rnd.choice(tetrominos)
                        next_show = copy.deepcopy(tetromino(next))
                        score += delete_all_filled_row()
                        pg.time.delay(200)
                        pg.time.set_timer(tetromino_dowm, speed)

                # if even.type == speedup:
                #
                #     # if score % 500==0 and score != 0:
                #         speed=int(speed*0.7)
                #         pg.time.set_timer(tetromino_dowm,speed)
                #         lever+=1
                if ev.type == pg.KEYDOWN:
                    # pg.key.set_repeat(1, 100)
                    if ev.key == pg.K_LEFT:
                        character.update(0, -1)
                    if ev.key == pg.K_RIGHT:
                        character.update(0, 1)
                    # if even.key == pg.K_DOWN:
                    #     character.update(1,0)
                    if ev.key == pg.K_SPACE:
                        # pg.key.set_repeat(1, 0)
                        character.rotate()
                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if pausebtn_pos[0] < mouse_pos[0] < pausebtn_pos[2]:  # ######### Pause game
                        if pausebtn_pos[1] < mouse_pos[1] < pausebtn_pos[3]:
                            screen.blit(board_img, ((screen_width-board_size[0])//2, ui_size*1.73))
                            end = False
                            while not end:
                                button_effect(btn_text)
                                for ev in pg.event.get():
                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                        i = check_button([1,2,3])
                                        if i == 1:
                                            screen.fill((0, 0, 0))
                                            game_ui_init()
                                            end = True
                                        if i == 2:
                                            s = save_game()  # ---------------------- SAVE GAME ------------------------
                                            if s:
                                                f = open(f"Data/{s}.dat", "w")
                                                for t in character.tetro:
                                                    f.write(str(t))
                                                f.write(f"\n{character.row}")
                                                f.write(f"\n{character.column}\n")
                                                for t in next_show.tetro:
                                                    f.write(str(t))
                                                f.write(f"\n{speed}")
                                                f.write(f"\n{score}")
                                                f.write(f"\n{difficulty}\n")
                                                for i in range(columns*rows):
                                                    f.write(str(grid[i]))
                                                f.close()
                                                print("Save complete!")
                                                return "Main menu"
                                            else:
                                                screen.fill((0, 0, 0))
                                                game_ui_init()
                                                end = True
                                        if i == 3:
                                            return "Main menu"
                                    if ev.type == pg.QUIT:
                                        return "Exit game"
                                pg.display.flip()

            keys = pg.key.get_pressed()
            # if keys[pg.K_LEFT]:
            #     character.update(0, -1)
            # if keys[pg.K_RIGHT]:
            #     character.update(0, 1)
            if keys[pg.K_DOWN]:
                character.update(1, 0)
            # if keys[pg.K_SPACE]:
            #     # pg.key.set_repeat(1, 0)
            #     character.rotate()

            # screen.blit(image_me, (350, 350))

        # visual
        te_surf.fill((0, 0, 0))
        pg.draw.rect(screen, (0, 0, 0), (x_show, y_show, sq_size * 4, sq_size * 4))
        character.show(te_surf)
        next_show.show_next()
        pg.draw.rect(screen, (0, 0, 0), (500, 250, 100, 35))  # clear
        screen.blit(textsurface4, (500, 250))  # diem hien tai
        for n, color in enumerate(grid):
            if color > 0:
                x = n % columns * sq_size  ## toa do x y dau
                y = n // columns * sq_size
                te_surf.blit(te_img[color], (x, y))

        if kt == True:  # end game
            pg.time.delay(500)
            return game_over_ui(score, difficulty)
            #
            #
            #
            #
            #
        pg.display.flip()

##########################

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pg.init()

    screen_width, screen_height = 600, 680
    ui_size = 75  # 40~80
    columns, rows = 10, 20
    sq_size = 30  # kich thuoc 1 o gach
    grid = [0]*columns*rows
    speed, score = 300, 0
    y_show: int = 75
    x_show: int = 425

    # button
    btn_left = int(screen_width // 2 - ui_size * 1.25)
    btn_right = int(screen_width // 2 + ui_size * 1.25)
    btn_top, btn_bot = [''] * 4, [''] * 4
    for i in range(4):
        btn_top[i] = int(ui_size * (2.5 + i * 1.5))
        btn_bot[i] = int(ui_size * (3.5 + i * 1.5))
    btn_text_font = pg.font.SysFont('Comic Sans MS', int(ui_size / 2.5))


    screen = pg.display.set_mode([screen_width, screen_height])
    pg.display.set_caption('Tetris')

    #Image
    btn1_img, btn2_img = [0]*2, [0]*2
    for i in range(2):
        btn1_img[i] = pg.transform.smoothscale(pg.image.load(f'Image/b1-{i}.png'), (ui_size * 2.5, ui_size))
        btn2_img[i] = pg.transform.smoothscale(pg.image.load(f'Image/b2-{i}.png'), (100, 100))
    border = (pg.transform.smoothscale(pg.image.load('Image/border.png'), (sq_size * (columns+2), sq_size * (rows+2))))
    board_size, board2_size = (ui_size*4, ui_size*5.6), (ui_size*6, ui_size*8.4)
    board_img = pg.transform.smoothscale(pg.image.load('Image/board.png'), board_size)
    board2_img = pg.transform.smoothscale(pg.image.load('Image/board.png'), board2_size)
    textbar_size = (ui_size*5.2,ui_size*5.2/6)
    textbar_img = pg.transform.smoothscale(pg.image.load('Image/textbar.png'), textbar_size)
    te_img = []
    for i in range(8):
        te_img.append(pg.transform.smoothscale(pg.image.load(f'Image/t{i}.png'), (sq_size, sq_size)))

    #Font
    font1 = pg.font.SysFont('Comic Sans MS', int(ui_size / 3))
    type_font = pg.font.SysFont('Consolas', int(ui_size / 1.8))
    big_font = pg.font.SysFont('Comic Sans MS', int(ui_size / 1.5))

    #Data
    high_score_data = []
    data = []
    for s in (0, 1, 2):
        try:
            f = open(f"Data/{s}.hscr")
            data = f.readlines()
            for i in range(len(data)):
                data[i] = data[i][:-1]
        except FileNotFoundError:  # Sample high score
            for i in range(10):
                data.append(f"Player{i+1}")
                data.append(str(1000-i*100))
        high_score_data.append(data)
        data = []

    scene = "Main menu"

    while True:
        screen.fill((0,0,0))
        if scene == "Main menu":
            scene = main_menu()
        elif scene == "New game":
            next = rnd.choice(tetrominos)
            character = tetromino(next)
            next = rnd.choice(tetrominos)
            next_show = copy.deepcopy(tetromino(next))
            grid = [0] * columns * rows
            score = 0
            d = select_difficulty()
            if d == 0:
                speed = 350
            elif d == 1:
                speed = 250
            elif d == 2:
                speed = 150
            scene = game(character, next_show, speed, score, grid, d)
        elif scene == "Load game":
            data = load_game()
            if data != 0:
                print("Load complete")
                character = tetromino(data[0])
                character.row = data[1]
                character.column = data[2]
                next_show = copy.deepcopy(tetromino(data[3]))
                next = rnd.choice(tetrominos)
                speed = data[4]
                score = data[5]
                d = data[6]
                grid = data[7]
                scene = game(character, next_show, speed, score, grid, d)
            else:
                scene = "Main menu"
        elif scene == "High score":
            scene = high_score_ui(select_difficulty())
        elif scene == "Exit game":
            break

    pg.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
