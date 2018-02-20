reset
n=40 #number of intervals
max=500 #max value
min=300 #min value
width=(max-min)/n #interval width
#function used to map a value to the intervals
hist(x,width)=width*floor(x/width)+width/2.0
set term pngcairo #output terminal and file
system("mkdir -p plots")
set output "plots/freefall_time_histogram.png"
set xrange [min:max]
set yrange [0:]
#to put an empty boundary around the
#data inside an autoscaled graph.
set offset graph 0.05,0.05,0.05,0.0
set xtics min,(max-min)/5,max
set boxwidth width*0.9
set style fill solid 0.5 #fillstyle
set tics out nomirror
set xlabel "Time [ms]"
set ylabel "Frequency"
#count and plot
set table 'hist_freefall_time.txt'
plot "freefall.txt" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb "green" t "Time"
unset table
Gauss(x) = a/(sigma*sqrt(2*pi)) * exp( -(x-mu)**2 / (2*sigma**2) )
a = 100.
mu = 400.
sigma = 10.
set fit err
fit Gauss(x) 'hist_freefall_time.txt' u 1:2 via a,mu,sigma
set label 1 sprintf("{/Symbol m} = %3.1f +/- %3.1f ms",mu,mu_err) at 300,3 font "arialbd,18"
set label 2 sprintf("{/Symbol s} = %3.1f +/- %3.1f ms",sigma,sigma_err) at 300,2.8 font "arialbd,18"
set label 3 sprintf("L = %3.1f +/- %3.1f cm",0.5* 9.806 * mu * mu / (10000), 2 * (mu_err/mu) * 0.5* 9.806 * mu * mu / (10000)) at 300,3.3 font "arialbd,18"
plot "freefall.txt" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb "green" t "Time", Gauss(x) w lines ls 2 lw 2 t "Fit"
