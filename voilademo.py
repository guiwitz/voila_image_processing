import ipywidgets as ipw
import skimage.io
import skimage.filters
import matplotlib.pyplot as plt
import numpy as np

class Improc:
    
    def __init__(self, sigma = 2):

        """Standard __init__ method.
        
        Parameters
        ----------
        
        Attributes
        ----------
        files : list
            list of imported files
            
        sigma = 2
        
        """
        
        self.sigma = sigma
        self.files = []
        self.file = ipw.FileUpload(multiple = True)
        self.select_file = ipw.Select()
        self.implot = None
        
        self.current_file = None
        
        
    def create_fig(self):
        self.fig, self.ax = plt.subplots()
        self.implot = self.ax.imshow(np.ones((100,100)))
        plt.show()
                               
    def make_import_button(self):

        output2 = ipw.Output()

        display(self.file, output2)

        self.file.observe(self.on_value_change, names='value')

        #return self.file

    def on_value_change(self, change):
        for filename in change['new'].keys():
            
            self.files.append(filename)
            
            with open(filename, "wb") as f:
                f.write(change['new'][filename]['content'])
        self.select_file.options=tuple(self.files)
        
        self.current_file = self.select_file.value
        
    def sigma_change(self, change):
        
        #if self.implot is None:
        #    self.create_fig()
        
        plt.cla()
        plt.clf()
        self.sigma = change['new']
        image = skimage.io.imread(self.select_file.value)[:,:,0]
        im_gauss = skimage.filters.gaussian(image, self.sigma, multichannel=False)
        plt.figure()
        plt.imshow(im_gauss)
        #plt.show()
        #self.fig.clear()
        #self.implot = self.ax.imshow(im_gauss)
        #plt.show()
        #self.implot.set_data(im_gauss)
        #self.implot.set_clim(vmin = 0, vmax = 255)
        #self.implot.set_extent((0, im_gauss.shape[0], im_gauss.shape[1],0))
        #print(self.implot.get_extent())
        #self.fig.canvas.draw()
        #self.fig.canvas.draw()
        plt.show()
        
    def image_processing(self, b):
        
        image = skimage.io.imread(self.select_file.value)
        im_gauss = skimage.filters.gaussian(image, self.sigma, multichannel=False)
        plt.imshow(im_gauss)
        plt.show()

        
                
                
                
                
                
                