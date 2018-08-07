import json
import urllib
import urllib.request
import sys



QID = str(sys.argv[1])
username = str(sys.argv[2])

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

for page in jsonFile["query"]["pages"]:
  print("Item: " + englishLabel(jsonFile["query"]["pages"][page]["title"]))
  print("Changes made:")
  for revision in jsonFile["query"]["pages"][page]["revisions"]:
    #print(str(revision))
    if revision["user"] == username:
     
     #get revisions that are creating new claims
      if revision["comment"].startswith('/* wbsetclaim-create:2||1 */ [[Property:'):
        propertyPID = str(revision["comment"][40:revision["comment"].find(']]',42)])
        #if making a claim that a property value is another item, look up the item and print it's english label
        if revision["comment"].find("]]: [[Q") > 1:
          assignedQID = (revision["comment"][revision["comment"].find("]]: [[Q") + 6:revision["comment"].find("]]",revision["comment"].find("]]: [[Q") + 2)])
          print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' created as: " + englishLabel(assignedQID))
        #otherwise just print the property value
        elif revision["comment"].find("]]: ") > 1:
         
          print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' created as: " + revision["comment"][revision["comment"].find("]]: ") + 4: ])
        else:
          pass
          
      #get revisions that are updating claims    
      elif revision["comment"].startswith("/* wbsetclaim-update:2||1|1 */ [[Property:"):
        #print("yes")
        propertyPID = str(revision["comment"][42:revision["comment"].find(']]',4)])
        
        if revision["comment"].find("]]: [[Q") > 1:
          assignedQID = (revision["comment"][revision["comment"].find("]]: [[Q") + 6:revision["comment"].find("]]",revision["comment"].find("]]: [[Q") + 2)])
          print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' updated to: " + englishLabel(assignedQID))
        elif revision["comment"].find("]]: ") > 1:
         
          print(revision["timestamp"] + ": '" + englishLabel(propertyPID) + "' updated to: " + revision["comment"][revision["comment"].find("]]: ") + 4:])
        else:
          pass
      
      elif revision["comment"].startswith("/* wbsetaliases-add:1|en */"):
        print(revision["timestamp"] + ": Alias created as: " + revision["comment"][28:])
      
      else:
        pass
     
