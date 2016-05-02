from bokeh.io import output_file, show, vplot, gridplot
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.sampledata.autompg import autompg as df

output_file("testPlots.html")

x = list(range(1000))
y0 = x

# create a new plot
s1 = figure(width=250, plot_height=250, title=None)
s1.circle(x, y0, size=10, color="navy", alpha=0.5)
gList = []
for i in range (0, 10):
    if i == 0:
        exec("g%d = s1" % i)
        exec("g%d = s1" % (i+1))
        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % i)
        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+1))
        exec("gList.append([g%d, g%d])" % (i , (i+1)))
    else:
        exec("g%d = s1" % (i+2))
        exec("g%d = s1" % (i+3))
        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+2))
        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+3))
        exec("gList.append([g%d, g%d])" % ((i+2) , (i+3)))
# put all the plots in a VBox
p = gridplot(gList)

# show the results
show(p)