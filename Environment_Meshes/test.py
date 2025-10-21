import numpy as np
from math import pi

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
        "pos_start": (0.75995, -0.5473, 0.05),
        "pos_end": (0.3208, 0.0008, 0.107),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "3.stl": { #NEW DARK RED
        "color": (0.4980, 0.0745, 0.1059),
        "pos_start": (0.6, -0.57453, 0.05),
        "pos_end": (0.4008, 0.0008, 0.139),
        "rot_start": (-29.915 * pi/180, 0, 0),
        "rot_end": (0, np.pi/2, np.pi/2)
    },
    "4.stl": { #EARTH BLUE
        "color": (0, 0.2235, 0.3686),
        "pos_start": (0.55536, -0.25309, 0.05),
        "pos_end": (0.1208, 0.0008, 0.075),
        "rot_start": (67.494 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "5.stl": { #EARTH BLUE
        "color": (0, 0.2235, 0.3686),
        "pos_start": (0.14783, -0.46479, 0.05,),
        "pos_end": (0.2808, 0.0008, 0.139),
        "rot_start": (190.98 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "6.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (0.23452, -0.4627, 0.05),
        "pos_end": (0.3208, 0.0008, 0.171),
        "rot_start": (-133.28 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    
    "7.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (0.44013, 0, 0.05),
        "pos_end": (0.158, 0.0008, 0.107),
        "rot_start": (48.806 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "8.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (-0.7277, 0.15, 0.05),
        "pos_end": (-0.1192, 0.0008, 0.075),
        "rot_start": (-42.022 * pi/180, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "9.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (-0.19349, 0.56355, 0.05),
        "pos_end": (-0.0792, 0.1208, 0.107),
        "rot_start": (-175.79 * pi/180, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "10.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (-0.21167, -0.59785, 0.05),
        "pos_end": (-0.0792, -0.11895, 0.107),
        "rot_start": (-5.1014 * pi/180, 0, 0),
        "rot_end": (np.pi, 0, 0)
    },
    "11.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (-0.21111, -0.43383, 0.05),
        "pos_end": (0.0008, -0.1992, 0.107),
        "rot_start": (4.3498 * pi/180, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "12.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (-0.2432, 0.70297, 0.05),
        "pos_end": (0.0008, 0.2008, 0.107),
        "rot_start": (20.098 * pi/180, 0, 0),
        "rot_end": (np.pi, 0, 0)
    },
    
    "13.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (-0.5469, 0.74508, 0.05),
        "pos_end": (-0.2392, 0.0008, 0.107),
        "rot_start": (-190.09 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "14.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (-0.46877, -0.75245, 0.05),
        "pos_end": (-0.5592, 0.0008, 0.075),
        "rot_start": (-154.47 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "15.stl": { #EARTH BLUE
        "color": (0, 0.2235, 0.3686),
        "pos_start": (0.57912, 0.19498, 0.05),
        "pos_end": (0.2808, 0.0008, 0.203),
        "rot_start": (113.43 * pi/180, 0, 0),
        "rot_end": (0, 0, 0)
    },
    "16.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.80295, -0.30272, 0.05),
        "pos_end": (0.18707, 0.0008, 0.20527),
        "rot_start": (32.713 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "17.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.59374, -0.0848, 0.05),
        "pos_end": (0.26707, 0.0008, 0.20527),
        "rot_start": (-90.826 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "18.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.49378, 0.27646, 0.05),
        "pos_end": (0.34707, 0.0008, 0.20527),
        "rot_start": (-58.469 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    
    "19.stl": { #BRIGHT ORANGE
        "color": (0.9608, 0.4902, 0.1255),
        "pos_start": (0.67258, 0.39539, 0.05),
        "pos_end": (0.4408, 0.0008, 0.266),
        "rot_start": (50.074 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "20.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (0.85733, 0.57601, 0.05),
        "pos_end": (0.4408, 0.0008, 0.275),
        "rot_start": (18.988 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "21.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (-0.48085, 0.26724, 0.05),
        "pos_end": (-0.2792, 0.0008, 0.203),
        "rot_start": (-91.016 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "22.stl": { #WHITE
        "color": (0.9569, 0.9569, 0.9569),
        "pos_start": (-0.66261, 0.30192, 0.05),
        "pos_end": (-0.1992, 0.0008, 0.203),
        "rot_start": (60.165 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "23.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (-0.7384, -0.46326, 0.05),
        "pos_end": (-0.3192, -0.2102, 0.08),
        "rot_start": (0, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "24.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (-0.74034, 0.45166, 0.05),
        "pos_end": (-0.3192, 0.2118, 0.08),
        "rot_start": (-51.12 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    
    "25.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.58453, -0.84006, 0.05),
        "pos_end": (0.3208, -0.2102, 0.08),
        "rot_start": (17.687 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "26.stl": { #COOL SILVER DRUM LACQUERED
        "color": (0.4667, 0.4667, 0.4745),
        "pos_start": (0.30067, 0.34492, 0.05),
        "pos_end": (0.3208, 0.2118, 0.08),
        "rot_start": (-88.349 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "27.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (-0.68106, -0.25906, 0.05),
        "pos_end": (-0.3192, -0.2102, 0.05),
        "rot_start": (50.215 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "28.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (-0.76188, 0.65304, 0.05),
        "pos_end": (0.3208, -0.2102, 0.05),
        "rot_start": (59.714 * pi/180, 0, 0),
        "rot_end": (-np.pi/2, 0, 0)
    },
    "29.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (0.2417, 0.52362, 0.05),
        "pos_end": (-0.3192, 0.2118, 0.05),
        "rot_start": (85.514 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    },
    "30.stl": { #BLACK
        "color": (0.0824, 0.0824, 0.0824),
        "pos_start": (0.24255, -0.6451, 0.05),
        "pos_end": (0.3208, 0.2118, 0.05),
        "rot_start": (-67.166 * pi/180, 0, 0),
        "rot_end": (np.pi/2, 0, 0)
    }
}