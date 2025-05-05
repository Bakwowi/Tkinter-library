from line_profiler import profile
# from memory_profiler import *

@profile
def sum(num):
    return num * (num + 1) // 2

print(sum(10000))
