
class RandomNumberGenerator:

    def __init__(self, seed):
        # init
        self.cur_round = 0
        self.last_generated = []

        self.seed_0 = seed
        self.a = 48271
        self.q = 44488
        self.r = 3399
        # m = a * q + r
        self.m = 2**31 - 1
        self.arrivalOrigin = 11
        self.j = 100000
        self.newly_generated = []
        self.new_numbers = []
        self.new_number = 0

    def GetRandList(self):
        self.new_numbers = []
        self.newly_generated = []
        for s in range(0, self.arrivalOrigin):
            if self.cur_round == 0:
                self.seed_0 = (pow(self.a, self.j) %
                               self.m) * self.seed_0 % self.m

            else:
                t = self.a * \
                    (self.last_generated[s] % self.q) - \
                    self.r * (self.last_generated[s] / self.q)
                if t > 0:
                    self.seed_0 = t
                else:
                    self.seed_0 = t + self.m

            self.new_number = float(self.seed_0) / self.m
            self.newly_generated.append(self.seed_0)
            self.new_numbers.append(self.new_number)

        self.cur_round += 1
        self.last_generated = self.newly_generated
        return self.new_numbers
