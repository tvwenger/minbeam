# minbeam
Given a set of ellipses (beams), `minbeam` will return the smallest-area
ellipse that encloses them all.

## Installation
Install via `pip`:
```
pip install git+https://github.com/tvwenger/minbeam.git
```
or clone the repository and install manually:
```bash
git clone https://github.com/tvwenger/minbeam.git
cd minbeam
python setup.py install
```

## Example
```python
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
```
<img src="https://raw.githubusercontent.com/tvwenger/minbeam/master/beam.png" width="45%" />

## Issues and Contributing

Please submit issues or pull requests via
[Github](https://github.com/tvwenger/minbeam).

## License and Warranty

GNU General Public License v3 (GNU GPLv3)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
