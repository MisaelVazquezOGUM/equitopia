$(function() {
    var target_drop = $("#vouge-header-new-3 #top_menu_collapse .nav-item");
    var add_target = $("#vouge-header-new-3 #top_menu_collapse .dropdown");
    var add_target_login = $("#vouge-header-new-3 #top_menu_collapse .dropup");
    if (target_drop.hasClass('dropdown')) {
      $(add_target).addClass('dropright');
      $(add_target_login).addClass('dropright');
    }

    var sidebar_wrap = $("body #wrapwrap");
    if($("header").hasClass('vouge_header_three')){
      $(sidebar_wrap).addClass('sidebar_wrap_border');
      $(sidebar_wrap).addClass('position-static');
      $(sidebar_wrap).addClass('wrap-border');
    }
});

$(document).ready(function(){
    
    $(function() {
      $('#wrapwrap').scroll(function() {
        if ($(this).scrollTop() > 100) {
          $('a.top').addClass('show-to-top');
        } else {
          $('a.top').removeClass('show-to-top');
        }
      });
      $('#to-top a').click(function() {
        $('body,html').animate({
          scrollTop : 0
        }, 800);
        return false;
      });
    });

    $(function() {
      $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
          $('.bizople-mbl-bottom-bar').addClass('show-bottom-bar');
        } else {
          $('.bizople-mbl-bottom-bar').removeClass('show-bottom-bar');
        }
      });
    });

    $("a.active").find('.mycheckbox').prop('checked', true);

    $('[data-toggle="popover"]').popover()

    $(".close-search").click(function() {
      $(".search-box").removeClass("open");
    });


    $(".open-extra-menu").click(function() {
      if($('.extra-menu-bar').hasClass('open')){
        $(".extra-menu-bar").removeClass("open");
        $(".bottom-bar-extra-menu").removeClass("active");
      } else {
        $(".extra-menu-bar").addClass("open");
        $(".bottom-bar-extra-menu").addClass("active");
      }
    });
    if($('.template_404_page').hasClass('template_404_page')){
      $('.template_404_page').parent().siblings('hr').addClass('d-none');
    }
});

$(function() {

  $("body").addClass("blured-bg");

  /* menu sidebar js */
  $("#show-sidebar").on("click", function(e) {
    $(".sidebar-wrapper").addClass("toggled");
    $(".blured-bg").addClass("active");
    e.stopPropagation()
  });
  $(".bottom-show-sidebar").on("click", function(e) {
    $(".sidebar-wrapper").addClass("toggled");
    $(".blured-bg").addClass("active");
    e.stopPropagation()
  });
  $("#close_mbl_sidebar").on("click", function(e) {
    $(".sidebar-wrapper").removeClass("toggled");
    $(".blured-bg").removeClass("active");
    e.stopPropagation()
  });
  $(document).on("click", function(e) {
    if (!$(e.target).closest('.sidebar-wrapper').length) {
      $(".sidebar-wrapper").removeClass("toggled");
      $(".blured-bg").removeClass("active");
    }
  });

});