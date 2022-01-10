import matplotlib
# from matplotlib.lines import _LineStyle
import matplotlib.pyplot as plt
import numpy as np
data = [1.064,
0.426,
0.851,
0.426,
0.426,
0.638,
0.851,
25.745,
0.213,
21.277,
1.064,
1.915,
16.170,
2.128,
4.043,
26.596,
3.617,
2.128,
0.426,
32.340,
1.064, 
0.213,
0.638,
0.851,
0.851,
0.638,
0.851,
1.702,
1.064,
0.638,
2.340,
0.213,
1.489]

tag_wind = ['K7+255', 'K17+608', 'K27+756', 'K35+374', 'K44+878', 'K49+844', 'k55+561', 'K64+732', 'K70+546',
                'K76+978', 'K84+596', 'K110+814', 'K114+915', 'K120+609', 'K124+026', 'K130+265', 'K135+191',
                'K140+767', 'K148+770', 'K155+244', 'K168+152', 'K170+903', 'K182+090', 'K187+060', 'K196+280', 
                'K209+060', 'K216+060', 'K225+101', 'K236+632', 'K241+520', 'K251+956', 'K255+190', 'K262+266' ]



data_show = []
w = 0.8
for j in range(100):
    
    data[1]+=0.25
    data[7]-=0.1
    data[9]+=0.05
    if j%2 == 0:
        data[11]+=0.05
        data[12]-=0.05
        data[15]+=0.1
        data[19]-=0.25
    plt.style.use('dark_background')

    plt.figure(figsize=(30, 5), dpi=80)

    for i in range(len(data)):
      
        if data[i]<15:
            plt.bar(tag_wind[i], data[i], color='green', width=w)
        if 15<data[i]<20:
            plt.bar(tag_wind[i], data[i], color='blue', width=w)
        if 20<data[i]<25:
            plt.bar(tag_wind[i], data[i], color='yellow', width=w)
        if 25<data[i]<30:
            plt.bar(tag_wind[i], data[i], color='orange', width=w)
        if 30<data[i]:
            plt.bar(tag_wind[i], data[i], color='red', width=w)
    plt.grid(axis = 'y', linestyle = '--', linewidth = 0.6)

    plt.yticks(np.arange(0, 48, 8))
    name = j+10
    plt.savefig("dataset_wind/"+str(name)+".jpg")
    