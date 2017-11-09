import sys
import os

folder = os.path.expandvars('/home/luka/Downloads/dissect-master/src')
if folder not in sys.path:
    sys.path.append(folder)
    
from composes.semantic_space.space import Space

my_space = Space.build(data = "/home/luka/Downloads/dissect-master/src/examples/data/in/ex01.sm",
                       rows = "/home/luka/Downloads/dissect-master/src/examples/data/in/ex01.rows",
                       cols = "/home/luka/Downloads/dissect-master/src/examples/data/in/ex01.cols",
                       format = "sm")



from composes.utils import io_utils
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting

my_space = io_utils.load("/home/luka/Downloads/dissect-master/src/examples/data/out/ex01.pkl")
print my_space.cooccurrence_matrix

my_space = my_space.apply(PpmiWeighting())
print my_space.cooccurrence_matrix