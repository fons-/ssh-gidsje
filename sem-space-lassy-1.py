import sys
import os

folder = os.path.expandvars('/home/luka/Downloads/dissect-master/src')
if folder not in sys.path:
    sys.path.append(folder)
    
from composes.semantic_space.space import Space

lassy_space = Space.build(data = "/home/luka/ThLi/cooccurrence/spm1.sm",
                       rows = "/home/luka/ThLi/cooccurrence/rows1.rows",
                       cols = "/home/luka/ThLi/cooccurrence/cols1.cols",
                       format = "sm")

#%%

from composes.utils import io_utils
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting

lassy_space = lassy_space.apply(PpmiWeighting())

