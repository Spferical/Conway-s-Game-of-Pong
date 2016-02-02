import libtcodpy as tcod
import config
import conway
import util


def constrain_value(x, (low, high)):
    if x < low:
        x = low
    elif x > high:
        x = high
    return x


class Player():
    dy = 0
    down = up = False
    score = 0

    @property
    def bottom(self):
        "The bottom of his paddle"
        return self.top + self.size

    @property
    def middle(self):
        "The middle of the paddle"
        return (self.top + self.bottom) / 2

    def __init__(self, (x, y), color, size=3, controls=None):
        self.x = x
        self.top = y
        self.color = color
        self.size = size
        self.controls = controls

    def update(self):
        self.dy = self.down - self.up
        self.top += self.dy

    def update_ai(self, ball, screen_height):
        if abs(ball.x - self.x) < screen_height / 2:
            if self.middle < ball.y:
                self.down = True
                self.up = False
            elif self.middle > ball.y:
                self.down = False
                self.up = True
            else:
                self.up = self.down = False
        else:
            self.up = self.down = False


class Ball(object):
    dx = dy = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x += self.dx
        self.y += self.dy


def render_conway_sim(sim):
    for x in range(sim.width):
        for y in range(sim.height):
            if sim[x, y]:
                if sim.color: color = sim[x, y]
                else: color = tcod.green
                tcod.console_set_char_background(0, x, y, color)


