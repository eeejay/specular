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
   setActiveDescendant(hoverColumn, id);
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
   removeClass(obj, "focus");
   var descendant = document.getElementById(
	  obj.getAttribute("aria-activedescendant"));
   if (descendant)
	  unhighlightNode(descendant);   
}

function getNextNodeId(obj) {
   var current_id = obj.getAttribute("aria-activedescendant");
   var nodes_depth = obj.getElementsByClassName("walkable");
   var i;
   for (i=0;i<nodes_depth.length-1;i++)
	  if (nodes_depth[i].id == current_id) {
		 if (!hasClass(nodes_depth[i+1], "hiddenDetails"))
			return nodes_depth[i+1].id;
         else if (i+2 < nodes_depth.length)
			return nodes_depth[i+2].id;
	  }
   return '';
}

function getPrevNodeId(obj) {
   var current_id = obj.getAttribute("aria-activedescendant");
   var nodes_depth = obj.getElementsByClassName("walkable");
   var i;
   for (i=1;i<nodes_depth.length;i++)
	  if (nodes_depth[i].id == current_id) {
		 if (!hasClass(nodes_depth[i-1], "hiddenDetails"))
			return nodes_depth[i-1].id;
		 else if (i-2 >= 0)
			return nodes_depth[i-2].id;
	  }
   return '';
}

function scrollIntoViewIfNeeded(obj) {
   if (obj.nodeName == "LI")
      obj = document.getElementById(obj.id+"Title");
   var top = obj.offsetTop;
   var offsetParent = obj.offsetParent;
   while (offsetParent != null) {
      top = top + offsetParent.offsetTop;
      offsetParent = offsetParent.offsetParent;
   }
   var bottom = top + obj.offsetHeight;
   if (bottom > (window.pageYOffset + window.innerHeight)) {
      dump(bottom+" "+window.pageYOffset+" "+window.innerHeight+" Scroll!\n");
      obj.scrollIntoView(false);
   } else {
      dump(bottom+" "+window.pageYOffset+" "+window.innerHeight+" Don't\n");
   }
   if (top < window.pageYOffset)
      obj.scrollIntoView(true);
}

function setActiveDescendant(container, id) {
   var current_id = container.getAttribute("aria-activedescendant");
   unhighlightNode(document.getElementById(current_id));
   var to_activate = document.getElementById(id);
   if (hasClass(to_activate, "hiddenDetails")) {
	  ad = id.replace(/Dialog/, "");
   	  setTimeout("showDetails(ad)", 0);
   }
   highlightNode(to_activate);
   scrollIntoViewIfNeeded(to_activate);
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
            var columns = document.getElementsByClassName("compareColumn");
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
		 if (!ad.match("Dialog")) {
			setTimeout("showDetails(ad)", 0);
		 } else {
			ad = ad.replace(/Dialog/, "");
			setTimeout("showDetails(ad)", 0);
			setActiveDescendant(target, ad);
		 }
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
   addClass(obj, "highlighted");
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  addClass(other_obj, "highlighted");
}

function unhighlightNode(obj) {
   removeClass(obj, "highlighted");
   var other_obj = getParallelObj(obj);
   if (other_obj)
	  removeClass(other_obj, "highlighted");
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
