# -*- coding: utf-8 -*-
from scipy.integrate import odeint
import numpy as np


class SEIR:
    def __init__(self,
                 incubation_period=5.2,
                 infective_period=2.9,
                 basic_reproduction_rate=3.4,
                 intervention_times=(23, 30, 60, 230, 330),
                 p0=(83019212., 0., 1., 0.),
                ):
        if infective_period <= 0.:
            raise Exception("infective_period must be larger than 0")
        self.t_inf = infective_period

        if incubation_period <= 0.:
            raise Exception("incubation_period must be larger than 0")
        self.t_inc = incubation_period

        if incubation_period < 0.:
            raise Exception("incubation_period must 0 or larger")
        self.r0 = basic_reproduction_rate

        self.p0 = tuple(p0)
        if len(self.p0) != 4:
            raise Exception("p0 must contain 4 values")
        self.n = sum(self.p0)

        if not np.all(intervention_times[1:] >= intervention_times[:-1]):
            raise Exception("intervention_times[] must be monotonically increasing")
        self.intervention_times = intervention_times

    def get_current_r(self, t, r_list):
        current_r = r_list[0]
        for i, intervention_time in enumerate(self.intervention_times):
            if t >= intervention_time:
                current_r = r_list[i + 1]
        return current_r

    def dS(self, t, susceptible, infectious, r_list):
        current_r = self.get_current_r(t, r_list)
        return -1 * susceptible / self.n * (current_r / self.t_inf * infectious)

    def dE(self, t, susceptible, exposed, infectious, r_list):
        current_r = self.get_current_r(t, r_list)
        return (susceptible / self.n) * (current_r / self.t_inf * infectious) - exposed / self.t_inc

    def dI(self, exposed, infectious):
        return exposed / self.t_inc - infectious / self.t_inf

    def dR(self, infectious):
        return infectious / self.t_inf

    def system(self, y, t, r_list=None):
        susceptible, exposed, infectious, removed = y
        if r_list is None:
            r_list = [self.r0] * len(self.intervention_times)
        return [self.dS(t, susceptible, infectious, r_list),
                self.dE(t, susceptible, exposed, infectious, r_list),
                self.dI(exposed, infectious),
                self.dR(infectious)]

    def __call__(self, t, r0, r1, r2, r3, e0):
        return np.sum(self.getSEIR(t, [r0, r1, r2, r3, r1, r0], e0)[:, 1:], axis=1)

    def getSEIR(self, t, r_list, e0):
        S0, E0, I0, R0 = self.p0
        p0 = (self.n - E0 - I0 - E0, e0, I0, R0)
        return odeint(self.system, y0=p0, t=t, args=(r_list,))


if __name__ == "__main__":
    bev_de = 83019213.
    times = np.arange(0., 365., 1.0)
    r = 3.
    e0 = 0.
    p = [bev_de - 1, e0, 1., 0.]
    model = SEIR(p0=p)
    for p in model.getSEIR(times, [r, r, r, r, r], e0):
        print("{0:09.0f}\t{1:09.0f}\t{2:09.0f}\t{3:09.0f}".format(*p))
