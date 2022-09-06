$(document).ready(function () {
    let nav_offset_top = $('.header_area').height()+5;

    function navbarFixed() {
        if ($('.header_area').length) {
            $(window).scroll(function () {
                let scroll = $(window).scrollTop();
                if (scroll >= nav_offset_top) {
                    $('.header_area .main-menu').addClass('on_scroll');
                } else {
                    $('.header_area .main-menu').removeClass('on_scroll');
                }
            })
        }
    }


navbarFixed();

});



