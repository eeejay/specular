var ad;
var hoverColumn = null;

function getDetailsTable(obj) {
   if (!obj)
	  return null;
   var collection = obj.getElementsByClassName("accDetails");
   if (collection.length == 0)
	  return null;
   return collection[0];
}

function onNodeClick(obj) {
   var id = obj.id.replace(/Title/, "");
   setActiveDescendant(hoverColumn.firstChild, id);
   showDetails(id);
}

function showDetails(id) {
   var obj = document.getElementById(id);
   var details = getDetailsTable(obj);
   if (hasClass(details, "hiddenDetails")) {
	  removeClass(details, "hiddenDetails");
	  obj.setAttribute("aria-expanded", "true");
      details.setAttribute("aria-hidden", "false");
	  return details;
   } else {
	  addClass(details, "hiddenDetails");
	  obj.setAttribute("aria-expanded", "false");
      details.setAttribute("aria-hidden", "true");
   }
   return null;
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
   container.setAttribute("aria-activedescendant", id);
}

function nodeKeyCallback(event) {
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
	  }  else if (event.keyCode == event.DOM_VK_ENTER ||
				  event.keyCode == event.DOM_VK_RETURN) {
		 ad = target.getAttribute("aria-activedescendant");
		 setTimeout("showDetails(ad)", 0);
	  }
   }
   return true;
}

function mouseOverNode(obj) {
   if (obj.id == '')
      return;
   addClass(obj, "mouseOverNode");
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  addClass(other_obj, "mouseOverNode");
}

function mouseOutNode(obj) {
   if (obj.id == '')
      return;
   removeClass(obj, "mouseOverNode");
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  removeClass(other_obj, "mouseOverNode");
}

function mouseOverTree(obj) {
   addClass(obj, "mouseOverTree");
   hoverColumn = obj;
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  addClass(other_obj, "mouseOverTree");
}

function mouseOutTree(obj) {
   removeClass(obj, "mouseOverTree");
   hoverColumn = null;
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  removeClass(other_obj, "mouseOverTree");
}


function highlightNode(obj) {
   if (obj.id == '')
      return;
   addClass(obj, "highlightedNode");
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  addClass(other_obj, "highlightedNode");
}


function getComputedBGColor(obj) {
   return window.getComputedStyle(obj, "").getPropertyValue('background-color')
}

function unhighlightNode(obj) {
   if (obj.id == '')
      return;
   removeClass(obj, "highlightedNode");
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  removeClass(other_obj, "highlightedNode");
}

function getParallelObj(obj) {
   if (obj.id == '')
	  return null;
   var other_id = getParallelId(obj.id);
   return document.getElementById(other_id);
}

function getParallelId(id) {
   if (!id)
	  return '';
   if (id.match("Left"))
      return id.replace(/(.*)Left(Title|Dialog)?/, "$1Right$2");
   else
      return id.replace(/(.*)Right(Title|Dialog)?/, "$1Left$2");
}

function addClass(obj, cls) {
   var regex = new RegExp("\\s"+cls, "g");
   classStr = obj.getAttribute("class").replace(regex, "");
   obj.setAttribute("class", classStr+" "+cls);
}

function removeClass(obj, cls) {
   var regex = new RegExp("\\s"+cls, "g");
   classStr = obj.getAttribute("class").replace(regex, "");
   obj.setAttribute("class", classStr);
}

function hasClass(obj, cls) {
   return obj.getAttribute("class").match(cls)
}
