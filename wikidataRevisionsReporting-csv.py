import json
import urllib
import urllib.request
import sys
import os
import csv


QID = str(sys.argv[1])
out_dirname = "."

#with all content:
#wdURL = "https://www.wikidata.org/w/api.php?action=query&titles=" + QID + "&prop=revisions&rvprop=content%7Ctimestamp%7Cuser&rvlimit=50&rvslots=main&format=json"

#without all content:
wdURL = "https://www.wikidata.org/w/api.php?action=query&titles=" + QID + "&prop=revisions&rvprop=timestamp%7Cuser%7Ccomment&rvlimit=500&rvslots=main&format=json"

def wdEntityJSON(entityQID):
  wdEntityURL = "https://www.wikidata.org/wiki/Special:EntityData/" + entityQID + ".json"
  wdEntityJSONURL = urllib.request.urlopen(wdEntityURL)
  return json.load(wdEntityJSONURL)
  
  
def englishLabel(entityQID):
  return wdEntityJSON(entityQID)["entities"][entityQID]["labels"]["en"]["value"]

wikidataJSONURL = urllib.request.urlopen(wdURL)

jsonFile = json.load(wikidataJSONURL)

data = []
data.append(["Item","QID","username","timestamp","Field","Field ID","Action","Value", "Value ID"])

print("working..........")

for page in jsonFile["query"]["pages"]:
  
  for revision in jsonFile["query"]["pages"][page]["revisions"]:
    #print(str(revision))
    csvRev = []
    #get revisions that are creating new claims
    if revision["comment"].startswith('/* wbsetclaim-create:2||1 */ [[Property:'):
      propertyPID = str(revision["comment"][40:revision["comment"].find(']]',42)])
      #if making a claim that a property value is another item, look up the item and print it's english label
      if revision["comment"].find("]]: [[Q") > 1:
        assignedQID = (revision["comment"][revision["comment"].find("]]: [[Q") + 6:revision["comment"].find("]]",revision["comment"].find("]]: [[Q") + 2)])
        csvRev.append(englishLabel(QID))
        csvRev.append(QID)
        csvRev.append(revision["user"])
        csvRev.append(revision["timestamp"])
        csvRev.append(englishLabel(propertyPID))
        csvRev.append(propertyPID)
        csvRev.append("created")
        csvRev.append(englishLabel(assignedQID))
        csvRev.append(assignedQID)
        #print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' (" + propertyPID + ")" + " created as: '" + englishLabel(assignedQID) + "'" + " (" + assignedQID + ")")
      #otherwise just print the property value
      elif revision["comment"].find("]]: ") > 1:
        csvRev.append(englishLabel(QID))
        csvRev.append(QID)
        csvRev.append(revision["user"])
        csvRev.append(revision["timestamp"])
        csvRev.append(englishLabel(propertyPID))
        csvRev.append(propertyPID)
        csvRev.append("created")
        csvRev.append(revision["comment"][revision["comment"].find("]]: ") + 4: ])
        csvRev.append("none")
        #print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' (" + propertyPID + ")" + " created as: '" + revision["comment"][revision["comment"].find("]]: ") + 4: ] + "'")
      else:
        pass
          
    #get revisions that are updating claims    
    elif revision["comment"].startswith("/* wbsetclaim-update:2||1|1 */ [[Property:"):
      #print("yes")
      propertyPID = str(revision["comment"][42:revision["comment"].find(']]',4)])
        
      if revision["comment"].find("]]: [[Q") > 1:
        assignedQID = (revision["comment"][revision["comment"].find("]]: [[Q") + 6:revision["comment"].find("]]",revision["comment"].find("]]: [[Q") + 2)])
        csvRev.append(englishLabel(QID))
        csvRev.append(QID)
        csvRev.append(revision["user"])
        csvRev.append(revision["timestamp"])
        csvRev.append(englishLabel(propertyPID))
        csvRev.append(propertyPID)
        csvRev.append("updated")
        csvRev.append(englishLabel(assignedQID))
        csvRev.append(assignedQID)
       # print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' (" + propertyPID + ")" + " updated to: '" + englishLabel(assignedQID) + "'" + " (" + assignedQID + ")")
      elif revision["comment"].find("]]: ") > 1:
         
        csvRev.append(englishLabel(QID))
        csvRev.append(QID)
        csvRev.append(revision["user"])
        csvRev.append(revision["timestamp"])
        csvRev.append(englishLabel(propertyPID))
        csvRev.append(propertyPID)
        csvRev.append("updated")
        csvRev.append(revision["comment"][revision["comment"].find("]]: ") + 4: ])
        csvRev.append("none")
        #print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' (" + propertyPID + ")" + " updated to: '" + revision["comment"][revision["comment"].find("]]: ") + 4:] + "'")
      else:
        pass
      
    #get revisions that are creating aliases
    elif revision["comment"].startswith("/* wbsetaliases-add:1|en */"):
      csvRev.append(englishLabel(QID))
      csvRev.append(QID)
      csvRev.append(revision["user"])
      csvRev.append(revision["timestamp"])
      csvRev.append("Alias")
      csvRev.append("none")
      csvRev.append("created")
      csvRev.append(revision["comment"][28:])
      csvRev.append("none")
      #print(revision["timestamp"] + ": Alias created as: '" + revision["comment"][28:] + "'")
      
    else:
      pass
    if len(csvRev) > 1:
      data.append(csvRev) 
    else:
      pass
#write out csv file
print("Done! Writing csv file..........")       
with open(os.path.join(out_dirname, "recentEditsTo" + QID + ".csv"), 'w',newline='') as outputFile:
  a = csv.writer(outputFile, delimiter=',')
  a.writerows(data)
outputFile.close()     
