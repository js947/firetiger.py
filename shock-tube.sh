#!/bin/bash
set -e

rm -f shock-tube*.h5
./shock-tube.py -x 100 -D1 -o shock-tube_1d.h5
./shock-tube.py -x 100 -D2 -o shock-tube_2d.h5

./run.py -t 0.3 shock-tube_1d.h5
./run.py -t 0.3 shock-tube_2d.h5

./slice.py shock-tube_2d.h5 -i 50 -o shock-tube_2d_slice.h5

rm -f shock-tube*.pdf
./plot_1d.py shock-tube_1d.h5 density velocity_x -o shock-tube_1d.pdf
./plot_2d.py shock-tube_2d.h5 velocity_x -o shock-tube_2d_x0.pdf -i 0
./plot_2d.py shock-tube_2d.h5 velocity_y -o shock-tube_2d_y0.pdf -i 0
./plot_2d.py shock-tube_2d.h5 velocity_x -o shock-tube_2d_x1.pdf
./plot_2d.py shock-tube_2d.h5 velocity_y -o shock-tube_2d_y1.pdf
./plot_1d.py shock-tube_2d_slice.h5 density velocity_x velocity_y -o shock-tube_slice.pdf

pdfjoin shock-tube_{1d,slice,2d_{x,y}{0,1}}.pdf -o shock-tube.pdf

exit 0


parallel './shock-tube.py -x 1000 -o shock-tube{}.h5 -c {}' ::: {1..5}
./run.py -on 100 -t 0.3   shock-tube1.h5 &
./run.py -on 100 -t 0.14  shock-tube2.h5 &
./run.py -on 100 -t 0.012 shock-tube3.h5 &
./run.py -on 100 -t 0.05  shock-tube4.h5 &
./run.py -on 100 -t 0.012 shock-tube5.h5 &
wait

./shock-tube.py -D 2 -d x -x 200 -o shock-tube_x.h5
./shock-tube.py -D 2 -d y -x 200 -o shock-tube_y.h5
./run.py -t 0.3 shock-tube_x.h5 &
./run.py -t 0.3 shock-tube_y.h5 &
wait

parallel --bar '
  ./plot_1d.py shock-tube{1}.h5 {2} -o shock-tube{1}_{2}.pdf
' ::: {1..5} ::: density pressure velocity_x
parallel --bar '
  ./plot_xt.py shock-tube{1}.h5 density -o shock-tube{1}_xt.pdf
' ::: {1..5}

./plot_2d.py shock-tube_x.h5 density -o shock-tube_x.pdf &
./plot_2d.py shock-tube_y.h5 density -o shock-tube_y.pdf &
wait

pdfjoin shock-tube_?.pdf shock-tube?_*.pdf -o shock-tube.pdf
