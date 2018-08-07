# WikidataRevisionReporting
A proof of concept program for reporting on revisions to Wikidata data items made by a particular user.

The program is not comprehensive. It's only intended to show that you can retrieve from https://wikidata.org only data from users that you trust. 


Usage:

Using your CLI (Powershell/Terminal etc) run the program with a QID and wikidata username as parameters, e.g.:

"python wikidataRevisionsReporting.py Q11272 YULdigitalpreservation"

Prerequisites:
Python 3.x


Added a version that will write to csv. Currently writes to the same folder as the program. It only requires a QID parameter on the CLI and gives results for all users (up to 50 revisions I believe).

Usage:


"python wikidataRevisionsReporting-csv.py Q11272"
