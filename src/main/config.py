# -*- coding: utf-8 -*-
import yaml
import os
import numpy as np

class Config:
    def __init__(self, filename):

        # directories
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.main_dir, '../resources')
        self.results = os.path.join(self.main_dir, '../results')
        self.configpath = os.path.join(self.resources_dir, filename)        
        
        with open(self.configpath, 'r') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
            
        # Number of data sets
        self.ndata = len(self.data)

        self.group_names = []
        
        for group_name, group_data in self.data.items():
            self.group_names.append(group_name)   
        
        # Number of pressure files
        self.np = len(self.data[self.group_names[0]]['files'])
            
        # Declaring variables
        self.names = []
        self.grids_files = []
        self.elements_files = []
        self.mesh_type = []
        self.press_type = []
        self.data_dir = []
        self.press_files = []
        self.plane = []
        self.direction = []
            
        for i in range(self.ndata):
            self.names.append(self.data[self.group_names[i]]['name'])
            self.grids_files.append(self.data[self.group_names[i]]['grids'])
            self.elements_files.append(self.data[self.group_names[i]]['elements'])
            self.mesh_type.append(self.data[self.group_names[i]]['mesh_type'])
            self.press_type.append(self.data[self.group_names[i]]['press_type'])
            self.data_dir.append(self.data[self.group_names[i]]['data_dir'])
            self.plane.append(self.data[self.group_names[i]]['plane'])
        

        for i in range(self.np):
            temp = []
            for j in range(self.ndata):
                temp.append(self.data[self.group_names[j]]['files'][i])
            self.press_files.append(temp)
            

    def read_slices(self):
        
        filepath = os.path.join(self.resources_dir, "slices.txt")
        
        with open(filepath, 'r') as file:
            line = file.readline()
            temp = line.split()
            
            self.nslices = int(temp[0])
            self.le = np.empty((self.nslices, 3))
            self.te = np.empty((self.nslices, 3))
            self.vec = np.empty((self.nslices, 3))
            self.nsteps = np.empty(self.nslices)
            self.labels = []
            
            for i in range(self.nslices):
            
                line = file.readline()
                temp = line.split()
                
                self.labels.append(temp[8])
                self.direction.append(temp[7])
                
                for j in range(3):
                    self.le[i, j] = float(temp[j])
                    self.te[i, j] = float(temp[j + 3])
                
                self.nsteps[i] = float(temp[6])
                
                self.vec[i, :] = (self.te[i, :] - self.le[i, :]) / self.nsteps[i]
            
        
        
