def image_1D(N=1000):

    import numpy as np    
    x = np.linspace(0,8*np.pi,N)        
    f = ((np.random.randint(0,10)*np.sin(x+np.random.randint(0,2*np.pi)) + 
    np.random.randint(0,10)*np.cos(x+np.random.randint(0,2*np.pi)) + 
    np.random.normal(0,0.2,N)))
    
    return f