# Now hosted at github: https://github.com/riivo/pwum #

## Finding frequent patterns from Apache Log files ##

This project provides alternative methods to analyse web access log files, focusing on usage mining and providing information how to make web site more accessible. This tool helps you to gain insight into what users are looking for and how quick they are finding it.

We provide solution to extract user sessions from apache log files (currently CLF format is supported). With user sessions following analysis is done:

  * Frequent patterns i.e. frquent combination of visited pages in sessions are found using apriori algorithm.

  * Timing information is provided for these patterns  to find elements (pages) in the path that are used only as a way to access a desired information (and ideally should be deleted).

  * Access patterns are clustered into use cases based on similarity.

  * Also, we provide a wat to study how usage patterns change in time.



Current solution is implemented in Python 2.5. Please note that the project is not under active development.

You can find the source code for the  [python clickstream analysis](https://github.com/riivo/pwum) at github https://github.com/riivo/pwum
