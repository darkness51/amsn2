// TODO: have info/debug/err functions

var g_loop = null;
// Utils {{{


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
//}}}
// Contact List {{{
var g_cl = null;

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

  var elem = new Element('li',
                         {id: 'ct_' + _uid + '_' + _gid,
                          onclick: 'g_cl.contactClick(\''+uid+'\'); return false;'});

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
    name = _name;
    for (k in elements) {
      elements[k].update(_name);
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

function contactUpdated(uid, name)
{
  if (g_cl)
    g_cl.getContact(uid).setName(name);
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
    Event.StopObserving(t, 'keydown');
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
var chatWindows = {};
var chatWidgets = {};

function newChatWindow(uid)
{
  if (chatWindows[uid] != undefined)
    chatWindows[uid].remove()
  chatWindows[uid] = new ChatWindow(uid);
}

function addChatWidget(windowUid, widgetUid)
{
  chatWindows[windowUid].addChatWidget(chatWidgets[widgetUid]);
}

function showChatWindow(uid)
{
  chatWindows[uid].show();
}

function hideChatWindow(uid)
{
  chatWindows[uid].hide();
}

function newChatWidget(uid)
{
  chatWidgets[uid] = new ChatWidget(uid);
}

function onMessageReceivedChatWidget(uid, msg)
{
  chatWidgets[uid].onMessageReceived(msg);
}

function nudgeChatWidget(uid)
{
  chatWidgets[uid].nudge();
} // }}}
// main {{{

var g_mainWindow = null;

function logoutCb() {
  if (confirm('Are you sure you want to logout?')) {
    new Ajax.Request('/logout');
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
    g_mainWindow.setHTMLContent('<div id="cl"></div>');
    g_mainWindow.setCloseCallback(logoutCb);
  }
  if (!g_cl) {
    g_cl = new ContactList($('cl'));
  }
  g_mainWindow.showCenter(false);
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

function myInfoUpdated(s)
{
  // TODO
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
    Event.StopObserving(window, 'resize');
    g_mainWindow = null;
  }

  for (c in chatWidgets) {
    chatWidgets[c].remove()
  }
  chatWidgets = {};

  for (c in chatWindows) {
    chatWindows[c].remove()
  }
  chatWindows = {};

  showLogin();
}

function aMSNStart()
{
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
