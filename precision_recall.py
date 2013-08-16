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

x_lim = [0.86,1.0]
y_lim = [0.86, 1.0]

def plot_roc(title, input, outfile):
   style = ['ro-', 'bs-', 'g^-', 'cD-', 'b<-', 'hm-']
   tmp = []
   leg_names = []
   # ticks = arange(11) * 0.1
   ticks = arange(11) * 0.02 + 0.8
   print ticks

   ### Set up figure
   fig = plot.figure()
   ax = fig.add_subplot(111)
   ax.axis('scaled')
   ax.set_title(title)
   ax.set_xlabel('Recall')
   ax.set_ylabel('Precision')
   ax.grid(True)
   ax.set_xticks(ticks)
   ax.set_yticks(ticks)
   ax.set_xlim(*x_lim)
   ax.set_ylim(*y_lim)


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

   tmp.append(x_lim)
   tmp.append(y_lim)
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
   if len(sys.argv) != 2:
      print 'give a filename.'
   else:
      dat = []

      with open(sys.argv[1]) as f:
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
