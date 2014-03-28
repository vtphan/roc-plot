'''
Summary: ploting ROC curves
Usage:  python roc.py data.roc.txt
Data.txt format:
Title
Series 1
sensitivities/true positive rate
specificities/1-false positive rate
Series 2
sensitivities/true positive rate
specificities/1-false positive rate
...
'''
import matplotlib.pyplot as plot
from matplotlib import legend
import sys
from numpy import arange
import argparse

x_min = 0.5
x_inc = 0.05
x_label = 'Recall'
y_min = 0.5
y_inc = 0.05
y_label = 'Precision'
scaled = False
figsize = (8,6)

def plot_roc(title, input, outfile):
   style = ['ro-', 'bs-', 'g^-', 'cD-', 'b<-', 'hm-']
   tmp = []
   leg_names = []

   ### Set up figure
   fig = plot.figure(figsize=figsize)
   ax = fig.add_subplot(111)
   if scaled:
      ax.axis('scaled')
   ax.set_title(title)
   ax.set_xlabel(x_label)
   ax.set_ylabel(y_label)
   ax.grid(True)
   ax.set_xticks(arange(int(1.0/x_inc + 1)) * x_inc)
   ax.set_yticks(arange(int(1.0/y_inc + 1)) * y_inc)
   ax.set_xlim(x_min, 1.0)
   ax.set_ylim(y_min, 1.0)


   ### Get data
   for i, d in enumerate(input):
      print 'Parsing', d[0]
      leg_names.append(d[0])
      precision_rate, recall_rate = [], []

      ### parse sensitivity
      for j in d[1].strip().split('\t'):
         try: val = float(j)
         except:
            print '\tFirst line: problem converting', j, 'to float.'
            sys.exit()
         if val < 0 or val > 1:
            print '\tFirst line: value is not proper:', val
            sys.exit()
         precision_rate.append(val)

      ### parse specificity
      for j in d[2].strip().split('\t'):
         try: val = float(j)
         except:
            print '\tSecond line: problem converting', j, 'to float.'
            sys.exit()
         if val < 0 or val > 1:
            print '\tFirst line: value is not proper:', val
            sys.exit()
         # recall_rate.append(1.0-val)
         recall_rate.append(val)

      if len(precision_rate) != len(recall_rate):
         print '\tFirst and second lines are not equal in length.'
         sys.exit()

      print '\tFinish processing', len(precision_rate), 'values of precision_rate and recall_rate.'
      tmp.append(recall_rate)
      tmp.append(precision_rate)
      tmp.append(style[i% len(style)])

   tmp.append([x_min, 1.0])
   tmp.append([y_min, 1.0])
   tmp.append('k--')
   ax.plot(*tmp)

   ### Set legend
   leg = ax.legend(leg_names, 'lower right', numpoints=1)
   for t in leg.get_texts():
      t.set_fontsize('small')
   for l in leg.get_lines():
      l.set_linewidth(0.5)

   ### Save image
   plot.savefig(outfile, format='png')
   print 'Finished.\nImage saved to', outfile


### Read file from command line input
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Plot roc curve.')
   parser.add_argument('file_name', help='file containing precision and recall values')
   parser.add_argument('-xmin', help='x_min', type=float, default=0)
   parser.add_argument('-xinc', help='x increment', type=float, default=0.1)
   parser.add_argument('-xlabel', help='x label', default=x_label)
   parser.add_argument('-ymin', help='x_min', type=float, default=0)
   parser.add_argument('-yinc', help='y increment', type=float, default=0.1)
   parser.add_argument('-ylabel', help='x label', default=y_label)
   parser.add_argument('-scaled', help='scaled x and y axes', action='store_true')
   parser.add_argument("-figsize", type=float, nargs=2, metavar=('w', 'h'),
      help='figure width and height in inches; default: %s %s.' % figsize)

   args = parser.parse_args()
   data_file = args.file_name
   x_min = args.xmin
   x_inc = args.xinc
   x_label = args.xlabel
   y_min = args.ymin
   y_inc = args.yinc
   y_label = args.ylabel
   scaled = args.scaled
   if args.figsize:
      figsize = args.figsize

   dat = []
   with open(data_file) as f:
      title = f.readline()
      print title
      end_of_file = False

      # Each data point consists of 3 lines:
      # series name
      # sensitivities
      # specificities
      while not end_of_file:
         dat.append( (f.readline(), f.readline(), f.readline()) )
         if not dat[-1][0].strip():
            dat.pop()
            end_of_file = True

      outfile = 'roc.' + sys.argv[1] + '.png'
      plot_roc(title, dat, outfile)
