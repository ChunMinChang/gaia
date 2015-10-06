'use strict';

/* Logger Table:

           | DOM 3                                                                   | Modifiers                    | Deprecated         |
------------------------------------------------------------------------------------------------------------------------------------------
Event type | phase | target | current target | key | code | location | data | repeat | shift | control | alt | meta | keycode | charcode |
------------------------------------------------------------------------------------------------------------------------------------------
keyup
------------------------------------------------------------------------------------------------------------------------------------------
keypress
------------------------------------------------------------------------------------------------------------------------------------------
keydown
------------------------------------------------------------------------------------------------------------------------------------------
*/

var TARGET_ID = 'input';
var LOGGER_ID = 'eventslogger';
var RESET_BTN_ID = 'reset';

window.addEventListener('load', function() {
  console.log('Hello World!');
  init();
});

function addEventListenerWithPhase(type, handler) {
  console.log('>> addEventListener:' + type);
  var tar = document.getElementById(TARGET_ID);
	window.addEventListener(type, handler, true); // capturing phase
  tar.addEventListener(type, handler); // target phase
  window.addEventListener(type, handler, false); // bubbling phase
}

function addEventListeners() {
  console.log('>> addEventListeners()');
	// keyboard events
  addEventListenerWithPhase('keydown', getEventInfo);
	addEventListenerWithPhase('keypress', getEventInfo);
	addEventListenerWithPhase('keyup', getEventInfo);

  // input-method-editor events
	// addEventListenerWithPhase("compositionstart", getEventInfo);
	// addEventListenerWithPhase("compositionupdate", getEventInfo);
	// addEventListenerWithPhase("compositionend", getEventInfo);
  addEventListenerWithPhase('input', getEventInfo);
}

function getEventPhase(num) {
  var phase = ['NONE', 'CAPTURING', 'TARGET', 'BUBBLING'];
  return phase[num];
}

function getModifierKey(key) {
	return key ? '✓' : '✗';
}

function getLocation(num) {
  var location = ['STANDARD', 'LEFT', 'RIGHT', 'NUMPAD'];
	return location[num];
}

function getString(data) {
    if (data === undefined) {
		return data;
	}
	return '\'' + data + '\'';
}

function getKeyVal(key) {
    if (key === undefined) {
		return key;
	}
    if (key >= 32 && key < 127) {
		return key + ' \'' + String.fromCharCode(key) + '\'';
	}
    return key;
}

function getTargetName(obj) {
  if (obj.window === obj) {
    return 'WINDOW';
  }
  return obj.nodeName;
}

function getEventInfo(evt) {
  // var eventinfo = {
  //   'type': evt.type,
  //   'phase': evt.eventPhase,
  //   'target': evt.target.nodeName,
  //   'current_target': evt.currentTarget,
  //   'key': evt.key,
  //   'code': evt.code,
  //   'location': evt.location,
  //   'data': evt.data,
  //   'repeat': evt.repeat,
  //   'shift': evt.shiftKey,
  //   'control': evt.ctrlKey,
  //   'alt': evt.altKey,
  //   'meta': evt.metaKey,
  //   'keyCode': evt.keyCode,
  //   'charCode': evt.charCode
  // };
  // console.log(eventinfo);
  var eventinfo = {
    'type': evt.type,
    'phase': getEventPhase(evt.eventPhase),
    'target': evt.target.nodeName,
    'current_target': getTargetName(evt.currentTarget),
    'key': getString(evt.key),
    'code': evt.code,
    'location': getLocation(evt.location),
    'data': getString(evt.data),
    'repeat': evt.repeat,
    'shift': getModifierKey(evt.shiftKey),
    'control': getModifierKey(evt.ctrlKey),
    'alt': getModifierKey(evt.altKey),
    'meta': getModifierKey(evt.metaKey),
    'keyCode': getKeyVal(evt.keyCode),
    'charCode': getKeyVal(evt.charCode)
  };
  appendEventToLogger(eventinfo);
}

function appendEventToLogger(eventinfo) {
  var loggerTBody = document.getElementById(LOGGER_ID).tBodies[0];

  // Insert to top of logger table
  // var newRow = loggerTBody.insertRow(loggerTBody.rows.length);
  var newRow = loggerTBody.insertRow(0);
  for (var prop in eventinfo) {
    var cell = newRow.insertCell(newRow.cells.length);
    // console.log("eventinfo." + prop + " = " + eventinfo[prop]);
    cell.innerHTML = (eventinfo[prop] === undefined)? '-':eventinfo[prop];
  }
}

function resetLogger() {
  // Clear logger table
  var newTBody = document.createElement('tbody');
  var oldTBody = document.getElementById(LOGGER_ID).tBodies[0];
  oldTBody.parentNode.replaceChild(newTBody, oldTBody);

  // Clear input text
  var tar = document.getElementById(TARGET_ID);
  tar.value='';

  // Focus on input text again
  tar.focus();
}

function init() {
  addEventListeners();

  // Set reset function to button
  var resetBtn = document.getElementById(RESET_BTN_ID);
  resetBtn.addEventListener('click', resetLogger);

  // Focus on input text
  var tar = document.getElementById(TARGET_ID);
  tar.focus();
}
