from config import Config
from surface import Surface
from plotslices import Slices
import numpy as np
import os

config_file = "config.txt"

# Initialization config object
c = Config(config_file)

# Reading Slices
c.read_slices()

# Reading pressures
for i in range(c.np):   # Pressure files loop

    ps = []
    for j in range(c.ndata): # Data set loops
        p = Surface(c.mesh_type[j])
        p.read_grids(c.data_dir[j], c.grids_files[j])
        p.read_elements(c.data_dir[j], c.elements_files[j])
        p.read_press(c.data_dir[j], c.press_files[i][j], c.press_type[j])
        ps.append(p)


    for i in range(c.nslices): # Slices loop
        s = Slices(c.le[i, :], c.te[i, :], c.vec[i, :], c.nsteps[i])
        filepath = os.path.join(c.results, "comparison_" + str(i) + ".png")
        
        # Getting pressures for each data set
        pp = np.empty((s.npt + 1, c.ndata))
        labels = []
        
        for j in range(c.ndata):
            if (c.press_type == 0):   # Pressure on grids
                pp[:, j] = s.get_press(ps[j].ngrids, ps[j].grids, ps[j].press, c.mesh_type[j])
            elif (c.press_type == 1):   # Pressure on panel centers
                pp[:, j] = s.get_press(ps[j].nelements, ps[j].centers, ps[j].press, c.mesh_type[j])
                
            labels.append(c.names[j])
        
        s.plot_press(pp, c.ndata, c.direction, labels, c.labels[i], filepath)
        
        
        
        
        