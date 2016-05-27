#File to test capabilities of Bokeh
# - James Varags-Witherell
from bokeh.io import output_file, show, vplot, gridplot
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.sampledata.autompg import autompg as df

output_file("testPlots.html")

#data set: change range to change number of plot points
x = list(range(5))
y0 = x

# create a new plot
s1 = figure(width=250, plot_height=250, title=None)
s1.circle(x, y0, size=10, color="navy", alpha=0.5)
gList = []
#plots are put into a 2x2 grid format. 0-10 means 22 plots
#to test other numbers of plots, simply change the end range to 1/2 of the desired number
#for i in range (1):
#    if i == 0:
#    	#each plot seems to need to be named differently to be graphed properly
#    	#exec calls are a method for procedurally generating variable names 
#        exec("g%d = s1" % i)
#        exec("g%d = s1" % (i+1))
#        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % i)
#        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+1))
#        exec("gList.append([g%d, g%d])" % (i , (i+1)))
#    else:
#        exec("g%d = s1" % (i+2))
#        exec("g%d = s1" % (i+3))
#        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+2))
#        exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+3))
#        exec("gList.append([g%d, g%d])" % ((i+2) , (i+3)))
# put all the plots in a VBox
i = 1
exec("g%d = s1" % i)
exec("g%d = s1" % (i+1))
exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % i)
exec("g%d.circle(x, y0, size=10, color=\"navy\", alpha=0.5)" % (i+1))
exec("gList.append([g%d, g%d])" % (i , (i+1)))
p = gridplot(gList)

# show the results
show(p)
#code is a mixture of my own + tutorials on the website.