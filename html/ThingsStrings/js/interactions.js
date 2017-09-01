//credit: http://stackoverflow.com/a/623770
function generateNodeSet() {
  var table = document.getElementById("results");
  var spans = table.getElementsByTagName("span");
  console.log("n spans:" + spans.length);
  var retarr = [];
  for(var i=0;i<spans.length; i++) { 
     retarr[retarr.length] = spans[i].id;
  } 
  return retarr; 
} 

function generateLinks(nodeIds) { 
  var retarr = []; 
  for(var i=0; i<nodeIds.length; i++) { 
    var id = nodeIds[i];
    var span = document.getElementById(id); 
    var atts = span.attributes; 
    var ids_str = false; 
    if((atts.getNamedItem) && (atts.getNamedItem('ids'))) { 
      ids_str = atts.getNamedItem('ids').value; 
      console.log(id + " ids=" + ids_str);
    } 
    if(ids_str) { 
      retarr[id] = ids_str.split(" ");
    }
  }
  
  return retarr; 
}

function getInteractions() {
  //alert("start drawing");
  var canvasdiv = document.getElementById("canvas");
  var spanboxdiv = document.getElementById("spanbox");
  

  nodeset = generateNodeSet(); 
  linkset = generateLinks(nodeset);
  tofromseparation = 20;

  result = {"nodes": [], "edges":[]};
  
   
  for(var key in linkset) { 
    newnode = {"id":key, "caption":document.getElementById(key).innerHTML};
    result["nodes"].push(newnode);
    console.log("working with " + key + " which has " + linkset[key].length + " connections");
    for (var i=0; i<linkset[key].length; i++) {
      fromid = key;
      toid = linkset[key][i];    
      console.log("from " + fromid + " to " + toid);
      newedge = {"source":fromid, "target":toid};
      result["edges"].push(newedge);

    } 
  }
  return result;
}
