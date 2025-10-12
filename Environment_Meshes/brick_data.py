import numpy as np

color_map = {
    "scaled_9551.stl"          : (0.9569,  0.9569,  0.9569),   #WHITE                     
    "scaled_241223(1).stl"     : (0     ,  0.2235,  0.3686),   #EARTH BLUE                
    "scaled_241223(2).stl"     : (0     ,  0.2235,  0.3686),   #EARTH BLUE                
    "scaled_303701.stl"        : (0.9569,  0.9569,  0.9569),   #WHITE                     
    "scaled_4211065.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_4548180.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_4632100(1).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_6029208(2).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_6029208(3).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_6029208(4).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_6058966.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_6061047(1).stl"    : (0.9569,  0.9569,  0.9569),   #WHITE                     
    "scaled_6061047(2).stl"    : (0.9569,  0.9569,  0.9569),   #WHITE                     
    "scaled_6170524.stl"       : (0.9569,  0.9569,  0.9569),   #WHITE                     
    "scaled_6186974.stl"       : (0     ,  0.2235,  0.3686),   #EARTH BLUE                
    "scaled_6218226(1).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0.9686,  0.8196,  0.0706),   #TR. YELLOW                
    "scaled_6251290.stl"       : (0.4980,  0.0745,  0.1059),   #NEW DARK RED              
    "scaled_6285534.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK                     
    "scaled_6329585.stl"       : (0.9569,  0.9569,  0.9569),   #WHITE                     
    "scaled_6365907(1).stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (0.9608,  0.4902,  0.1255)    #BRIGHT ORANGE             
}

position_map_end = {
    "scaled_9551.stl"          : (0.04,     0.08,       0.025),     #WHITE                     
    "scaled_241223(1).stl"     : (0.28,     0.08,       0.025),     #EARTH BLUE                
    "scaled_241223(2).stl"     : (0.44,     0.08,       0.089),     #EARTH BLUE                
    "scaled_303701.stl"        : (0.32,     0.08,       0.057),     #WHITE                     
    "scaled_4211065.stl"       : (0.48,     0.08,       0.121),     #BLACK                     
    "scaled_4548180.stl"       : (-0.12,    0.08,       0.153),     #BLACK                     
    "scaled_4632100(1).stl"    : (0.34627,  0.08,       0.15527),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (0.42627,  0.08,       0.15527),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (0.50627,  0.08,       0.15527),   #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (-0.16,    -0.131,     0.),        #BLACK                     
    "scaled_6029208(2).stl"    : (0.48,     -0.131,     0.),        #BLACK                     
    "scaled_6029208(3).stl"    : (-0.16,    0.291,      0.),        #BLACK                     
    "scaled_6029208(4).stl"    : (0.48,     0.291,      0.),        #BLACK                     
    "scaled_6058966.stl"       : (0.6,      0.08,       0.225),     #BLACK                     
    "scaled_6061047(1).stl"    : (0.08,     0.2,        0.057),     #WHITE                     
    "scaled_6061047(2).stl"    : (0.08,     -0.03975,   0.057),     #WHITE                     
    "scaled_6170524.stl"       : (-0.4,     0.08,       0.025),     #WHITE                     
    "scaled_6186974.stl"       : (0.44,     0.08,       0.153),     #EARTH BLUE                
    "scaled_6218226(1).stl"    : (-0.16,    -0.131,     0.030),     #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (-0.16,    0.291,      0.030),     #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0.48,     -0.131,     0.030),     #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0.48,     0.291,      0.030),     #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0.48,     0.08,       0.057),     #TR. YELLOW                
    "scaled_6251290.stl"       : (0.56,     0.08,       0.089),     #NEW DARK RED              
    "scaled_6285534.stl"       : (0.16,     0.08,       0.025),     #BLACK                     
    "scaled_6329585.stl"       : (-0.04,    0.08,       0.153),     #WHITE                     
    "scaled_6365907(1).stl"    : (0.16,     -0.12,      0.057),     #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (0.16,     0.28,       0.057),     #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (-0.08,    0.08,       0.057),     #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (0.6,      0.08,       0.216)      #BRIGHT ORANGE             
}

