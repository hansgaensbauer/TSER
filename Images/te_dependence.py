import matplotlib.pyplot as plt
import numpy as np

tedata = np.array([[100,2.423],
            [150,2.683],
            [200,2.67],
            [250,2.63],
            [300,2.587],
            [350,2.623],
            [400,2.599],
            [450,2.579],
            [500,2.547],
            [550,2.52],
            [600,2.427],
            [700,2.414],
            [800,2.337],
            [900,2.255],
            [1000,2.173],
            [1100,2.076],
            [1200,2.004],
            [1300,1.916],
            [1400,1.828],
            [1500,1.748],
            [1600,1.664],
            [1800,1.515],
            [2000,1.378],
            [2200,1.243],
            [2400,1.113],
            [2600,1.034],
            [3000,0.836],
            [3400,0.711],
            [3800,0.601],
            [4200,0.512],
            [4600,0.444],
            [5000,0.399],
            [5800,0.305],
            [6600,0.243]])

te_fig, ax = plt.subplots(figsize=(6,3))
ln1 = ax.plot(tedata[:,0], tedata[:,1], 'kx')
ax.set_xlabel('TE (us)')
ax.set_ylabel('Measured $T_2$ (s)')
axn = ax.twinx()
axn.set_ylabel("Equivalent Concentration ($\mu$M)")
ln2 = axn.plot(tedata[:,0], (1/tedata[:,1] - 0.4)/0.0146, color='grey')
ax.grid()
ax.legend(ln1+ln2,["Water $T_2$", "Estimated LoD"],  loc='upper center')
plt.tight_layout()
plt.show()