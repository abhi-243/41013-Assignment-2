import numpy as np

stl_data = {
    "1.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (0.0, 0.0, 0.05),
        "pos_end": (0.0008, 0.0008, 0.075),
        "rot_start": (np.pi/2, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "2.stl": { #TR. YELLOW
        "color": (0.9686, 0.8196, 0.0706),
        "pos_start": (0.5, 0.0, 0.05),
        "pos_end": (0.3208, 0.0008, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "3.stl": { #NEW DARK RED
        "color": (0.4980, 0.0745, 0.1059),
        "pos_start": (1.0, 0.0, 0.05),
        "pos_end": (0.4008, 0.0008, 0.139),
        "rot_start": (0, 0, 0),
        "rot_end": (0, np.pi/2, np.pi/2)
    },
    "4.stl": { #EARTH BLUE
        "color": (0, 0.2235, 0.3686),
        "pos_start": (1.5, 0.0, 0.05),
        "pos_end": (0.1208, 0.0008, 0.075),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "5.stl": { #EARTH BLUE
        "color": (0, 0.2235, 0.3686),
        "pos_start": (2.0, 0.0, 0.05),
        "pos_end": (0.2808, 0.0008, 0.139),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "6.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (2.5, 0.0, 0.05),
        "pos_end": (0.3208, 0.0008, 0.171),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    
    "7.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (0.0, 0.5, 0.05),
        "pos_end": (0.1608, 0.0008, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "8.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (0.5, 0.5, 0.05),
        "pos_end": (-0.1192, 0.0008, 0.075),
        "rot_start": (0, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "9.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (1.0, 0.5, 0.05),
        "pos_end": (-0.0792, 0.1208, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "10.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (1.5, 0.5, 0.05),
        "pos_end": (-0.0792, -0.11895, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi, 0, 0)
    },
    "11.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (2.0, 0.5, 0.05),
        "pos_end": (0.0008, -0.1992, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "12.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (2.5, 0.5, 0.05),
        "pos_end": (0.0008, 0.2008, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi, 0, 0)
    },
    
    "13.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (0.0, 1.0, 0.05),
        "pos_end": (-0.2392, 0.0008, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "14.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (0.5, 1.0, 0.05),
        "pos_end": (-0.5592, 0.0008, 0.075),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "15.stl": { #EARTH BLUE
        "color": (0, 0.2235, 0.3686),
        "pos_start": (1.0, 1.0, 0.05),
        "pos_end": (0.2808, 0.0008, 0.203),
        "rot_start": (0, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "16.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (1.5, 1.0, 0.05),
        "pos_end": (0.18707, 0.0008, 0.20527),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "17.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (2.0, 1.0, 0.05),
        "pos_end": (0.26707, 0.0008, 0.20527),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "18.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (2.5, 1.0, 0.05),
        "pos_end": (0.34707, 0.0008, 0.20527),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    
    "19.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (0.0, 1.5, 0.05),
        "pos_end": (0.4408, 0.0008, 0.266),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "20.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (0.5, 1.5, 0.05),
        "pos_end": (0.4408, 0.0008, 0.275),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "21.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (1.0, 1.5, 0.05),
        "pos_end": (-0.2792, 0.0008, 0.203),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "22.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (1.5, 1.5, 0.05),
        "pos_end": (-0.1992, 0.0008, 0.203),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "23.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (2.0, 1.5, 0.05),
        "pos_end": (-0.3192, -0.2102, 0.08),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "24.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (2.5, 1.5, 0.05),
        "pos_end": (-0.3192, 0.2118, 0.08),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    
    "25.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.0, 2.0, 0.05),
        "pos_end": (0.3208, -0.2102, 0.08),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "26.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.5, 2.0, 0.05),
        "pos_end": (0.3208, 0.2118, 0.08),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "27.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (1.0, 2.0, 0.05),
        "pos_end": (-0.3192, -0.2102, 0.05),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "28.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (1.5, 2.0, 0.05),
        "pos_end": (0.3208, -0.2102, 0.05),
        "rot_start": (0, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "29.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (2.0, 2.0, 0.05),
        "pos_end": (-0.3192, 0.2118, 0.05),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "30.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (2.5, 2.0, 0.05),
        "pos_end": (0.3208, 0.2118, 0.05),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    }
}