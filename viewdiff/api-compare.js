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

function highlightNode(obj) {
   if (obj.id == '')
      return;
   var other_obj = getParallelObj(obj);
   obj.prev_bg = getComputedBGColor(obj);
   obj.style.backgroundColor = "#aaa";
   other_obj.prev_bg = getComputedBGColor(other_obj);
   other_obj.style.backgroundColor = "#aaa";
}

function getComputedBGColor(obj) {
   return window.getComputedStyle(obj, "").getPropertyValue('background-color');
}

function unhighlightNode(obj) {
   if (obj.id == '')
      return;
   var other_obj = getParallelObj(obj);
   obj.style.backgroundColor = obj.prev_bg;
   other_obj.style.backgroundColor = other_obj.prev_bg;
}

function getParallelObj(obj) {
   var other_id;
   if (obj.id == '')
	  return null;
   var suffix_index;
   if (obj.id.match("Left"))
      other_id = obj.id.replace(/Left/, "Right");
   else
      other_id = obj.id.replace(/Right/, "Left");

   return document.getElementById(other_id);
}