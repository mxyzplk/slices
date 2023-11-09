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


    for j in range(c.nslices): # Slices loop
        s = Slices(c.le[j, :], c.te[j, :], c.vec[j, :], c.nsteps[j])
        filepath = os.path.join(c.results, "comparison_file" + str(i) + "_slice_" + str(j) + ".png")
        
        # Getting pressures for each data set
        pp = np.empty((s.npt, c.ndata))
        labels = []
        
        for k in range(c.ndata):
            if (c.press_type[k] == 0):   # Pressure on grids
                pp[:, k] = s.get_press(ps[k].ngrids, ps[k].grids, ps[k].press, c.mesh_type[k], c.plane[k])
            elif (c.press_type[k] == 1):   # Pressure on panel centers
                pp[:, k] = s.get_press(ps[k].nelements, ps[k].centers, ps[k].press, c.mesh_type[k], c.plane[k])
                
            labels.append(c.names[k])
        
        s.plot_press(pp, c.ndata, c.direction, labels, c.labels[j], filepath)
        
        
        
        
        