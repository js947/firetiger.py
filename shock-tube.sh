#!/bin/bash
set -e

parallel './shock-tube.py -x 1000 -o shock-tube{}.h5 -c {}' ::: {1..5}
./run.py -on 100 -t 0.3   shock-tube1.h5 &
./run.py -on 100 -t 0.14  shock-tube2.h5 &
./run.py -on 100 -t 0.012 shock-tube3.h5 &
./run.py -on 100 -t 0.05  shock-tube4.h5 &
./run.py -on 100 -t 0.012 shock-tube5.h5 &
wait

parallel --bar '
  ./plot_1d.py shock-tube{1}.h5 {2} -o shock-tube{1}_{2}.pdf
' ::: {1..5} ::: density pressure velocity_x
parallel --bar '
  ./plot_xt.py shock-tube{1}.h5 density -o shock-tube{1}_xt.pdf
' ::: {1..5}
pdfjoin shock-tube?_*.pdf -o shock-tube.pdf
