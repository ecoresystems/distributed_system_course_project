import time

start_time = time.time()

for i in range(10000):
    print(i)
eof = time.time()-start_time
print(eof)
print(type(eof))