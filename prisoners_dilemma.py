import random
import numpy as np

SCORE = [[3, 0], [5, 1]]
C = 0
D = 1

PLAYER = []

"""
Playerの種類
AllC: All-C
AllD: All-D
TFT: しっぺ返し
Random: ランダム
Downing
Joss
Tester
TFTT: Tit For Two Tat
DTFT
DDowning
Tranquilizer
"""

class Player:
    def __init__(self):
        self.my_score = 0

    def action(self):
        pass

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]

# All-C
class AllC(Player):
    def action(self):
        return C

# All-D
class AllD(Player):
    def action(self):
        return D

# Tit For Tat(しっぺ返し)
class TFT(Player):
    def __init__(self):
        self.my_score = 0
        self.opp_prev_action = 0

    def action(self):
        if self.opp_prev_action == C:
            return C
        else:
            return D

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.opp_prev_action = a2

class Random(Player):
    def action(self):
        return random.randrange(2)

class Downing(Player):
    def __init__(self):
        self.my_score = 0
        self.my_prev_action = 0
        self.prop_c = 0.5
        self.prop_d = 0.5

    def action(self):
        if abs(self.prop_c - self.prop_d) < 0.1:
            return D
        # 協調したら協調してくる→C
        elif self.prop_c > self.prop_d:
            return C
        # 裏切っても協調してくる→裏切る
        elif self.prop_d > self.prop_c:
            return D

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.update(a2)
        self.my_prev_action = a1

    def update(self, a2):
        if self.my_prev_action == 0:
            if a2 == 0:
                self.prop_c += 0.05
            else:
                self.prop_d += 0.05
        else:
            if a2 == 0:
                self.prop_d += 0.05
            else:
                self.prop_c += 0.05

class Joss(Player):
    def __init__(self):
        self.my_score = 0
        self.opp_prev_action = 0

    def action(self):
        if self.opp_prev_action == 0:
            if random.randrange(10) == 0:
                return D
            else:
                return C
        else:
            return D

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.opp_prev_action = a2

class Tester(Player):
    def __init__(self):
        self.counter = 0
        self.tit_flg = False
        self.opp_prev_action = C
        self.my_score = 0

    def action(self):
        # 初回は裏切る
        if self.counter == 0:
            return D
        # (D,C)→(C,D)ならしっぺ返し
        if self.counter == 2:
            if self.my_first_action == D and self.opp_first_action == C and self.my_second_action == C and self.opp_second_action == D:
                self.tit_flg = True
            else:
                return C

        if self.counter == 3 and not self.tit_flg:
            return C

        if self.tit_flg:
            if self.opp_prev_action == C:
                return C
            else:
                return D
        else:
            if self.my_prev_action == C:
                return D
            else:
                return C

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.counter += 1
        if self.counter == 1:
            self.my_first_action = a1
            self.opp_first_action = a2
        if self.counter == 2:
            self.my_second_action = a1
            self.opp_second_action = a2
        self.my_prev_action = a1
        self.opp_prev_action = a2

# Tit for two tat
class TFTT(Player):
    def __init__(self):
        self.my_score = 0
        self.opp_prev_action = 0
        self.opp_prev_prev_action = 0

    def action(self):
        if self.opp_prev_action == 1 and self.opp_prev_prev_action == 1:
            return D
        else:
            return C

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.opp_prev_action = a2
        self.opp_prev_prev_action = self.opp_prev_action

# 変形しっぺ返し: 3回目裏切るやつ
class DTFT(Player):
    def __init__(self):
        self.my_score = 0
        self.opp_prev_action = 0
        self.counter = 0

    def action(self):
        if self.counter == 2:
            return D
        if self.opp_prev_action == C:
            return C
        else:
            return D

    def add_score(self, a1, a2):
        self.counter += 1
        self.my_score += SCORE[a1][a2]
        self.opp_prev_action = a2

# 変形Downing
class DDowning(Player):
    def __init__(self):
        self.my_score = 0
        self.my_prev_action = 0
        self.prop_c = 0.5
        self.prop_d = 0.5
        self.counter = 0
        self.opp_coop_count = 0
        self.opp_coop_prop = 0

    def action(self):
        if abs(self.prop_c - self.prop_d) < 0.1:
            return D
        # 協調したら協調してくる→C
        elif self.prop_c > self.prop_d:
            return C
        # 裏切っても協調してくる→裏切る
        elif self.prop_d > self.prop_c:
            return D

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.counter += 1
        self.update(a2)
        self.my_prev_action = a1

    def update(self, a2):
        if self.my_prev_action == 0:
            if a2 == C:
                self.prop_c += 0.05
                self.opp_coop_count += 1
            else:
                self.prop_d += 0.05
        else:
            if a2 == C:
                self.prop_d += 0.05
                self.opp_coop_count += 1
            else:
                self.prop_c += 0.05
        self.opp_coop_prop = self.opp_coop_count / self.counter

