import random as rd

class LiftRandoms:

    def nextArrivalTime(self, maxlambda, thin_fn, cur_time):
        u = 1
        arr_time = cur_time

        while u > (thin_fn(arr_time)/maxlambda):
            arr_time += rd.expovariate(maxlambda)
            u = rd.uniform(0, 1)
        
        return arr_time

    def thinning_fn(self, x):
        day_phase, hr_phase = self.phase(x)

        if hr_phase == 'off_peak':
            return 14/225

        if day_phase == 'morning' and hr_phase == 'pre_peak':
            return 9/100
        if day_phase == 'morning' and hr_phase == 'peak':
            return 127/900
        if day_phase == 'morning' and hr_phase == 'post_peak1':
            return 1/12
        if day_phase == 'morning' and hr_phase == 'post_peak2':
            return 11/225
        
        if day_phase == 'afternoon' and hr_phase == 'pre_peak':
            return 19/150
        if day_phase == 'afternoon' and hr_phase == 'peak':
            return 167/900
        if day_phase == 'afternoon' and hr_phase == 'post_peak1':
            return 21/200
        if day_phase == 'afternoon' and hr_phase == 'post_peak2':
            return 29/600

        if day_phase == 'evening' and hr_phase == 'pre_peak':
            return 31/600
        if day_phase == 'evening' and hr_phase == 'peak':
            return 7/75
        if day_phase == 'evening' and hr_phase == 'post_peak1':
            return 3/50

    ## TODO: phase function!!
