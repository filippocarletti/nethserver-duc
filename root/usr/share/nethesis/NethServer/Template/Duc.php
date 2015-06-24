<?php

/* @var $view \Nethgui\Renderer\Xhtml */

echo $view->header()->setAttribute('template', $T('Duc_Title'));

// set title
$view->includeCss('
body {
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
  display: none;
}

#sidebar {
  float: right;
  width: 400px;
  margin-top: 35px;
}

#sequence {
  width: 600px;
  height: 40px;
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

#chart {
  margin-top: -20px;
  margin-bottom: -80px;
}

#chart path {
  stroke: #fff;
}

#explanation {
  margin-top: 50px;
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
  margin-top: 20px;
}
#sizeFolder {
  font-size: 2.5em;
  margin: 5px;
}

#updateInfo div.TextLabel {
  font-size: 14px;
  color: #666;
  font-weight: 600;
}
');

$modulePath = $view->getModuleUrl();

$dateTarget = $view->getClientEventTarget('date');

$view->includeFile('NethServer/Js/d3.v3.min.js');
$view->includeFile('NethServer/Js/sequences.js');
$view->includeFile('NethServer/Js/filesize.js');
$view->includeJavascript("
(function($){
    var updateGraph = function() {
        var cv;
        $('#chart').empty();

        $.ajax('${modulePath}?get_json').done(function(data) {

            if(data) {
                if(!cv) {
                    cv = $.duc();
                }
                cv(data);
                $('#main').show();
            }
        });

    };
    $(updateGraph);
    $('.${dateTarget}').on('nethguiupdateview', updateGraph);
}(jQuery));
");

// show widget
$widget = '<div id="main" class="">
        <a href="javascript:void(0)"><div onclick="$.reset();" id="baseBread">/</div></a>
        <div id="sequence"></div>

        <div id="explanation">
            <p id="nameFolder">/</p>
            <p id="sizeFolder"></p>
        </div>

        <div id="chart">
        </div>
</div>
<div id="updateInfo">
'.$view->buttonList()->insert($view->button('Update', $view::BUTTON_SUBMIT)).
$view->textLabel('date')->setAttribute('template', $T('Updated on ${0}'))->setAttribute('tag','div') .'
</div>';

echo $widget;
