var g_logging_out = false;
var g_loop = null;
// Utils {{{


function debug(s) {
  // TODO
}

var g_t_info = 0;
function info(s) {
  var inf = $('info');
  var d = new Date();

  inf.update('<div class="info-msg" onclick="$(\'info\').update();">'+s+'</div>');
  g_t_info = d.getTime()
}
function hideInfoIfNeeded() {
  var d = new Date();

  if (g_t_info + 5000 <= d.getTime()) {
    $('info').update();
  }
}

function error(e) {
  var err = $('error');
  var msg = new Element('div', {class: 'error-msg'});
  var children = err.childElements();
  var a = new Element('a', {class: 'error-close'});
  var s = new Element('span');

  s.update(e);
  a.update('[X] ');
  a.observe('click', function(event) {
    elt = Event.findElement(event, 'div');
    elt.remove();
  });

  msg.insert(a);
  msg.insert(s);
  if (children.length >= 5) {
    children[0].remove();
  }
  err.insert(msg);
}

function debug(d) {
  var dbg = $('debug');
  var msg = new Element('div', {class: 'debug-msg'});
  var children = dbg.childElements();
  var a = new Element('a', {class: 'debug-close'});
  var s = new Element('span');

  s.update(d);
  a.update('[X] ');
  a.observe('click', function(event) {
    elt = Event.findElement(event, 'div');
    elt.remove();
  });

  msg.insert(a);
  msg.insert(s);
  dbg.insert(msg);
}
//}}}
// Contact List {{{
var g_cl = null;
var g_pw = null;

function changeMe()
{
  if($('changeMe')) {
    Windows.getWindow('changeMe').toFront();
    return;
  }

  changeMe = new Window({id: 'changeMe', className: "win", title: "Change my infos",
                        width: 300, height: 160, minWidth: 240, minHeight: 150,
                        resizable: true, draggable: true, closable: true,
                        maximizable: false, minimizable: false, detachable: false,
                        showEffectOptions: {duration: 0},
                        hideEffectOptions: {duration: 0}});

  changeMe.setConstraint(true, {left: 0, right: 0, top: 0, bottom: 0});
  var h = '<form id="fchangeme" action="/changeMe">';
  h += 'Nick:<br/><input type="text" name="nick" value="';
  h += $('pw_nick').innerHTML.replace(/^Nick: /, '') + '" /> <br/>';
  h += 'Personal Message:<br/><input type="text" name="psm" value="';
  h += $('pw_psm').innerHTML.replace(/^Msg: /, '') + '" /> <br/>';
  h += '<div id="changemebuttons">';
  h += '<input type="submit" value="Change" />';
  h += '<input type="reset" value="Cancel" />';
  h += '</div></form>';

  changeMe.setHTMLContent(h);

  changeMe.setDestroyOnClose();
  changeMe.showCenter();

  Event.observe('fchangeme', 'submit', function(event) {
    event.stop();
    $('fchangeme').request({
      onComplete: function(){ Windows.getWindow('changeMe').destroy(); }
    });
  });
  Event.observe('fchangeme', 'reset', function(event) {
    event.stop();
    Windows.getWindow('changeMe').destroy();
  });
  $('changemebuttons').setStyle({position: 'absolute', bottom: '10px', left: '25px'});
}

function PersonalWidget(_parent)
{
  var parent = _parent;

  parent.update('<a href="#" id="pw_nick" onclick="changeMe();">Nick: </a><br/>'
                +'<a href="#" id="pw_psm" onclick="changeMe();">Msg: </a><br/>'
                +'<a href="#" id="pw_presence">Presence: </a>');

  this.remove = function() {
    parent.update();
  }

  this.update = function(_nick, _presence, _psm) {
    $('pw_nick').update('Nick: ' + _nick);
    $('pw_psm').update('Msg: ' + _psm);
    $('pw_presence').update('Presence: ' + _presence);
  }
}

