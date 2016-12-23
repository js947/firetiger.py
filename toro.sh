set -e

parallel 'python toro.py -x 1000 -o toro{}.h5 -c {}' ::: {1..5}
python run.py -on 100 -t 0.3   toro1.h5 &
python run.py -on 100 -t 0.14  toro2.h5 &
python run.py -on 100 -t 0.012 toro3.h5 &
python run.py -on 100 -t 0.05  toro4.h5 &
python run.py -on 100 -t 0.012 toro5.h5 &
wait

parallel --bar '
  python plot_1d.py toro{1}.h5 {2} -o toro{1}_{2}.pdf
' ::: {1..5} ::: density pressure velocity_x
parallel --bar '
  python plot_xt.py toro{1}.h5 density -o toro{1}_xt.pdf
' ::: {1..5}
pdfjoin toro?_*.pdf -o toro.pdf
