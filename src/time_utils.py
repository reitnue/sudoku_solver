import sys
import time

class Timer():
    def __init__(self, name):
        self.name = name
        self.total_time = 0
        self.count = 0
        self.curr_start = 0
        self.times = []

    def start(self):
        self.curr_start = time.time()
        self.count += 1

    def stop(self):
        if self.curr_start == 0:
            sys.stderr.write("Timer: Error: cannot stop before start\n")
            return -1
        elapsed = time.time() - self.curr_start
        self.total_time += elapsed
        self.times.append(elapsed)
        print("{:30}: Count {:02} took {:.5f} seconds; averaging {:.5f} seconds".format(self.name, self.count, elapsed, self.total_time / self.count))
        return 0

    def summary(self):
        print("{:30} ran {} times, averageing {:.5f} seconds".format(self.name, self.count, self.total_time / self.count))


if __name__ == '__main__':
    temp = Timer("temp")
    for _ in range(2):
        temp.start()
        time.sleep(0.5)
        temp.stop()