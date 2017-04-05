# Calculate average track from set of GPS tracks

version: 1.0
date: 2017-04-03

Average Tracks is a Python port of an R script developed by Michiel Faber.
<http://www.openstreetmap.org/user/Michiel%20Faber>
The script averages a set of GPS tracks into a line of best fit.
The script assumes a directory of CSV files that contain latitude/longitude data.
The script will read the directory and find the GPS track with the most points.
That track will be the reference track for creating the average track.

For each of the remaining tracks the script will create a new set of points
equal in number to the reference track. The new points are calculated this way:
1. Assume two files: the "reference track" and an "compare track"
2. For each point in the reference track the script will determine the point
in the compare track that is closest to it (using the Pythagorean distance formula).
(Note that some points in the compare track may be used multiple times, while other points
may never be used.)
3. This process repeats for every point in the reference track.
4. The resulting set is an "updated compare track"
5. At the end, the reference track and each of the updated compare tracks are added
elementwise and then averaged by dividing by the total number of tracks.
6. The result is the new "average track."

See http://wiki.openstreetmap.org/wiki/average_tracks for additional detail.

Dependencies:

```
pandas>=0.18.1
numpy>=1.11.1
scipy>=0.18.0
```
