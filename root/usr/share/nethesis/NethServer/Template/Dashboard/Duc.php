<?php
// set title
$view->includeCss('
body {
    overflow-x: hidden;
}
circle {
  fill: none;
  pointer-events: all;
}

.sidebar-elem {
    height: 24px;
    text-align: center;
    line-height: 24px;
    color: white;
    font-weight: 800;
    margin: 2px;
}

#main {
  float: left;
}

#sidebar {
  float: right;
  width: 400px;
  margin-top: 35px;
}

#sequence {
  width: 600px;
  height: 70px;
  float: left;
}

#sequence text {
  font-weight: 600;
  fill: #fff;
}

#baseBread {
  float: left;
  height: 30px;
  background: rgb(103, 102, 102);
  margin-right: 3px;
  line-height: 30px;
  width: 90px;
  text-align: center;
  color: white;
}

#chart path {
  stroke: #fff;
}

#explanation {
  margin: auto;
  position: absolute;
  top:90px; left: 0; bottom: 80%; right: 0;
  text-align: center;
  color: #666;
  z-index: 10;
}
#totalSize {
  font-size: 2.5em;
  color: #666;
}
#nameFolder {
  font-size: 20px;
  margin: 5px;
}
#sizeFolder {
  font-size: 2.5em;
  margin: 5px;
}
');

$modulePath = $view->getModuleUrl();

$view->includeFile('NethServer/Js/d3.v3.min.js');
$view->includeFile('NethServer/Js/sequences.js');
$view->includeFile('NethServer/Js/filesize.js');
$view->includeJavascript("
(function($){

    $(function() {
        var cv;

        $.ajax('${modulePath}?get_json').done(function(data) {

        if(! cv) {
             cv = $.duc();
        }
           cv(data);
        });
    });
}(jQuery));
");

// show widget
echo '<div id="main" class="">
        <div id="baseBread">/</div>
        <div id="sequence"></div>
        <div id="explanation">
            <p id="nameFolder">/</p>
            <p id="sizeFolder"></p>
        </div>
        <div id="chart">
        </div>
</div>';
