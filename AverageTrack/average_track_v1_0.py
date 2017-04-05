import pandas as pd
import glob, os
import csv
import numpy as np
from scipy.spatial import distance

#used to set float precision when displaying data
#float precision when exporting to csv is handled by pandas to_csv method
#np.set_printoptions(precision=6)        

in_dir = '[your input directory. code assumes that it will read all csv files in this directory]'
out_dir = '[your output directory]'

files_processed = 0
longest_track = ''
most_rows = 0

os.chdir(in_dir)
for file in glob.glob("*.csv"):
    row_count = (sum(1 for row in open(file))) -1
    if row_count > most_rows:
        most_rows = row_count
        longest_track = file
    files_processed +=1

print('Finished reading %d files' % (files_processed))
print('Longest track is %s' % (longest_track))
print('Length of track is %d data points' % (most_rows))

#create dataframe to hold lat/lon data for reference track, i.e., track with most points
pd_ref = pd.read_csv(in_dir + longest_track)  

#source for the distance algorithm found here:
#http://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points

#need to split dataframe into two arrays. the scipy distance method can't parse dataframes.
arr_lat = np.array(pd_ref['Lat'])
arr_lon = np.array(pd_ref['Lon'])

os.chdir(in_dir)
for file in glob.glob("*.csv"):
    if file != longest_track:
        #nothing fancy here; code assumes a csv of two columns and a header
        tmp = pd.read_csv(file)
        tmp.columns = ['Lat', 'Lon']
        a = list(tmp['Lat'])
        b = list(tmp['Lon'])
        c=list(zip(a,b))
        output = []
        for i in range(0,most_rows):
            ref_point = (pd_ref.ix[i]['Lat'],pd_ref.ix[i]['Lon'])
            output.append(c[distance.cdist([ref_point], c).argmin()])
        list1, list2 = zip(*output)
        #sum latitudes/longitudes
        arr_lat = arr_lat + list1
        arr_lon = arr_lon + list2

#find average lat/lon for each point
arr_lat = arr_lat / (files_processed)
arr_lon = arr_lon / (files_processed)

#create dataframe of average track data, mostly for ease in exporting to csv
pd_avg_track = pd.DataFrame(list(zip(arr_lat, arr_lon)))
pd_avg_track.rename(columns={0:'Lat', 1:'Lon'}, inplace=True)  

pd_avg_track.to_csv(out_dir + 'avg_track.csv', index=False, float_format='%0.6f')

print('All done!')