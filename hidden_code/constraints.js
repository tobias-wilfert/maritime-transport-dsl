// GC_all_sequential_ids

var allSources = getAllNodes(['/Formalisms/WMS/WMS/Source']);
var allSinks = getAllNodes(['/Formalisms/WMS/WMS/Sink']);
var allSegments = getAllNodes(['/Formalisms/WMS/WMS/Segment']);
var allConfluences = getAllNodes(['/Formalisms/WMS/WMS/Confluence']);

var allTiles = allSources.concat(allSinks,allSegments,allConfluences)
var seenIDs = new Set();
var onlyUnique = true;
for(tile of allTiles){
    var id = int(getAttr('pId',tile));
    if(seenIDs.has(id)){
        onlyUnique = false;
        print('Double entry on id ' + id)
    }else{
        seenIDs.add(id);
    }
}
(seenIDs.size-1 == Math.max(seenIDs) - Math.min(seenIDs)) && onlyUnique 

/*
[0,1,2,3,4] --> (0,1,2,3,4)
onlyUnique == True && 5-1 == 4-0

[1,2,3,4] --> (1,2,3,4)
onlyUnique == True && 4-1 == 4-1

[-2,-1,0,1,2] --> (-2,-1,0,1,2)
onlyUnique == True && 5-1 == 2 -(-2)

[-1,0] --> (-1,0)
onlyUnique == True && 2-1 == 0-(-1)
*/
