# minbeam
Given a set of ellipses (beams), `minbeam` will return the smallest
area ellipse that encloses them all.

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

## Usage
The `minbeam` package supplies two functions: `minbeam` and `plot`.

The `minbeam` function returns the major axis, minor axis, and
position angle of the smallest area ellipse that encloses several
ellipses. The set of ellipses are defined by their major axes,
minor axes, and position angles (radians). For example:
```python
import numpy as np
from minbeam import minbeam
beams = [
    [10.0, 5.0, np.pi/2.0], # major, minor, pa of beam 1
    [8.0, 7.0, np.pi/4.0], # major, minor, pa of beam 2
]
# major axis, minor axis, and position angle (radians) of enclosing
# ellipse
major, minor, pa = minbeam.minbeam(beams)
```

The `plot` function returns a `matplotlib.Figure` containing a plot
of the set of ellipses and the enclosing ellipse. For example, using
`beams` defined above:
```python
fig = minbeam.plot(beams)
fig.show()
```
By default, the position angle is defined as zero along the positive
x-axis. This can be changed via the `zero_pa` argument. For example,
if position angle is defined as zero along the positive y-axis, then:
```python
fig = minbeam.plot(beams, zero_pa="+y")
fig.show()
```
Possible values are `+x` (default), `+y`, `-x`, and `-y`.

## Example
```python
import numpy as np
from minbeam import minbeam

# random seed for reproducibility
np.random.seed(1234)

# random major axis
major = np.random.uniform(5.0, 10.0, 10)
# random minor axis
minor = np.random.uniform(2.0, 5.0, 10)
# random position angle
pa = np.random.normal(np.pi / 2.0, np.pi / 6.0, 10)
beams = np.array([major, minor, pa]).T

# enclosing beam
enc_major, enc_minor, enc_pa = minbeam.minbeam(beams)

# plot beams with position angle defined as zero along +y axis.
fig = minbeam.plot(beams, zero_pa='+y')
fig.tight_layout()
fig.savefig("beam.png")
```
<img src="https://raw.githubusercontent.com/tvwenger/minbeam/master/beam.png" width="60%" />

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
