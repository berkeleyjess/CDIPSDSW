import pandas as pd
import numpy as np
import csv as csv

results = pd.read_csv('output_guesses.csv', header=0)

n_clicked_predicted=0
n_clicked_missed=0
n_notclicked_predicted=0
n_notclicked_missed=0

for x in xrange(len(results['id'])):
    if results['did_click'][x]==True:
        if results['will_click'][x]==True: n_clicked_predicted+=1
        else: n_clicked_missed+=1
    else:
        if results['will_click'][x]==False: n_notclicked_predicted+=1
        else: n_notclicked_missed+=1

print "Fraction of clicks predicted:", float(n_clicked_predicted)/(n_clicked_missed+n_clicked_predicted)
print "Fraction of non-clicks predicted:", float(n_notclicked_predicted)/(n_notclicked_missed+n_notclicked_predicted)

