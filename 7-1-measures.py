import RPi.GPIO as g
import time
import matplotlib.pyplot as plt
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
g.setmode(g.BCM)
g.setup(dac, g.OUT)
g.setup(troyka, g.OUT, initial = g.HIGH)
g.setup(comp, g.IN)
def d2b(n):
    return [int(x) for x in bin(n)[2:].zfill(8)]
def adc():
    a = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        a[i] = 1
        g.output(dac, a)
        v = int("".join([str(x) for x in a]), 2) / 256 * 3.3
        time.sleep(0.01)
        if g.input(comp) == 0:
            a[i] = 0
    return [a, v]
    


mesurement = []
x = []
counter = 1
start_time = time.time()
flag = 0
with open('data.txt', 'w') as data:

    try:
        while True:
            a = adc()
            
            value = int("".join([str(x) for x in a[0]]), 2)
            bin_val = a[0]
            voltage = a[1]
            data.write(str(value) + '\n')
            if voltage >= 3.3 * 0.97:
                g.setup(troyka ,g.OUT, initial = 0)
                flag = 1
            print("Value = {:^3} -> {}, voltage = {:.2f}".format(int("".join([str(x) for x in a[0]]), 2), a[0], a[1]))
            mesurement.append(voltage)
            x.append(counter)
            counter += 1
            if voltage <= 3.3 * 0.02 and flag:
                end_time = time.time()
                break
    finally:
        g.output(dac, 0)
        g.output(troyka, 0)
        g.cleanup()

exp_time = end_time - start_time
with open ('settings.txt', 'w') as settings:
    settings.write(f'Период: {exp_time}' + '\n')
    settings.write(f'Частота: {exp_time/ len(mesurement)}'+'n')
    settings.write(f'Квантование: {3.3 / 255}')
print(exp_time)
plt.plot(x, mesurement)
plt.show()
