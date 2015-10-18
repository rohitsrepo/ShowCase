var baseUrl = 'http://www.thirddime.com/contribute-artwork';
// var baseUrl = 'http://localhost:8000/contribute-artwork';

var template = '<section class="extension-thirddime"> \
            <section class="extension-thirddime-actions"> \
                <button class="close-button">x</button> \
            </section> \
        </section>'

$('body').prepend(template)
$('.extension-thirddime').hide();

var hidden = true;

function handleState () {
    if (hidden) {
       $('.extension-thirddime').show();
       $('body').addClass('disable-scroll');
    } else {
       $('.extension-thirddime').hide();
       $('body').removeClass('disable-scroll');
    }
    hidden = !hidden;
};

$('.close-button').on('click', function(){
        handleState();
});

function getImageContainer(source){
    var container = '<div class="extension-thirddime-container">  \
                <section> \
                        <img class="source-image" src="' + source +'"> \
                </section> \
                <section class="user-actions"> \
                </section> \
        </div>';

    var actionButton = $('<button>Add artwork to Thirddime</button>').on('click', function () {
        var targetUrl = baseUrl + '/?artImage=' + encodeURI(source);
        window.open(targetUrl, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=800,width=800')
    })
    var container = $(container);
    container.find('.user-actions').append(actionButton);
    return container;
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){

    switch(request.action){
        case "show-thirddime-pane":
            if (hidden) {
                 var thirddimeList = $('.extension-thirddime');
                 thirddimeList.children().remove('.extension-thirddime-container');

                 $.each($('img'), function(index, value) {

                    if(value.width >= 300 && value.height >= 250){
                        thirddimeList.append(getImageContainer(value.currentSrc));
                    }
                 });
             }

             handleState();
             break;
    }
    return true;
});