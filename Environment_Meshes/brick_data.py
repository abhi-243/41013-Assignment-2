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
    "scaled_9551.stl"          : (-0.1192,    0.0008,     0.075),     #WHITE                     
    "scaled_241223(1).stl"     : (0.1208,     0.0008,     0.075),     #EARTH BLUE                
    "scaled_241223(2).stl"     : (0.2808,     0.0008,     0.139),     #EARTH BLUE                
    "scaled_303701.stl"        : (0.1608,     0.0008,     0.107),     #WHITE                     
    "scaled_4211065.stl"       : (0.3208,     0.0008,     0.171),     #BLACK                     
    "scaled_4548180.stl"       : (-0.2792,    0.0008,     0.203),     #BLACK                     
    "scaled_4632100(1).stl"    : (0.18707,    0.0008,     0.20527),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (0.26707,    0.0008,     0.20527),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (0.34707,    0.0008,     0.20527),   #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (-0.3192,   -0.2102,     0.05),      #BLACK                     
    "scaled_6029208(2).stl"    : (0.3208,    -0.2102,     0.05),      #BLACK                     
    "scaled_6029208(3).stl"    : (-0.3192,    0.2118,     0.05),      #BLACK                     
    "scaled_6029208(4).stl"    : (0.3208,     0.2118,     0.05),      #BLACK                     
    "scaled_6058966.stl"       : (0.4408,     0.0008,     0.275),     #BLACK                     
    "scaled_6061047(1).stl"    : (-0.0792,    0.1208,     0.107),     #WHITE                     
    "scaled_6061047(2).stl"    : (-0.0792,   -0.11895,    0.107),     #WHITE                     
    "scaled_6170524.stl"       : (-0.5592,    0.0008,     0.075),     #WHITE                     
    "scaled_6186974.stl"       : (0.2808,     0.0008,     0.203),     #EARTH BLUE                
    "scaled_6218226(1).stl"    : (-0.3192,   -0.2102,     0.08),      #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (-0.3192,    0.2118,     0.08),      #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0.3208,    -0.2102,     0.08),      #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0.3208,     0.2118,     0.08),      #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0.3208,     0.0008,     0.107),     #TR. YELLOW                
    "scaled_6251290.stl"       : (0.4008,     0.0008,     0.139),     #NEW DARK RED              
    "scaled_6285534.stl"       : (0.0008,     0.0008,     0.075),     #BLACK                     
    "scaled_6329585.stl"       : (-0.1992,    0.0008,     0.203),     #WHITE                     
    "scaled_6365907(1).stl"    : (0.0008,    -0.1992,     0.107),     #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (0.0008,     0.2008,     0.107),     #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (-0.2392,    0.0008,     0.107),     #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (0.4408,     0.0008,     0.266)      #BRIGHT ORANGE             
}

position_map_start = {
    "scaled_9551.stl"          : (0.5, 0.5, 0.05),       #WHITE                     
    "scaled_241223(1).stl"     : (1.5, 0.0, 0.05),       #EARTH BLUE                
    "scaled_241223(2).stl"     : (2.0, 0.0, 0.05),       #EARTH BLUE                
    "scaled_303701.stl"        : (0.0, 0.5, 0.05),       #WHITE                     
    "scaled_4211065.stl"       : (2.5, 0.0, 0.05),       #BLACK                     
    "scaled_4548180.stl"       : (1.0, 1.5, 0.05),       #BLACK                     
    "scaled_4632100(1).stl"    : (1.5, 1.0, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (2.0, 1.0, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (2.5, 1.0, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (1.0, 2.0, 0.05),       #BLACK                     
    "scaled_6029208(2).stl"    : (1.5, 2.0, 0.05),       #BLACK                     
    "scaled_6029208(3).stl"    : (2.0, 2.0, 0.05),       #BLACK                     
    "scaled_6029208(4).stl"    : (2.5, 2.0, 0.05),       #BLACK                     
    "scaled_6058966.stl"       : (0.5, 1.5, 0.05),       #BLACK                     
    "scaled_6061047(1).stl"    : (1.0, 0.5, 0.05),       #WHITE                     
    "scaled_6061047(2).stl"    : (1.5, 0.5, 0.05),       #WHITE                     
    "scaled_6170524.stl"       : (0.5, 1.0, 0.05),       #WHITE                     
    "scaled_6186974.stl"       : (1.0, 1.0, 0.05),       #EARTH BLUE                
    "scaled_6218226(1).stl"    : (2.0, 1.5, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (2.5, 1.5, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0.0, 2.0, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0.5, 2.0, 0.05),       #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0.5, 0.0, 0.05),       #TR. YELLOW                
    "scaled_6251290.stl"       : (1.0, 0.0, 0.05),       #NEW DARK RED              
    "scaled_6285534.stl"       : (0.0, 0.0, 0.05),       #BLACK                     
    "scaled_6329585.stl"       : (1.5, 1.5, 0.05),       #WHITE                     
    "scaled_6365907(1).stl"    : (2.0, 0.5, 0.05),       #BRIGHT ORANGE             
    "scaled_6365907(2).stl"    : (2.5, 0.5, 0.05),       #BRIGHT ORANGE             
    "scaled_6365908.stl"       : (0.0, 1.0, 0.05),       #BRIGHT ORANGE             
    "scaled_6370526.stl"       : (0.0, 1.5, 0.05)        #BRIGHT ORANGE             
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