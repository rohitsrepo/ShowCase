$(document).ready(function() {
     $(".middle a").click(function() {
                $.scrollTo($(".second-view"), { duration: 1200});
        });

    //DEAL WITH CURTAIN HERE

    var leftCurtainHandler = {

        addCurtain: function () {
            $(".curtain-left").removeClass('animated fadeOutLeft');
            $(".curtain-left").addClass('animated fadeInLeft');
            $(".curtain-left").animate({marginLeft:0}, 400);
            $(".curtain-left .link1").addClass('animated fadeInUpBig');
            setTimeout(function(){$(".curtain-left .link2").addClass('animated fadeInUpBig')}, 50);
            setTimeout(function(){$(".curtain-left .link3").addClass('animated fadeInUpBig')}, 90);
            setTimeout(function(){$(".curtain-left .link4").addClass('animated fadeInUpBig')}, 130);
            setTimeout(function(){$(".curtain-left .link5").addClass('animated fadeInUpBig')}, 170);
            setTimeout(function(){$(".curtain-left .link6").addClass('animated fadeInUpBig')}, 210);
            setTimeout(function(){$(".curtain-overlay-placeholder").addClass("curtain-overlay")}, 250);
        },

         removeCurtain: function () {
            $(".curtain-left .link1").removeClass('animated fadeInUpBig');
            $(".curtain-left .link2").removeClass('animated fadeInUpBig');
            $(".curtain-left .link3").removeClass('animated fadeInUpBig');
            $(".curtain-left .link4").removeClass('animated fadeInUpBig');
            $(".curtain-left .link5").removeClass('animated fadeInUpBig');
            $(".curtain-left .link6").removeClass('animated fadeInUpBig');
            $(".curtain-left").removeClass('animated fadeInLeft');
            $(".curtain-left").addClass('animated fadeOutLeft');
            $(".curtain-left").animate({marginLeft:-500}, 300);
            $(".curtain-overlay-placeholder").removeClass("curtain-overlay");
        },

         isCurtainActive: function () {
            if($(".curtain-left").hasClass("fadeInLeft")){
                return true;
            }
            return false;
        }
    };

    var rightCurtainHandler = {

        addCurtain: function () {
            $(".curtain-right").removeClass('animated animated fadeOutRight');
            $(".curtain-right").addClass('animated fadeInRight');
            $(".curtain-right").animate({marginRight:0}, 400);
            $(".auth-user").removeClass("animated fadeInRight");
            $(".auth-user").addClass("animated fadeOutLeft");
            setTimeout(function(){$(".curtain-overlay-placeholder").addClass("curtain-overlay")}, 250);
        },

         removeCurtain: function () {
            $(".curtain-right").removeClass('animated fadeInRight');
            $(".curtain-right").animate({marginRight:-500}, 300);
            $(".auth-user").removeClass("animated fadeOutLeft");
            $(".auth-user").addClass("animated fadeInRight");
            $(".curtain-overlay-placeholder").removeClass("curtain-overlay");
        },

         isCurtainActive: function () {
            if($(".curtain-right").hasClass("fadeInRight")){
                return true;
            }
            return false;
        }
    };

    $(".logo").click(function () {
        if(!leftCurtainHandler.isCurtainActive()){
            leftCurtainHandler.addCurtain();
        }
        else {
            leftCurtainHandler.removeCurtain();
        }
    });

    $(".auth-user").click(function () {
        if(!rightCurtainHandler.isCurtainActive()){
            rightCurtainHandler.addCurtain();
        }
        else {
            rightCurtainHandler.removeCurtain();
        }
    });
        
    $('.posts, .banner').click(function() {
        if(leftCurtainHandler.isCurtainActive()){
            leftCurtainHandler.removeCurtain();
        }

        if(rightCurtainHandler.isCurtainActive()){
            rightCurtainHandler.removeCurtain();
        }
    });

});