function ContactList(_parent)
{
  var groups = {};
  var contacts = {};
  var group_ids = [];
  var parent = _parent;

  parent.update('<ul class="clGroups"><li id="fakegroup" style="display:none"></li></ul>');

  this.remove = function() {
    parent.update();
  }

  this.setGroups = function(_group_ids){
    var prev = $('fakegroup');
    var i, j = 0;

    for (i = group_ids.length - 1; i >= 0; i--) {
      if (_group_ids.indexOf(group_ids[i]) < 0) {
        group_ids[i].remove();
        group_ids.splice(i,1);
      }
    }

    for (i = 0; i < _group_ids.length; i++) {
      if (group_ids[j] == _group_ids[i]) {
        prev = this.getGroup(_group_ids[i]).getElement();
        j++;
      } else {
        elem = this.getGroup(_group_ids[i]).getElement();
        prev.insert({after: elem});
        prev = elem;
      }
    }
    group_ids = _group_ids;
  }

  this.getContact = function(uid){
    if (contacts[uid] == undefined)
      return null;
    return contacts[uid];
  }

  this.setContact = function(uid, c) {
    contacts[uid] = c;
  }

  this.getGroup = function(uid){
    if (groups[uid] == undefined)
      groups[uid] = new Group(uid);
    return groups[uid];
  }

  this.contactClick = function(uid) {
    new Ajax.Request('/contactClicked',
      {parameters:
        {uid: uid}
    });
  }

  this.groupToggle = function(gid) {
    var cts = $('grp_' + gid + '_cts');
    var arrow = $('grp_' + gid + '_arrow');

    if (cts.visible()) {
      cts.hide();
      arrow.src = 'static/images/arrow_up.png';
    } else {
      cts.show();
      arrow.src = 'static/images/arrow.png';
    }
  }
}

function Group(_gid)
{
  var gid = _gid;
  var contact_ids = [];

  var name = "";

  var elem = new Element('li', {id: 'grp_' + gid});

  var h;
  h  = '<div onclick="g_cl.groupToggle(\''+ gid+'\'); return false;">'
  h += '<img id="grp_' + gid + '_arrow" src="static/images/arrow.png" />';
  h += '<span id="grp_' + gid + '_hdr">loading…</span></div>';
  h += '<ul  id="grp_' + gid + '_cts" class="clContacts">';
  h += '<li  id="grp_' + gid + '_fake" style="display:none"></ul>';
  elem.update(h);

  var isCollapsed = false;

  this.remove = function() {
    for (cid in contact_ids) {
      contact_ids[cid].removeFromGroup(gid);
    }
    elem.remove();
  }

  this.getName = function() {
    return name;
  }

  this.getGid = function() {
    return gid;
  }

  this.setName = function(_name) {
    var hdr  = $('grp_' + gid + '_hdr');
    this.name = _name;
    hdr.update(_name);
  }

  this.setContacts = function(_contact_ids) {
    var prev = $('grp_' + gid + '_fake');
    var i, j = 0;

    for (i = contact_ids.length - 1; i >= 0; i--) {
      if (_contact_ids.indexOf(contact_ids[i]) < 0) {
        contact_ids.splice(i,1);
      }
    }

    for (i = 0; i < _contact_ids.length; i++) {
      if (contact_ids[j] == _contact_ids[i]) {
        prev = this.getContact(_contact_ids[i]).getElement(gid);
        j++;
      } else {
        elem = this.getContact(_contact_ids[i]).getElement(gid);
        prev.insert({after: elem});
        prev = elem;
      }
    }
    contact_ids = _contact_ids;
  }

  this.getContacts = function() {
    return contact_ids;
  }

  this.getElement = function() {
    return elem;
  }

  this.getContact = function(_uid) {
    c = g_cl.getContact(_uid);
    if (!c) {
      c = new Contact(gid, _uid);
      g_cl.setContact(_uid, c);
    }
    contact_ids[_uid] = c;
    return c;
  }
}

function Contact(_gid, _uid)
{
  var name = "";
  var uid = _uid;
  var status = "offline";

  var elem = new Element('li',
                         {id: 'ct_' + _uid + '_' + _gid,
                          onclick: 'g_cl.contactClick(\''+uid+'\'); return false;'});
  var img = new Element('img',
                        {src: 'static/images/icons/'+status+'.png'});
  var span = new Element('span');
  elem.insert(img);
  elem.insert(span);

  var elements = {};
  elements[_gid] = elem;

  this.remove = function() {
    for (k in elements) {
      elements[k].remove();
    }
    g_cl.contacts[uid] = undefined;
  }

  this.removeFromGroup = function(_gid) {
    if (elements[groupId] != undefined)
      elements[groupId].remove();
    // TODO: check if elements is empty
  }

  this.setName = function(_name) {
    if (name != _name) {
      name = _name;
      for (k in elements) {
        elements[k].childElements()[1].update('&nbsp;'+_name);
      }
    }
  }
  this.setStatus = function(_status) {
    if (status != _status) {
      status = _status;
      for (k in elements) {
        e = elements[k].childElements()[0];
        e.writeAttribute('src','static/images/icons/'+status+'.png');
      }
    }
  }

  this.getUid = function() {
    return uid;
  }

  this.getName = function() {
    return name;
  }

  this.getElement = function(groupId) {
    if (elements[groupId] == undefined)
      elements[groupId] = elem.clone(true);
    return elements[groupId];
  }
}


