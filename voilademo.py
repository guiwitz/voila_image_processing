import ipywidgets as ipw
import skimage.io
import skimage.filters
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output
from notebook.notebookapp import list_running_servers


import time

class Improc:
    
    def __init__(self, sigma_min = 1, sigma_max = 5):

        """Standard __init__ method.
        
        Parameters
        ----------
        sigma_min = float
            min variance for gaussian smoothing
        sigma_max = float
            max variance for gaussian smoothing
        
        Attributes
        ----------
            
        sigma = float
            variance for gaussian smoothing
        files: list
            list of uploaded files
        current_file: str
            currently analyzed file
        imgauss: 2D numpy array
            processed image
        ax:  AxesSubplot object
        implot : AxesImage object
        
        file: upload widget
        select_file : selection widget
        sigma_slide : float slider widget
        out : output widget
        
        """
        
        self.sigma = None
        self.files = []
        self.current_file = None
        self.ax = None
        self.implot = None
        self.im_gauss = None
        
        #create widgets
        self.file = ipw.FileUpload(multiple = True)
        self.select_file = ipw.Select()
        self.sigma_slider = ipw.FloatSlider(min = sigma_min, max = sigma_max, continuous_update = False)
        self.out = ipw.Output()

        #connect widgets to actions
        self.sigma_slider.observe(self.sigma_change, names = 'value')
        self.file.observe(self.on_value_change, names='value')
        
        my_adress = next(list_running_servers())['base_url']
        self.myHTML = ipw.HTML("""<a href="https://hub.gke.mybinder.org"""+my_adress+"""notebooks/image.tif" target="_blank">Download</a>""")

   
    def on_value_change(self, change):
        for filename in change['new'].keys():
            
            self.files.append(filename)
            
            with open(filename, "wb") as f:
                f.write(change['new'][filename]['content'])
        self.select_file.options=tuple(self.files)
        
        self.current_file = self.select_file.value
       
        
    def sigma_change(self, change):
        
        #recover sigma value and do operation
        self.sigma = change['new']
        image = skimage.io.imread(self.select_file.value)
        im_gauss = skimage.filters.gaussian(image, self.sigma, multichannel=False, preserve_range = True)
        
        
        #construct or update image
        if self.ax is None:
            self.fig, self.ax = plt.subplots()#plt.gca()
            self.implot = self.ax.imshow(im_gauss)
        else:
            self.implot.set_data(im_gauss)
        
        #update output widget for voila
        with self.out:
            clear_output(wait=True)
            display(self.fig)
            
        self.im_gauss = im_gauss
            
        skimage.io.imsave('image.tif', self.im_gauss.astype(np.uint16))
            
            
    
        
  
                
                