class Tranquilizer(Player):
    def __init__(self):
        self.my_score = 0
        self.counter = 0
        self.my_scores = []
        self.init_phase = 10 + random.randrange(11)
        self.my_defect_count = 0
        self.my_defect_prop = 0
        self.my_prev_action = 0
        self.opp_defect_count = 0
        self.opp_defect_prop = 0
        self.cont_both_coop = 0

    def action(self):
        # 裏切りが25%を超えないようにする
        if self.my_defect_prop >= 0.25:
            return C

        # 相手が裏切ってきたら裏切る覚悟をする
        if self.opp_defect_prop >= 0.3:
            return D

        # 10~20までは協調する
        if self.counter < self.init_phase:
            return C

        # 平均点が2.25以上の時，2回連続で裏切らない
        if self.average >= 2.25 and self.my_prev_action == D:
            return C

        # 協調するパターンが発生したら裏切る
        if self.cont_both_coop >= 3:
            return D

        return C

    def add_score(self, a1, a2):
        self.counter += 1

        self.my_score += SCORE[a1][a2]
        self.my_scores.append(SCORE[a1][a2])
        self.average = sum(self.my_scores) / self.counter
        self.my_prev_action = a1
        if a1 == D:
            self.my_defect_count += 1
        if a2 == D:
            self.opp_defect_count += 1
        if a1 == C and a2 == C:
            self.cont_both_coop += 1
        else:
            self.cont_both_coop = 0
        self.my_defect_prop = self.my_defect_count / self.counter
        self.opp_defect_prop = self.opp_defect_count / self.counter

class MyStrategy(Player):
    def __init__(self):
        self.my_score = 0
        self.my_prev_action = C
        self.prev_score = 3

    def action(self):
        if self.my_prev_action == C:
            # うまくいったら(C, C) → 3
            if self.prev_score == 3:
                return C
            # (C, D) → 0
            else:
                return D
        else:
            # (D, C) → 5
            if self.prev_score == 2:
                return D
            # (D, D) → 1
            else:
                return C

    def add_score(self, a1, a2):
        self.my_score += SCORE[a1][a2]
        self.my_prev_action = a1
        self.prev_score = SCORE[a1][a2]

class PlayerCreator:
    def create_player(self, name):
        if name == "AllC":
            return AllC()
        elif name == "AllD":
            return AllD()
        elif name == "TFT":
            return TFT()
        elif name == "Random":
            return Random()
        elif name == "Downing":
            return Downing()
        elif name == "Joss":
            return Joss()
        elif name == "Tester":
            return Tester()
        elif name == "TFTT":
            return TFTT()
        elif name == "DTFT":
            return DTFT()
        elif name == "DDowning":
            return DDowning()
        elif name == "Tranquilizer":
            return Tranquilizer()
        elif name == "MyStrategy":
            return MyStrategy()
        else:
            import sys
            print("Not Defined {}.".format(name))
            sys.exit(1)

class TableData:
    def __init__(self, header):
        self.header = header
        self.length = len(self.header) + 1
        self.array = [[0 for i in range(self.length)] for j in range(self.length)]
        self.array[0][0] = "P1/P2"
        count = 1
        for h in self.header:
            self.array[0][count] = h
            self.array[count][0] = h
            count += 1

    def add_data(self, s1, s2, x, y):
        self.array[x][y] = "({}, {})".format(s1, s2)

    def print_data(self):
        print("\n\n")
        x = 0
        y = 0
        for x in range(self.length):
            for y in range(self.length):
                print("|{:^12}|".format(self.array[x][y]), end=" ")
            print("\n")

    def print_sum_data(self):
        from statistics import mean, median,variance,stdev
        print("\n\n")
        i = 0
        header = ["Name", "Sum", "Mean", "Median", "Var", "Std"]
        print("| {:>12} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5}  |".format(header[0], header[1], header[2], header[3], header[4], header[5]))
        for h in self.header:
            arr = []
            for j in self.array[i+1][1:]:
                arr.append(int(j.split('(')[1].split(',')[0]))

            print("| {:>12} | {:^5} | {:^.2f} | {:^5} | {:^.0f} | {:^.2f} |".format(self.header[i], sum(arr), mean(arr), median(arr), variance(arr), stdev(arr)))
            i += 1
        print("\n\n")


def play_game(p1, p2):
    # print("Player1({}): {}".format(p1.__class__.__name__, p1.my_score))
    # print("Player2({}): {}".format(p2.__class__.__name__, p2.my_score))

    loop_time = 200
    for i in range(loop_time):
        a1 = p1.action()
        a2 = p2.action()
        # print("({}, {})".format(a1, a2))
        p1.add_score(a1, a2)
        p2.add_score(a2, a1)

    # print("Player1({}): {}".format(p1.__class__.__name__, p1.my_score))
    # print("Player2({}): {}".format(p2.__class__.__name__, p2.my_score))

    return [p1.my_score, p2.my_score]

def main():
    player_arr = ["AllC", "AllD", "TFT", "Random", "Downing", "Joss", "Tester", "TFTT", "DTFT", "DDowning", "Tranquilizer", "MyStrategy"]
    td = TableData(player_arr)
    pc = PlayerCreator()
    x = 1
    for pp1 in player_arr:
        y = 1
        for pp2 in player_arr:
            p1 = pc.create_player(pp1)
            p2 = pc.create_player(pp2)
            s1, s2 = play_game(p1, p2)
            td.add_data(s1, s2, x, y)
            y += 1
        x += 1
    # p1 = Downing()
    # p2 = TFT()
    # play_game(p1, p2)
    td.print_data()
    td.print_sum_data()

if __name__ == '__main__':
    main()
