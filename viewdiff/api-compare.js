function showDetails(obj) {
   if (obj.nextSibling.style.display == 'table')
      obj.nextSibling.style.display = 'none'
   else
      obj.nextSibling.style.display = 'table';
}

function highlightMoved(obj) {
   var other_obj = getParallelObj(obj);
   var compStyle = window.getComputedStyle(obj, "");
   obj.prev_bg = compStyle.getPropertyValue('background-color');
   obj.style.backgroundColor = "#FFA500";
   other_obj.style.backgroundColor = "#FFA500";
}

function unhighlightMoved(obj) {
   var other_obj = getParallelObj(obj);
   obj.style.backgroundColor = obj.prev_bg;
   other_obj.style.backgroundColor = obj.prev_bg;
}

function getParallelObj(obj) {
   var other_id;
   var suffix_index;
   if (obj.id.match("Left"))
      other_id = obj.id.replace(/Left/, "Right");
   else
      other_id = obj.id.replace(/Right/, "Left");

   return document.getElementById(other_id);
}