position_map_start = {
    "scaled_9551.stl"          : (0.5, 0.5, 0.0),       #WHITE                     
    "scaled_241223(1).stl"     : (1.5, 0.0, 0.0),       #EARTH BLUE                
    "scaled_241223(2).stl"     : (2.0, 0.0, 0.0),       #EARTH BLUE                
    "scaled_303701.stl"        : (0.0, 0.5, 0.0),       #WHITE                     
    "scaled_4211065.stl"       : (2.5, 0.0, 0.0),       #BLACK                     
    "scaled_4548180.stl"       : (1.0, 1.5, 0.0),       #BLACK                     
    "scaled_4632100(1).stl"    : (1.5, 1.0, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (2.0, 1.0, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (2.5, 1.0, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (1.0, 2.0, 0.0),       #BLACK                     
    "scaled_6029208(2).stl"    : (1.5, 2.0, 0.0),       #BLACK                     
    "scaled_6029208(3).stl"    : (2.0, 2.0, 0.0),       #BLACK                     
    "scaled_6029208(4).stl"    : (2.5, 2.0, 0.0),       #BLACK                     
    "scaled_6058966.stl"       : (0.5, 1.5, 0.0),       #BLACK                     
    "scaled_6061047(1).stl"    : (1.0, 0.5, 0.0),       #WHITE                     
    "scaled_6061047(2).stl"    : (1.5, 0.5, 0.0),       #WHITE                     
    "scaled_6170524.stl"       : (0.5, 1.0, 0.0),       #WHITE                     
    "scaled_6186974.stl"       : (1.0, 1.0, 0.0),       #EARTH BLUE                
    "scaled_6218226(1).stl"    : (2.0, 1.5, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (2.5, 1.5, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0.0, 2.0, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0.5, 2.0, 0.0),       #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0.5, 0.0, 0.0),       #TR. YELLOW                
    "scaled_6251290.stl"       : (1.0, 0.0, 0.0),       #NEW DARK RED              
    "scaled_6285534.stl"       : (0.0, 0.0, 0.0),       #BLACK                     
    "scaled_6329585.stl"       : (1.5, 1.5, 0.0),       #WHITE                     
    "scaled_6365907(1).stl"    : (2.0, 0.5, 0.0),       #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (2.5, 0.5, 0.0),       #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (0.0, 1.0, 0.0),       #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (0.0, 1.5, 0.0)        #BRIGHT ORANGE             
}


rotation_map_end = {
    "scaled_9551.stl"          : (0,        0,       0),        #WHITE                     
    "scaled_241223(1).stl"     : (np.pi/2,  0,       0),        #EARTH BLUE                
    "scaled_241223(2).stl"     : (np.pi/2,  0,       0),        #EARTH BLUE                
    "scaled_303701.stl"        : (-np.pi/2, 0,       0),        #WHITE                     
    "scaled_4211065.stl"       : (np.pi/2,  0,       0),        #BLACK                     
    "scaled_4548180.stl"       : (-np.pi/2, 0,       0),        #BLACK                     
    "scaled_4632100(1).stl"    : (np.pi/2,  0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (np.pi/2,  0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (np.pi/2,  0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (-np.pi/2, 0,       0),        #BLACK                     
    "scaled_6029208(2).stl"    : (-np.pi/2, 0,       0),        #BLACK                     
    "scaled_6029208(3).stl"    : (np.pi/2,  0,       0),        #BLACK                     
    "scaled_6029208(4).stl"    : (np.pi/2,  0,       0),        #BLACK                     
    "scaled_6058966.stl"       : (np.pi/2,  0,       0),        #BLACK                     
    "scaled_6061047(1).stl"    : (0,        0,       0),        #WHITE                     
    "scaled_6061047(2).stl"    : (np.pi,    0,       0),        #WHITE                     
    "scaled_6170524.stl"       : (-np.pi/2, 0,       0),        #WHITE                     
    "scaled_6186974.stl"       : (0,        0,       0),        #EARTH BLUE                
    "scaled_6218226(1).stl"    : (np.pi/2,  0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (-np.pi/2, 0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (np.pi/2,  0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (-np.pi/2, 0,       0),        #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (np.pi/2,  0,       0),        #TR. YELLOW                
    "scaled_6251290.stl"       : (0,        np.pi/2, np.pi/2),  #NEW DARK RED              
    "scaled_6285534.stl"       : (np.pi/2,  0,       0),        #BLACK                     
    "scaled_6329585.stl"       : (np.pi/2,  0,       0),        #WHITE                     
    "scaled_6365907(1).stl"    : (0,        0,       0),        #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (np.pi,    0,       0),        #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (-np.pi/2, 0,       0),        #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (-np.pi/2, 0,       0)         #BRIGHT ORANGE             
}

rotation_map_start = {
    "scaled_9551.stl"          : (0, 0, 0),     #WHITE                     
    "scaled_241223(1).stl"     : (0, 0, 0),     #EARTH BLUE                
    "scaled_241223(2).stl"     : (0, 0, 0),     #EARTH BLUE                
    "scaled_303701.stl"        : (0, 0, 0),     #WHITE                     
    "scaled_4211065.stl"       : (0, 0, 0),     #BLACK                     
    "scaled_4548180.stl"       : (0, 0, 0),     #BLACK                     
    "scaled_4632100(1).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (0, 0, 0),     #BLACK                     
    "scaled_6029208(2).stl"    : (0, 0, 0),     #BLACK                     
    "scaled_6029208(3).stl"    : (0, 0, 0),     #BLACK                     
    "scaled_6029208(4).stl"    : (0, 0, 0),     #BLACK                     
    "scaled_6058966.stl"       : (0, 0, 0),     #BLACK                     
    "scaled_6061047(1).stl"    : (0, 0, 0),     #WHITE                     
    "scaled_6061047(2).stl"    : (0, 0, 0),     #WHITE                     
    "scaled_6170524.stl"       : (0, 0, 0),     #WHITE                     
    "scaled_6186974.stl"       : (0, 0, 0),     #EARTH BLUE                
    "scaled_6218226(1).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0, 0, 0),     #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0, 0, 0),     #TR. YELLOW                
    "scaled_6251290.stl"       : (0, 0, 0),     #NEW DARK RED              
    "scaled_6285534.stl"       : (0, 0, 0),     #BLACK                     
    "scaled_6329585.stl"       : (0, 0, 0),     #WHITE                     
    "scaled_6365907(1).stl"    : (0, 0, 0),     #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (0, 0, 0),     #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (0, 0, 0),     #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (0, 0, 0)      #BRIGHT ORANGE             
}