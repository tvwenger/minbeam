import numpy as np
from minbeam import minbeam

# random seed for reproducibility
np.random.seed(1234)

# random beams
major = np.random.uniform(5.0, 10.0, 10)
minor = np.random.uniform(2.0, 5.0, 10)
pa = np.random.normal(np.pi / 2.0, np.pi / 6.0, 10)
beams = np.array([major, minor, pa]).T

# enclosing beam
enc_major, enc_minor, enc_pa = minbeam.minbeam(beams)

# plot
fig = minbeam.plot(beams)
fig.tight_layout()
fig.savefig("beam.png")
