x = 80
y = 140

x_arriv = -170
y_arriv = 365

x_step = (x_arriv-x)/100
y_step = (y_arriv-y)/100

for i in range(100):
    x += x_step
    y += y_step
    print(i, "  ",x,y)
