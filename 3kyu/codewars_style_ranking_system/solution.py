from main import Test


class User(object):
    _rank_list = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self):
        self.progress = 0
        self.rank = self._rank_list[0]
        self.reward_map = {i: 10 * i ** 2 for i in xrange(len(self._rank_list))}
        self.reward_map[0] = 3
        self.reward_map[-1] = 1

    def inc_progress(self, activity_rank):
        points_earned = self._calculate_points(activity_rank)
        self.progress += points_earned
        while self.progress >= 100:
            self.progress -= 100
            self._rank_up()
        self._rank_cap()

    def _calculate_points(self, activity_rank, user_rank=None):
        user_rank = user_rank if user_rank else self.rank
        user_rank = self._rank_list.index(user_rank)
        activity_rank = self._rank_list.index(activity_rank)
        rank_difference = activity_rank - user_rank

        return self.reward_map.get(
            rank_difference) if rank_difference > -2 else 0

    def _rank_up(self):
        if not self.rank == self._rank_list[-1]:
            true_rank = self._rank_list.index(self.rank)
            self.rank = self._rank_list[true_rank + 1]
        self._rank_cap()

    def _rank_cap(self):
        if self.rank == self._rank_list[-1]:
            self.progress = 0




Test.it("Calculates points, given activity and user ranks")
calculate_points = User()
Test.assert_equals(calculate_points._calculate_points(-8, -6), 0)
Test.assert_equals(calculate_points._calculate_points(-8, -7), 1)
Test.assert_equals(calculate_points._calculate_points(-8, -8), 3)
Test.assert_equals(calculate_points._calculate_points(-7, -8), 10)
Test.assert_equals(calculate_points._calculate_points(-6, -8), 40)
Test.assert_equals(calculate_points._calculate_points(-5, -8), 90)
Test.assert_equals(calculate_points._calculate_points(-4, -8), 160)
Test.assert_equals(calculate_points._calculate_points(1, -1), 10)
Test.assert_equals(calculate_points._calculate_points(8, -8), 2250)
Test.assert_equals(calculate_points._calculate_points(-3, -1), 0)
Test.assert_equals(calculate_points._calculate_points(-2, 1), 0)
Test.assert_equals(calculate_points._calculate_points(-3, 1), 0)
Test.assert_equals(calculate_points._calculate_points(-4, 1), 0)

Test.it("Has a max rank")
rank_up = User()
rank_up.rank = 7
rank_up.progress = 70
rank_up._rank_up()
Test.assert_equals(rank_up.rank, 8)
Test.assert_equals(rank_up.progress, 0)
del rank_up


rank_up = User()
rank_up.rank = 8
rank_up.progress = 70
rank_up._rank_up()
Test.assert_equals(rank_up.rank, 8)
Test.assert_equals(rank_up.progress, 0)
del rank_up


rank_up = User()
rank_up.rank = -1
rank_up.progress = 70
rank_up._rank_up()
Test.assert_equals(rank_up.rank, 1)
Test.assert_equals(rank_up.progress, 70)
del rank_up


user = User()
Test.assert_equals(user.rank, -8)
Test.assert_equals(user.progress, 0)

user.inc_progress(-7)
Test.assert_equals(user.progress, 10)

user.inc_progress(-5)  # will add 90 progress
Test.assert_equals(user.progress, 0)  # progress is now zero
Test.assert_equals(user.rank, -7)  # rank was upgraded to -7

user.inc_progress(-2)
Test.assert_equals(user.progress, 50)
Test.assert_equals(user.rank, -5)

user.inc_progress(4)
Test.assert_equals(user.progress, 90)
Test.assert_equals(user.rank, 2)

user.inc_progress(-1)
Test.assert_equals(user.progress, 90)
Test.assert_equals(user.rank, 2)

user.inc_progress(7)
Test.assert_equals(user.progress, 40)
Test.assert_equals(user.rank, 5)

user.inc_progress(8)
Test.assert_equals(user.progress, 30)
Test.assert_equals(user.rank, 6)

user.inc_progress(8)
Test.assert_equals(user.progress, 70)
Test.assert_equals(user.rank, 6)

user.inc_progress(8)
Test.assert_equals(user.progress, 10)
Test.assert_equals(user.rank, 7)

for _ in xrange(8):
    user.inc_progress(8)

Test.assert_equals(user.progress, 90)
Test.assert_equals(user.rank, 7)

user.inc_progress(8)
Test.assert_equals(user.progress, 0)
Test.assert_equals(user.rank, 8)

user.inc_progress(8)
Test.assert_equals(user.progress, 0)
Test.assert_equals(user.rank, 8)

user.inc_progress(8)
Test.assert_equals(user.progress, 0)
Test.assert_equals(user.rank, 8)