from openmdao.lib.datatypes.api import Int, List, Any

from openmdao.main.api import Component
from openmdao.main.interfaces import IComponent, obj_has_interface


class Mux(Component): 
    """ Takes in n inputs, and exports a length n Array 
    with the data. It is a logical multiplexer."""
    
    n = Int(2,low=2,iotype="in",desc="number of inputs to be multiplexed")
    output = List(iotype="out")
    
    def __init__(self,n=2,*args,**kwargs): 
        super(Mux,self).__init__(*args,**kwargs)
        self.n = n
        self._n_changed(n,n) #just to initialize it
        
    def _n_changed(self,old,new):
        self._inputs = []
        
        #build the inputs
        for i in xrange(new): 
            name = "input_%d"%(i+1)
            self.add_trait(name, Any(iotype="in"))
            self._inputs.append(name)
            
    def execute(self): 
        self.output = [getattr(self,inp) for inp in self._inputs]
        

class DeMux(Component): 
    """ Takes one Array input, and splits it into n indvidual outputs. This is a 
    logical demultiplexer. """

    n = Int(2,low=2,iotype="in",desc="number of items in the array to be \
    demultiplexed")
    inputs = List(iotype="in")
    
    def __init__(self,n=2,*args,**kwargs): 
        super(DeMux,self).__init__(*args,**kwargs)
        self.n = n
        self._n_changed(n,n)
        
    def _n_changed(self,old,new): 
        self._outputs = []
        
        for i in xrange(new): 
            name = "output_%d"%(i+1)
            self.add_trait(name,Any(iotype="out"))
            self._outputs.append(name)
            
    def execute(self):
        for data,out in zip(self.inputs,self._outputs): 
            setattr(self,out,data)
            