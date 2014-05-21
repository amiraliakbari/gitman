import os
import time
from subprocess import call
from random import seed, randrange


class Move(object):
    def __init__(self, uid, player, mover):
        self.uid = uid
        self.player = player
        self.mover = mover
        self.move = (0, 0)

    @classmethod
    def parse(cls, s, player):
        # Format: MOVE-UID \n MOVER \n TOP \n RIGHT \n BOTTOM \n LEFT
        try:
            a = s.strip().lower().split('\n')
            m = cls(uid=a[0], player=player, mover=a[1])
            mm = map(lambda n: min(int(n), 1), a[2:6])
            m.move = (mm[2]-mm[0], mm[1]-mm[3])
            return m
        except (ValueError, IndexError):
            return None


class World(object):
    def __init__(self, world_name, size):
        self.world_name = world_name
        self.size = size
        self.players = {}
        self.done = []

    def prepare_player(self, name):
        if not name in self.players:
            self.players[name] = (randrange(0, self.size), randrange(0, self.size))

    def update_winner(self):
        n = self.size
        self.done = []
        for player_name, loc in self.players.iteritems():
            i, j = loc
            if i < 0:
                self.done.append((player_name, j + 1))
            if j >= n:
                self.done.append((player_name, i + n + 1))
            if i >= n:
                self.done.append((player_name, (n - j) + 2 * n))
            if j < 0:
                self.done.append((player_name, (n - i) + 3 * n))

    def is_player_done(self, player_name):
        return player_name in [x for x, _ in self.done]

    def move_player(self, player_name, move):
        if self.is_player_done(player_name):
            print('[RULE] player {} is done and can not be moved!'.format(player_name))
            return
        p = self.players[player_name]
        print('[MOVE] player: {}, move: {}'.format(player_name, move.move))
        self.players[player_name] = (p[0] + move.move[0], p[1] + move.move[1])
        self.update_winner()

    def show(self):
        b = ''
        hr = '-' * (1 + 4 * self.size)
        b += hr + '\n'
        for i in range(self.size):
            b += '| '
            for j in range(self.size):
                p = ' '
                for name, place in self.players.iteritems():
                    if place == (i, j):
                        p = name[0].upper()
                b += p + ' | '
            b += '\n' + hr + '\n'
        b += str(self.done)
        with open(os.path.join('output', self.world_name), 'w') as f:
            f.write(b)


def game_loop():
    seed()
    clk = 0
    worlds = {'a': World('a', 16)}  # create it from worlds sub-directories
    processed_moves = {}
    while True:
        for world_name, world in worlds.iteritems():
            world.show()
            r = call('git -C ./worlds/{} pull'.format(world_name), shell=True)
            if r != 0:
                print('[SYSTEM] Fatal: failed to fetch world repository for {}'.format(world_name))
                time.sleep(10000)
                continue
            player_files = ['a.txt', 'b.txt', 'c.txt']
            for p in player_files:
                player = p.split('.', 1)[0].lower()
                world.prepare_player(player)
                try:
                    content = open('worlds/{}/{}'.format(world_name, p)).read()
                    m = Move.parse(content, player)
                except IOError:
                    continue
                if not m:
                    print("[WORLD {}] Error: Invalid move file for player {}".format(world_name, p))
                    continue
                if m.uid in processed_moves:
                    # file not changed or duplicate move uid
                    continue
                world.move_player(player, m)
                world.show()
                processed_moves[m.uid] = m
        clk += 1
        time.sleep(1)


if __name__ == '__main__':
    game_loop()