function showContactListWindow()
{
  // FIXME
  //$("div.contact_list").show("slow");
}

function hideContactListWindow()
{
  // FIXME
  //$("div.contact_list").hide("slow");
}

function setContactListTitle(title)
{
  // FIXME
  //$("div.contact_list div.title").text(title);
}

function contactListUpdated(groups)
{
  if (g_cl)
    g_cl.setGroups(groups);
}

function groupUpdated(uid, name, contact_ids)
{
  if (g_cl) {
    var group = g_cl.getGroup(uid);
    group.setName(name);
    group.setContacts(contact_ids);
  }
}

function contactUpdated(uid, name, status)
{
  if (g_cl) {
    c = g_cl.getContact(uid);
    c.setName(name);
    c.setStatus(status);
  }
}
// }}}
// ChatWindow {{{
function ChatWindow(_uid)
{
  var uid = _uid;
  var win = new Window({
    id: 'cw_'+uid, className: "win",
    width: 300, height: 300, zIndex: 100,
    minWidth: 205, minHeight: 150,
    resizable: true, draggable: true, closable: true,
    maximizable: true, detachable: false,
    showEffectOptions: {duration: 0}, hideEffectOptions: {duration: 0},
    onClose: function(event) {
      new Ajax.Request('/closeCW',
        {parameters:
          {uid: uid}
      });
    }});

  var widgets = [];

  this.show = function() {
    win.show();
  }

  this.hide = function() {
    win.hide();
  }

  this.remove = function() {
    for (w in widgets) {
      w.remove();
    }
    win.destroy();
  }

  this.shake = function() {
    //FIXME
    var i = 0;
    for (; i < 5; i++)
      Effect.Shake(win.getElement());
  }

  this.addChatWidget = function(widget) {
    win.setContent(widget.getElement());
    widget.setParent(this);
  }

  this.setTitle = function(title) {
    win.setTitle(title);
  }
}

function ChatWidget(_uid)
{
  var uid = _uid;
  var win = null;

  var elem = new Element('div', {id: 'cwdgt_' + uid,
                                 class: 'chatWidget'});

  var c  = new Element('div', {class: 'chatWidgetConversation'});
  var d = new Element('div', {class: 'chatBottomDiv'});
  var t  = new Element('textarea',
                       {class: 'chatTextInput',
                        contenteditable: true});
  elem.appendChild(c);
  d.appendChild(t);
  elem.appendChild(d);

  Event.observe(t, 'keydown',
    function(event) {
      if (event.keyCode == Event.KEY_RETURN) {
        msg = this.getValue();
        this.setValue("");
        new Ajax.Request('/sendMsg',
          {parameters:
            {uid: uid, msg: msg}
        });
        event.stop();
      }
  });

  this.remove = function() {
    Event.stopObserving(t, 'keydown');
    elem.remove();
    win = null;
  }

  this.setParent = function(p) {
    win = p;
  }

  this.getElement = function() {
    return elem;
  }
  /* TODO/FIXME
  conversation.scroll(function() {
    reScroll = Math.abs(conversation[0].scrollHeight - conversation.scrollTop() - conversation.outerHeight()) < 20;
  });


  function scrollBottom()
  {
    if(reScroll)
      conversation.animate({
        scrollTop: conversation[0].scrollHeight
      });
  }
  this.scroll = scrollBottom;
  */

  this.onMessageReceived = function(txt) {
    var msg = new Element('div', {class:'chatMessage'});
    msg.insert(txt);
    //TODO: process smilies on msg
    c.appendChild(msg);
    msg.show();
    /*
    if (reScroll) {
      if (naive) {
        naive = reScroll = false;
        setTimeout(function(){
          scrollBottom();
          reScroll = true;
        }, 1000);
      } else {
        scrollBottom();
      }
    }
    */
  }

  this.nudge = function() {
    win.shake();
  }
}
// Chat functions
var g_chatWindows = {};
var g_chatWidgets = {};

function newChatWindow(uid)
{
  if (g_chatWindows[uid] != undefined)
    g_chatWindows[uid].remove()
  g_chatWindows[uid] = new ChatWindow(uid);
}

function addChatWidget(windowUid, widgetUid)
{
  g_chatWindows[windowUid].addChatWidget(g_chatWidgets[widgetUid]);
}

function showChatWindow(uid)
{
  g_chatWindows[uid].show();
}

function hideChatWindow(uid)
{
  g_chatWindows[uid].hide();
}

function newChatWidget(uid)
{
  g_chatWidgets[uid] = new ChatWidget(uid);
}

function onMessageReceivedChatWidget(uid, msg)
{
  g_chatWidgets[uid].onMessageReceived(msg);
}

