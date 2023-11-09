from idw import IDWInterpolator
import matplotlib.pyplot as plt
import numpy as np


class Slices:
    def __init__(self, le, te, vec, npt):
        
        self.npt = int(npt + 1)
        self.pt = np.empty((self.npt, 3))
        
        for i in range(self.npt):
            self.pt[i, 0] = le[0] + i * vec[0]
            self.pt[i, 1] = le[1] + i * vec[1]
            self.pt[i, 2] = le[2] + i * vec[2]
        
    
    def get_press(self, ng, grid, press, mesh, plane):
        
        m = IDWInterpolator(int(ng), 4, int(mesh))
        
        if (int(plane) == 0):  # xy
            m.set_mesh(grid[:, 0], grid[:, 1], press)
            
        elif (int(plane) == 1): # xz
            m.set_mesh(grid[:, 0], grid[:, 2], press)
        
        p = m.eval_mesh(self.pt, plane, self.npt)
        
        return p
        
        
    def plot_press(self, press, ndata, direction, labels, xlabel, fout):
        
        colors = ['r', 'g', 'b', 'c', 'm']
        
        plt.clf()
        plt.close('all')
        plt.figure(figsize=(14, 6))
        
        for i in range(ndata):
            plt.plot(self.pt[:, int(direction[i])], press[:, i], marker='o', linestyle='-', color=colors[i], label=labels[i])
            
        plt.xlabel(xlabel)
        plt.grid(True)
        plt.legend()
        plt.savefig(fout)
        plt.close('all')
    