
class FuzzyController:
    """
    #todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self):
        pass

    def decide(self, left_dist, right_dist):
        """
        main method for doin all the phases and returning the final answer for rotation
        """

        return (self.defuzz(
            self.get_active_rules(self.membership_right_dist(right_dist), self.membership_left_dist(left_dist))))

    """this function returns the defuzzificationed  value of rotation"""
    def defuzz(self, membership_rotate):
        X = {}
        X_u_rotate = {}
        type_period = {"u_high_right": (-50, -5), "u_low_right": (-20, 0), "u_nothing": (-10, 10),
                       "u_low_left": (10, 20),
                       "u_high_left": (5, 50)}
        active_rules = [rule for rule in membership_rotate.keys() if eval(membership_rotate[rule]) > 0]
        step_len = 0.1
        for rule in active_rules:
            start, end = type_period[rule]
            for i in range(int(start / step_len), int(end // step_len) + 1):
                index = str("%.10f" % int(i * step_len))
                index_u_membership = eval(
                    X_u_rotate.get(index, self.get_membership_rotation_per_point(eval(index))[rule]))
                current_rule_membership = eval(membership_rotate[rule])
                X[index] = max(min(index_u_membership, current_rule_membership), X.get(index, 0))
        soorat = 0
        makhraj = 0
        for x in X.keys():
            soorat = soorat + eval(x) * X[x]
            makhraj = makhraj + X[x]

        return (soorat / makhraj)

    """this function returns active rules based  on rules and memberships """
    def get_active_rules(self, membership_r, membership_l):
        membership_rotate = {}
        # rule 1 :IF (d_L IS close_L ) AND (d_R IS moderate_R)  THEN  Rotate IS low_right
        # rule 2 :IF (d_L IS close_L ) AND (d_R IS far_R)  THEN  Rotate IS high_right
        # rule 3: IF (d_L IS moderate_L ) AND (d_R IS close_R)  THEN  Rotate IS low_left
        # rule 4: IF (d_L IS far_L ) AND (d_R IS close_R)  THEN  Rotate IS high_left
        # rule 5: IF (d_L IS moderate_L ) AND (d_R IS moderate_R)  THEN  Rotate IS nothing
        membership_rotate["u_low_right"] = min(membership_l["close_L"], membership_r["moderate_R"])
        membership_rotate["u_high_right"] = min(membership_l["close_L"], membership_r["far_R"])
        membership_rotate["u_low_left"] = min(membership_l["moderate_L"], membership_r["close_R"])
        membership_rotate["u_high_left"] = min(membership_l["far_L"], membership_r["close_R"])
        membership_rotate["u_nothing"] = min(membership_l["moderate_L"], membership_r["moderate_R"])

        return membership_rotate

    """this function  gives point that shows rotation and return its membership according to given chart"""
    def get_membership_rotation_per_point(self, x):
        membership = {}
        u_high_right = lambda x: (x + 50) * 1 / 30 if -50 <= x <= -20 else (
            1 - 1 / 15 * (x + 20) if -20 <= x <= -5 else 0)
        u_low_right = lambda x: (x + 20) * 1 / 10 if -20 <= x <= -10 else (
            1 - 1 / 10 * (x + 10) if -10 <= x <= 0 else 0)
        u_nothing = lambda x: (x + 10) * 1 / 10 if -10 <= x <= 0 else (1 - 1 / 10 * (x) if 0 <= x <= 10 else 0)
        u_low_left = lambda x: (x) * 1 / 10 if 0 <= x <= 10 else (1 - 1 / 10 * (x - 10) if 10 <= x <= 20 else 0)
        u_high_left = lambda x: (x - 5) * 1 / 15 if 5 <= x <= 20 else (1 - 1 / 30 * (x - 20) if 20 <= x <= 30 else 0)
        membership["u_low_right"] = "%.10f" % u_low_right(x)
        membership["u_high_right"] = "%.10f" % u_high_right(x)
        membership["u_nothing"] = "%.10f" % u_nothing(x)
        membership["u_low_left"] = "%.10f" % u_low_left(x)
        membership["u_high_left"] = "%.10f" % u_high_left(x)
        return membership

    """
    the two following functions return the membership of given dist according to  given chart per each direction
    """
    def membership_left_dist(self, dist):
        membership = {}
        close_L = lambda d: -0.02 * d + 1 if 0 <= d <= 50 else (0 if d > 50 else 1)#
        moderate_L = lambda d: (1 / 15) * (d - 35) if 35 <= d <= 50 else (1-(1 / 15) * (d-50) if 50 <= d <= 65 else 0)
        far_L = lambda d: 0.02 * (d - 50) if 50 <= d <= 100 else (0 if d < 50 else 1)
        membership["close_L"] = "%0.10f" % close_L(dist)
        membership["moderate_L"] = "%0.10f" % moderate_L(dist)
        membership["far_L"] = "%0.10f" % far_L(dist)
        return membership

    def membership_right_dist(self, dist):
        membership = {}
        close_R = lambda d: -0.02 * d + 1 if 0 <= d <= 50 else (0 if d > 50 else 1)
        moderate_R = lambda d: (1 / 15) * (d - 35) if 35 <= d <= 50 else (1-(1 / 15) * (d-50) if 50 <= d <= 65 else 0)
        far_R = lambda d: 0.02 * (d - 50) if 50 <= d <= 100 else (0 if d < 50 else 1)
        membership["close_R"] = "%0.10f" % close_R(dist)
        membership["moderate_R"] = "%0.10f" % moderate_R(dist)
        membership["far_R"] = "%0.10f" % far_R(dist)
        return membership