function nudgeChatWidget(uid)
{
  g_chatWidgets[uid].nudge();
}

function setTitleCW(uid, title)
{
  g_chatWindows[uid].setTitle(title);
} // }}}
// main {{{

var g_mainWindow = null;

function logoutCb() {
  if (g_logging_out)
    return true;
  if (confirm('Are you sure you want to logout?')) {
    new Ajax.Request('/logout');
    g_logging_out = true;
    loggedOut();
    return true;
  }
  return false;
}
function showMainWindow()
{
  if (!g_mainWindow) {
    function fixMainWindow() {
      $('mw_minimize').setStyle({left: (g_mainWindow.getSize()['width'] - 42) + 'px'});
    }

    Event.observe(window, 'resize', fixMainWindow);

    g_mainWindow = new Window({
      id: 'mw', className: "win",
      width: 210, height: (document.viewport.getHeight() - 60),
      minWidth: 205, minHeight: 150,
      zIndex: 100,
      resizable: true, draggable: true,
      closable: true, maximizable: false, detachable: false,
      showEffectOptions: {duration: 0},
      title: 'aMSN 2',
      hideEffectOptions: {duration: 0},
    });
    g_mainWindow.setConstraint(true, {left: 0, right: 0, top: 0, bottom: 0});
    fixMainWindow();
    g_mainWindow.setHTMLContent('<div id="pw"></div><div id="cl"></div>');
    g_mainWindow.setCloseCallback(logoutCb);
  }
  if (!g_cl) {
    g_cl = new ContactList($('cl'));
    g_pw = new PersonalWidget($('pw'));
  }

  g_mainWindow.showCenter(false, 10, document.viewport.getWidth() - g_mainWindow.getSize()['width'] - 10);
  g_mainWindow.toFront();
}
function hideMainWindow()
{
  g_mainWindow.hide();
}
function setMainWindowTitle(title)
{
  g_mainWindow.setTitle(title);
}
function onConnecting(msg)
{
  info(msg);
}
function showLogin()
{
  $('login').show();
}
function hideLogin()
{
  $('login').hide();
} // }}}

function signingIn()
{
  hideLogin();
}

function myInfoUpdated(_nick, _presence, _psm)
{
  if (g_pw) {
    g_pw.update(_nick, _presence, _psm);
  }
}

function loggedOut() {
  // TODO: show message
  g_loop.stop();
  g_loop = null;

  if (g_cl) {
    g_cl.remove();
    g_cl = null;
  }

  if (g_mainWindow) {
    g_mainWindow.destroy();
    Event.stopObserving(window, 'resize');
    g_mainWindow = null;
  }

  for (c in g_chatWidgets) {
    g_chatWidgets[c].remove()
  }
  g_chatWidgets = {};

  for (c in g_chatWindows) {
    g_chatWindows[c].remove()
  }
  g_chatWindows = {};

  g_logging_out = false;

  hideInfoIfNeeded();

  Event.stopObserving(window, 'beforeunload');
  Event.stopObserving(window, 'unload');

  showLogin();
}






function callInProgress (xmlhttp) {
  switch (xmlhttp.readyState) {
    case 1: case 2: case 3:
      return true;
      break;
      // Case 4 and 0
    default:
      return false;
      break;
  }
}
// Register global responders that will occur on all AJAX requests
Ajax.Responders.register({
  onCreate: function(request) {
    request['timeoutId'] = window.setTimeout( function() {
      // If we have hit the timeout and the AJAX request is active, abort it and let the user know
      if (callInProgress(request.transport)) {
        request.transport.abort();
        error("Unable to contact the aMSN2 server.");
        // Run the onFailure method if we set one up when creating the AJAX object
        if (request.options['onFailure']) {
            request.options['onFailure'](request.transport, request.json);
          }
        }
      },
      5000 // Five seconds
    );
  },
  onComplete: function(request) {
    // Clear the timeout, the request completed ok
    window.clearTimeout(request['timeoutId']);
    if (request.transport.status == 0) {
      error("Unable to contact the aMSN2 server.");
    }
  }
});

function aMSNStart()
{
  $('info').update();
  $('error').update();
  $('debug').update();

  g_logging_out = false;
  g_loop = new PeriodicalExecuter(function(pe) {
    hideInfoIfNeeded();
    new Ajax.Request('/out', {
      method: 'get',
      onException: function(r, e) {
        console.log(e);
      }
    });
  }, 0.5);
  Event.observe(window, 'beforeunload', function(event) {
    if (!logoutCb()) {
      event.stop();
    }
  });
  Event.observe(window, 'unload', function(event) {
    new Ajax.Request('/logout');
  });
}

//vim:sw=2:fdm=marker:
