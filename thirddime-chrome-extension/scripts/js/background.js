function httpGet(theUrl)
{
  var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
  }

  chrome.extension.onMessage.addListener(function(request, sender, sendResponse){
    switch(request.type){
      case "add-to-series":
      console.log(request.data.imageUrl);
      console.log(httpGet("http://192.168.3.12:8000/users/me/buckets"));
      break;
    }
    return true;
  });

  chrome.browserAction.onClicked.addListener(function(tab){
    console.log(tab);
    chrome.tabs.sendMessage(tab.id, {action: "show-thirddime-pane"}, function(response) {});
    return true;
  });