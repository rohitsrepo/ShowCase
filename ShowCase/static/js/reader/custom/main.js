$(document).ready(function() {
	 $(".middle a").click(function() {
        $.scrollTo($(".second-view"), { duration: 1200});
    });
	 $(".da0").click(function() {
        $.scrollTo($(".feed1"), { duration: 1000});
    });
	 $(".da1").click(function() {
        $.scrollTo($(".feed2"), { duration: 1000});
    });
	 $(".da2").click(function() {
        $.scrollTo($(".feed3"), { duration: 1000});
    });
	 $(".da3").click(function() {
        $.scrollTo($(".feed4"), { duration: 1000});
    });

});