class Game():
    alive = True
    conway_timer = 0

    def __init__(self, player_controls, conway_speed, map_size, fps, color,
                 paddle_size, seamless):
        self.width, self.height = map_size
        self.init_players(player_controls, paddle_size)
        self.init_map(map_size, color)
        (w, h) = map_size
        tcod.console_init_root(w, h, config.GAME_TITLE, False)
        tcod.sys_set_fps(fps)
        self.conway_speed = conway_speed
        self.ball = Ball(1, 1)
        self.seamless = seamless

    def init_players(self, controls, paddle_size):
        self.players = []
        for i in range(len(controls)):
            if i == 0:
                x = 0
            elif i == 1:
                x = self.width - 1
            y = self.height / 2
            self.players.append(Player((x, y),
                                       config.PLAYER_COLORS[i],
                                       controls=controls[i],
                                       size=paddle_size))

    def init_map(self, size, color):
        self.conway = conway.ConwaySim(size, color)

    def run(self):
        while self.alive and not tcod.console_is_window_closed():
            self.update()

    def start_new_round(self, winner_of_last_round=None):
        """starts a new round of pong
        says who won, shows a countdown, moves the ball to the center, resets the players
        at the end, wipes the conway sim and resumes play """

        # lets do stuff in an off-screen console, so we can use transparency
        # so the player can see the map
        con = tcod.console_new(self.width, self.height)
        time_elapsed = 0.0  # in seconds
        x = self.width / 2
        tcod.console_set_alignment(con, tcod.CENTER)
        while self.alive and not tcod.console_is_window_closed() and \
                time_elapsed < 3.0:
            y = self.height / 2
            if winner_of_last_round:
                tcod.console_set_default_foreground(con,
                                                    winner_of_last_round.color)
                player_num = self.players.index(winner_of_last_round) + 1
                string = "Player %d scores!" % player_num
                height = tcod.console_get_height_rect(con, x, y, self.width,
                                                      self.height, string)
                tcod.console_print_rect(con, x, y, self.width, height, string)
                y += height
            tcod.console_set_default_foreground(con, tcod.white)

            string = "New round starting in %d seconds..." % int(3 - time_elapsed)
            height = tcod.console_get_height_rect(con, x, y, self.width,
                                                  self.height,  string)
            tcod.console_print_rect(con, x, y, self.width, height, string)

            self.handle_input()
            self.update_conway()
            self.render_all()
            tcod.console_blit(con, 0, 0, 0, 0, 0, 0, 0, 1.0, 0.75)
            tcod.console_flush()
            time_elapsed += tcod.sys_get_last_frame_length()


        # delete tcod console we created
        tcod.console_delete(con)

        #reset the ball
        self.ball = Ball(1, 1)

        #reset the player positions
        for player in self.players:
            player.top = self.height / 2

        # wipe the conway simulation (by creating a new one)
        self.init_map(self.conway.size, self.conway.color)


    def update(self):
        self.handle_input()
        self.update_players()
        self.constrain_player_positions()
        self.handle_collisions()
        self.handle_screen_edge_collisions()
        self.update_ball()
        self.update_conway()
        self.update_scores()
        self.render_all()
        tcod.console_flush()

    def update_scores(self):
        if self.ball.x == 0:
            self.players[1].score += 1
            if not self.seamless:
                self.start_new_round(self.players[1])
        elif self.ball.x == self.width - 1:
            self.players[0].score += 1
            if not self.seamless:
                self.start_new_round(self.players[0])

    def update_conway(self):
        self.conway_timer += 1
        self.conway[self.ball.x, self.ball.y] = tcod.white

        for player in self.players:
            for y in range(player.top, player.bottom + 1):
                self.conway[player.x, y] = player.color
        if self.conway_timer >= self.conway_speed:
            self.conway.update()
            self.conway_timer = 0

    def update_players(self):
        for player in self.players:
            if player.controls == 'ai':
                player.update_ai(self.ball, self.height)
            player.update()

    def update_ball(self):
        self.ball.update()

    def render_players(self):
        for player in self.players:
            for y in range(player.top, player.bottom + 1):
                tcod.console_put_char_ex(0, player.x, y, 'I',
                        tcod.black, player.color)

    def render_ball(self):
        tcod.console_put_char_ex(0, self.ball.x, self.ball.y, 'O',
                                 tcod.black, tcod.white)

    def render_scores(self):
        tcod.console_set_alignment(0, tcod.CENTER)
        for i in range(len(self.players)):
            tcod.console_set_default_foreground(0, config.PLAYER_COLORS[i])
            tcod.console_print(0, self.width / 2, i,
			    "P%d: %d" % (i + 1, self.players[i].score))

    def render_all(self):
        tcod.console_clear(0)
        render_conway_sim(self.conway)
        self.render_players()
        self.render_ball()
        self.render_scores()
        self.render_fps()

    def render_fps(self):
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_print_ex(0, 0, self.height - 1, tcod.BKGND_NONE, tcod.LEFT,
                              "%d FPS" % tcod.sys_get_fps())

    def constrain_player_positions(self):
        for player in self.players:
            ybounds = (0, self.height - 1 - player.size)
            player.top = constrain_value(player.top, ybounds)

    def handle_collisions(self):
        xcol = ycol = False
        #collide with conway sim cells
        if self.conway.get_blocked((self.ball.x + self.ball.dx, self.ball.y)):
            self.ball.dx = - self.ball.dx
            xcol = True
        if self.conway.get_blocked((self.ball.x, self.ball.y + self.ball.dy)):
            self.ball.dy = - self.ball.dy
            ycol = True
        if not (xcol or ycol):
            if self.conway.get_blocked((self.ball.x + self.ball.dx,
                                        self.ball.y + self.ball.dy)):
                self.ball.dx = - self.ball.dx
                self.ball.dy = - self.ball.dy

        #collide with players
        #player collisions are checked last, for precedence
        for player in self.players:
            future_x = self.ball.x + self.ball.dx
            if future_x == player.x:
                future_y = self.ball.y + self.ball.dy
                if future_y >= player.top and future_y <= player.bottom:
                    self.ball.dx = - self.ball.dx


    def handle_screen_edge_collisions(self):
        # with the conway simulation updating (practically) unpredictably,
        # the ball can 'bounce' out of bounds
        # to ensure that never happens, make sure that if the ball is
        # travelling out of bounds, make it /not/ travel out of bounds
        x = self.ball.x + self.ball.dx #  so test the ball's predicted x
        y = self.ball.y + self.ball.dy #  and y position
        #if the ball will travel out of bounds: make sure it moves in the
        #opposite direction
        if self.ball.x == 0: self.ball.dx = 1
        if self.ball.y == 0: self.ball.dy = 1
        if self.ball.x == self.width - 1: self.ball.dx = -1
        if self.ball.y == self.height - 1: self.ball.dy = -1


    def handle_input(self):
        raw_key = tcod.console_check_for_keypress(
            tcod.KEY_PRESSED | tcod.KEY_RELEASED)
        while raw_key.vk != tcod.KEY_NONE:
            key = util.get_key(raw_key)
            if key == tcod.KEY_ESCAPE:
                self.alive = False
            for player in self.players:
                if player.controls not in ['ai', None]:
                    if key in player.controls:
                        if raw_key.pressed:
                            if player.controls.index(key) == 0:  # up
                                player.up = True
                            else:
                                player.down = True  # down
                        else:
                            if player.controls.index(key) == 0:  # up
                                player.up = False
                            else:
                                player.down = False
            raw_key = tcod.console_check_for_keypress(
                tcod.KEY_PRESSED | tcod.KEY_RELEASED)
