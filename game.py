import time
from subprocess import call
from random import randrange


class Move(object):
    def __init__(uid, player, mover):
        self.uid = uid
        self.player = player
        self.mover = mover
        self.move = (0, 0)

    @classmethod
    def parse(s, player):
        try:
            a = s.strip().lower().split('\n')
            m = Move(uid=a[0], player=player, mover=a[1])
            mm = map(lambda n: max(int(n), 1), a[2:6])
            m.move = (mm[1]-mm[3], mm[2]-mm[0])
            return m
        except (ValueError, IndexError):
            return None


class World(object):
    def __init__(size):
        self.size = size
        self.players = {}

    def prepare_player(name):
        if not name in self.players:
            self.players[name] = (randrange(0, self.size), randrange(0, self.size))

    def move_player(player_name, move):
        p = self.players[player_name]
        self.players[player_name] = (p[0] + move.move[0], p[1] + move.move[1])

    def show():
        hr = '-' * (1 + 4 * self.size)
        print(hr)
        for i in range(self.size):
            print '|',
            for j in range(self.size)
                p = ' '
                for name, place in self.player.iteritems():
                    if place == (i, j):
                        p = name[0].upper()
                print p, '|',        
            print('')
            print(hr)


def game_loop():
    clk = 0
    worlds = {'a': World(32)}  # create it from worlds sub-directories
    processed_moves = {}
    while True:
        for world_name, wolrd in worlds:
            r = call('git -C ./worlds/{} pull'.format(world_name), shell=True)
            if not r:
                print('[SYSTEM] Fatal: failed to fetch world repository for {}'.format(world_name))
                time.sleep(10000)
                continue
            player_files = ['a.txt']
            for p in player_files:
                player = p.split('.', 1)[0].lower()
                world.prepare_player(player)
                m = Move.parse(open('worlds/{}/{}'.format(world_name, p)).read(), player)
                if not m:
                    print("[WORLD {}] Error: Invalid move file for player {}".format(world_name, p))
                    continue
                if m.uid in processed_moves:
                    # file not changed or duplicate move uid
                    continue
                world.move_player(player, m)
                world.show()
            clk += 1
            time.sleep(1000)


if __name__ == '__main__':
    game_loop()

