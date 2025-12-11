import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2
ALPHA = 7.2973525693e-3
V0 = abs(np.log(ALPHA)) / (PHI ** 2)
C_ALPHA_SCAR = V0 / (PHI ** 2)
LAMBDA_STERILE = 6.18034e-9
PHI_MIN_TARGET = 1e-14
