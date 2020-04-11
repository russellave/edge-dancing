// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 0; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
  close[i].onclick = function() {
    var div = this.parentElement;
    div.style.display = "none";
    console.log("clicked")
  }
}

Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

// Add a "checked" symbol when clicking on a list item

var dropdown = [];
var br = document.createElement("br");
// Create a new list item when clicking on the "Add" button
function newElement() {
  var li = document.createElement("li");
  var inputValue1 = document.getElementById("myTitle").value;
  // var inputValue2 = document.getElementById("myESP32").value;
  // var inputValue3 = document.getElementById("myPin").value;

  var t = document.createTextNode(inputValue1)
    // +'-'+inputValue2+'-'+inputValue3);
  li.appendChild(t);
  // li.appendChild(br);
  // li.appendChild(document.createTextNode("hi"));
  if (inputValue1 === '' ) {
  //|| inputValue2 === '' || inputValue3 === '') {
    alert("You must input all fields!");
  } else {
    document.getElementById("myUL").appendChild(li);
  }
  document.getElementById("myTitle").value = "";
  // document.getElementById("myESP32").value = "";
  // document.getElementById("myPin").value = "";


  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      var div = this.parentElement;
      var name =  div.textContent.split('-')[0]
      div.style.display = "none";
      dropdown.remove(div.textContent.split('-')[0])
      var select = document.getElementById("selectComponent");
      while (select.firstChild) {
        select.firstChild.remove();
      } 
      var ele = document.createElement("option");
      ele.textContent = "Choose a component";
      ele.value = "Choose a component";
      select.appendChild(ele);
    //   for (i=0; i < select.children.length; i++) {
    //       select.children[i].style.display="none";
    //   }
    
      for(var i = 0; i < dropdown.length; i++) {
            var opt = dropdown[i];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            select.appendChild(el);
      }
      //remove from schedule
      var comps = document.getElementById("myUL2").children
      // console.log(comps[0].textContent)
      for (var j = 0; j < comps.length; j++) {
        if (comps[j].id === name) {
          comps[j].style.display = "none";
          break
        }
      }

     }
  }
//   var list = document.querySelector('ul');
//   for (i=0; i<list.children.length; i++) {
//      dropdown.push(list.children[i].textContent.split('-')[0])
//   }
  dropdown.push(inputValue1)
  var select = document.getElementById("selectComponent");
  while (select.firstChild) {
    select.firstChild.remove();
  } 
  var ele = document.createElement("option");
  ele.textContent = "Choose a component";
  ele.value = "Choose a component";
  select.appendChild(ele);
//   for (i=0; i < select.children.length; i++) {
//       select.children[i].style.display="none";
//   }

  for(var i = 0; i < dropdown.length; i++) {
        var opt = dropdown[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
  }
  
}

function log() {
  var start = document.getElementById("start").value
  var end = document.getElementById("end").value

  if (document.getElementById("selectComponent").value === "Choose a component") {
    alert("Must select a component first! If no components appear, try adding one below.")
  }
  else if (document.getElementById("selectOnOff").value === "Choose on/off") {
    alert("You must select the component to be on or off!")
  }
  else{
    var id = document.getElementById("selectComponent").value
    var found = false
    var comps = document.getElementById("myUL2").children
    for (var i = 0; i < comps.length; i++){
      if (comps[i].id === id) {
        var t = document.createTextNode("-" + document.getElementById("selectOnOff").value + ' @ ' + start)
        comps[i].appendChild(document.createElement("br"))
        comps[i].appendChild(t)
        found = true
        break
      }
    }
    if (!found) {
      var li = document.createElement("li");
      li.id = id
      var t = document.createTextNode(document.getElementById("selectComponent").value);
      t.onclick = function () {console.log("hi")}
      li.appendChild(t)
      li.appendChild(document.createElement("br"))
      var v = document.createTextNode("-" + document.getElementById("selectOnOff").value + ' @ ' + start)
      li.appendChild(v)
      document.getElementById("myUL2").appendChild(li);
    }

  }
}

function save() {
  var comps = document.getElementById("myUL2").children
  if (comps == null) {
    return;
  }
  var toSave = []
  for (i = 0; i < comps.length; i++) {
    var id = comps[i].id;
    var elements = comps[i].textContent.split('-').slice(1)
    for (j = 0; j < elements.length; j++) {
      var parse = elements[j].split('@').map(item => item.trim())
      var color = parse[0]
      var time = parse[1]
      var spl = time.split(':')
      time = (parseFloat(spl[0])*60*60 + parseFloat(spl[1])*60 + parseFloat(spl[2])).toFixed(2)
      var obj = {
        "ID": id,
        "COLOR": color,
        "TIME": time
      }
      toSave.push(obj)
    }
  }
  toSave.sort((a,b) => a.TIME-b.TIME)
  var hiddenElement = document.createElement('a');
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(convertToCSV(toSave));
  hiddenElement.target = '_blank';
  hiddenElement.download = 'people.csv';
  hiddenElement.click();
  // console.log(toSave)
}
function convertToCSV(arr) {
  const array = [Object.keys(arr[0])].concat(arr)

  return array.map(it => {
    return Object.values(it).toString()
  }).join('\n')
}