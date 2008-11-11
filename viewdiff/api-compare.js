showingDetails = new Array();

function hideShowing() {
   var i;
   for (i in showingDetails)
	  showingDetails[i].style.display = 'none';
}

function getDetailsTable(obj) {
   if (!obj)
	  return null;
   var collection = obj.getElementsByClassName("accDetails");
   if (collection.length == 0)
	  return null;
   return collection[0];
}

function showDetails(obj) {
   obj = obj.parentNode.parentNode
   var details = getDetailsTable(obj);
   if (!details)
	  return;
   var parallel = getDetailsTable(getParallelObj(obj));   
   if (details.style.display == 'table') {
      details.style.display = 'none';
	  if (parallel)
		 parallel.style.display = 'none';
	  showingDetails = new Array();
   } else {
	  hideShowing();
	  details.style.display = 'table';
	  showingDetails[0] = details;
	  if (parallel) {
		 parallel.style.display = 'table';
		 showingDetails[1] = parallel;
	  }
   }
}

function onTreeFocus(obj) {
   var classStr = obj.getAttribute("class").replace(/(.*)focus/, "$1");
   obj.setAttribute("class", classStr+" focus");
   var id = obj.getAttribute("aria-activedescendant");
   setActiveDescendant(obj, id);
}

function OnTreeBlur(obj) {
   var classStr = obj.getAttribute("class").replace(/\sfocus/g, "");
   obj.setAttribute("class", classStr);
   var id = obj.getAttribute("aria-activedescendant");
   var descendant = document.getElementById(id+"Title");
   unhighlightNode(descendant);   
}

function getNextNodeId(obj) {
   var current_id = obj.getAttribute("aria-activedescendant");
   var nodes_depth = obj.getElementsByClassName("treeNode");
   var i;
   for (i=0;i<nodes_depth.length-1;i++)
	  if (nodes_depth[i].id == current_id)
		 return nodes_depth[i+1].id;
   return '';
}

function getPrevNodeId(obj) {
   var current_id = obj.getAttribute("aria-activedescendant");
   var nodes_depth = obj.getElementsByClassName("treeNode");
   var i;
   for (i=1;i<nodes_depth.length;i++)
	  if (nodes_depth[i].id == current_id)
		 return nodes_depth[i-1].id;
   return '';
}

function setActiveDescendant(container, id) {
   var current_id = container.getAttribute("aria-activedescendant");
   unhighlightNode(document.getElementById(current_id+"Title"));
   highlightNode(document.getElementById(id+"Title"));
   dump("setActiveDescendant "+id+"\n");
   container.setAttribute("aria-activedescendant", id);
}

function keyCallback(event) {
   var target = event.target;

   if (event.type == "keydown") {
      if (event.altKey) {
         return true;
      }
	  
	  if (event.keyCode == event.DOM_VK_DOWN) {
		 var node_id = getNextNodeId(target);
         if (node_id != '')
            setActiveDescendant(target, node_id)
		 return false;
	  } else if (event.keyCode == event.DOM_VK_UP) {
		 var node_id = getPrevNodeId(target);
         if (node_id != '')
            setActiveDescendant(target, node_id)
		 return false;
	  }  else if (event.keyCode == event.DOM_VK_RIGHT ||
                  event.keyCode == event.DOM_VK_LEFT) {
         var parallel = document.getElementById(getParallelId(
                                                   target.getAttribute(
                                                      "aria-activedescendant")));
         if (parallel) {
            var columns = document.getElementsByClassName("compareTree");
            var column;
            if (event.keyCode == event.DOM_VK_RIGHT)
               column = columns[1];
            else
               column = columns[0];
            column.setAttribute("aria-activedescendant", parallel.id);
            column.focus();
         }
      } 
   }
   return true;
}

function mouseOverNode(obj) {
   if (obj.id == '')
      return;
   var other_obj = getParallelObj(obj);
   obj.mouseout_bg = getComputedBGColor(obj);
   obj.style.backgroundColor = "#ddd";
   if (other_obj) {
      other_obj.mouseout_bg = getComputedBGColor(other_obj);
      other_obj.style.backgroundColor = "#eee";
   }
}

function mouseOutNode(obj) {
   if (obj.id == '')
      return;
   var other_obj = getParallelObj(obj);
   obj.style.backgroundColor = obj.mouseout_bg;
   if (other_obj)
      other_obj.style.backgroundColor = other_obj.mouseout_bg;
}


function highlightNode(obj) {
   if (obj.id == '')
      return;
   var other_obj = getParallelObj(obj);
   var classStr = obj.getAttribute("class").replace(/(.*)highlightedNode/, "$1");
   dump(classStr+"\n");
   obj.setAttribute("class", classStr+" highlightedNode");
   if (other_obj) {
      classStr = other_obj.getAttribute("class").replace(
            /(.*)highlightedNode/, "$1");
      other_obj.setAttribute("class", classStr+" highlightedNode");   }
}


function getComputedBGColor(obj) {
   return window.getComputedStyle(obj, "").getPropertyValue('background-color');
}

function unhighlightNode(obj) {
   if (obj.id == '')
      return;
   var other_obj = getParallelObj(obj);
   var classStr = obj.getAttribute("class").replace(
      /(.*)highlightedNode/, "$1");
   dump('unhighlightNode '+classStr+"\n");
   obj.setAttribute("class", classStr);
   if (other_obj) {
      classStr = other_obj.getAttribute("class").replace(
         /(.*)highlightedNode/, "$1");
      other_obj.setAttribute("class", classStr);
   }
}

function getParallelObj(obj) {
   if (obj.id == '')
	  return null;
   var other_id = getParallelId(obj.id);
   return document.getElementById(other_id);
}

function getParallelId(id) {
   if (id.match("Left"))
      return id.replace(/(.*)Left(Title)?/, "$1Right$2");
   else
      return id.replace(/(.*)Right(Title)?/, "$1Left$2");
}