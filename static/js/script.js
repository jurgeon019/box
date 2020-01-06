$(document).ready(function() {

  if ($('input[name="phone"]').length > 0) {
    $('input[name="phone"]').mask("+380(99)999-99-99");
  }

  $('.form-sign_up').on('click', function(e) {
    e.preventDefault();
    $.fancybox.close();
    $.fancybox.open({
      src: '#form-register',
    });
  });
  $('.btn_card-credit').on('click', function(e) {
    e.preventDefault();
    var id = $(this).data('item_id');
    if (id !== "") {
      $.fancybox.close();
      $.fancybox.open({
        src: '#form-order-credit',
        afterShow: function() {
          var product_item = document.createElement("input");
          product_item.setAttribute('type', 'hidden');
          product_item.setAttribute('name', 'product_id');
          product_item.setAttribute('value', id);
          $('.fancybox-content').append(product_item);
        }
      });
    } else {
      console.log("id_productu_ne_vedene");
    }
  });
  $('.form-sign_in').on('click', function(e) {
    e.preventDefault();
    $.fancybox.close();
    $.fancybox.open({
      src: '#form-login',
    });
  });
  $('.tab_header_item').on('click', function() {
    $('.tab_header_item').removeClass('tab_header_item-active');
    $(this).addClass('tab_header_item-active');
    $('.tab_main').removeClass('tab_main-active');
    $('#' + $(this).data('item')).addClass('tab_main-active');
  })





  $('.search__input').on('focus', function() {
    $(this).parents('.search__form').addClass('search__form-focus');

  });
  $('.search').on('click', function() {
    if ($(this).val() === '') {
      $(this).parents('.search__form').removeClass('search__form-focus')
    }
  });

  $('.next').on('click', function() {
    if ($(this).parents('.search__form')[0].querySelector('input').value === '') {
      $('.search__form').removeClass('search__form-focus')
    } else {
      var querySearch = $(this).parents('.search__form')[0].querySelector('input').value;


      sessionStorage.setItem('search__site', querySearch);
      location.href = "/search/";
    }
  });
  $('.blog_search .search__input').on('keydown', function(e) {
    if ($(this).val() !== '' && e.keyCode === 13) {
      e.preventDefault();
      console.log($(this).val());

    }
  });

  $('.search__input').on('blur', function() {
    if ($(this).parents('.search__form')[0].querySelector('input').value === '') {
      $('.search__form').removeClass('search__form-focus')
    }
  });


  $('.search__input').on('keydown', function(e) {
    if ($(this).val() !== '' && e.keyCode === 13) {
      e.preventDefault();
      sessionStorage.setItem('search__site', $(this).val());
      location.href = "/search/";
    }
  });

  $(".js-hamburger").on('click', function(e) {
    $('.js-hamburger').toggleClass('is-active');
    $('.navbar').toggleClass('navbar-active');
    $('.body_bg').toggleClass('body_bg-active');
    $('body').toggleClass('body__navbar-active');
    $('.navbar__wrap').toggleClass('navbar__wrap-active');

    $('.navbar__main').removeClass('navbar__main_next-step');
    $('.navbar__submenu').removeClass('navbar__submenu-active_mob');

  });

  select_main_menu(document.getElementsByClassName('navbar_item'), "nbbmnggg");

  $('.navbar_item_text').on('click', function() {
    console.log();
    if ($(this)[0].parentNode.getElementsByClassName('navbar__submenu').length > 0) {
      $(this)[0].parentNode.getElementsByClassName('navbar__submenu')[0].classList.add("navbar__submenu-active_mob")
      $('.navbar__main').addClass('navbar__main_next-step')
    }
  })
  $('.navbar__submenu_prev-step').on('click', function() {
    $('.navbar__main').removeClass('navbar__main_next-step');
    $('.navbar__submenu').removeClass("navbar__submenu-active_mob")
  })

  $('.header__section_login-control').on('click', function() {
    $('.section__login_info').toggleClass('section__login_info-active');
    $('.header__section_login-control').toggleClass('header__section_login-control-active');
  })

  if (document.getElementsByClassName('main_slider_wrap').length > 0) {
    $('.main_slider_wrap').slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false
    });
    $('.main_slider_wrap').on('afterChange', function(event, slick, direction) {

      // left
    });
  }
  // Search page знизу




  // ******************* СКрипти на головній вище Каталог нище




  $('.select__wrap_item').on('click', function() {
    var text = $(this).text();
    var id = $(this).data('id');
    var field = $(this).parents('.select').find(".field_text ");
    var input_select = $(this).parents('.select').find("input");
    $(field).text(text);
    $(input_select).val(id);
    $('.select__wrap').removeClass('select__wrap-active');
    $('.field').removeClass('field-active');
  });


  $('.select__intup').on('click', doSomething);


  // ************Картка товару нище
  if (document.getElementsByClassName('gallery-thumbs').length > 0) {

    var galleryThumbs = new Swiper('.gallery-thumbs', {
      spaceBetween: 10,
      slidesPerView: 4,
      loop: true,
      freeMode: true,
      loopedSlides: 5, //looped slides should be the same
      watchSlidesVisibility: true,
      watchSlidesProgress: true
    });
    var galleryTop = new Swiper('.gallery-top', {
      spaceBetween: 10,
      loop: true,
      loopedSlides: 5, //looped slides should be the same
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
      },
      thumbs: {
        swiper: galleryThumbs
      }
    });
  }
  $('.btn-more').on('click', function() {
    $('.product__description__wrap').toggleClass('product__description__wrap-active');

  })
  if (document.getElementsByClassName('card-list__related').length > 0) {
    var swiper = new Swiper('.card-list__related', {
      slidesPerView: 3,
      spaceBetween: 30,
      pagination: {
        el: '.swiper-pagination',
        clickable: true
      },
      breakpoints: {
        510: {
          slidesPerView: 1,
          spaceBetween: 60
        },

        992: {
          slidesPerView: 2,
          spaceBetween: 50
        }
      }
    });
  }
  var pluses, minuses, inputs;
  pluses = document.querySelectorAll('.plus-btn')
  minuses = document.querySelectorAll('.minus-btn')
  inputs = document.querySelectorAll('.product__quantity_count')
  pluses.forEach(function(plus) {
    plus.addEventListener('click', change_cart_item_amount)
  })
  minuses.forEach(function(minus) {
    minus.addEventListener('click', change_cart_item_amount)

  })
  inputs.forEach(function(input) {
    input.addEventListener('change', change_cart_item_amount)

  })
  var add_basket;
  add_basket = document.querySelectorAll('.add_basket');
  add_basket.forEach(function(basket) {
    basket.addEventListener('click', add_card_item)
  })

  function add_card_item() {

    console.log();
    if (!$(this).hasClass('btn-disable')) {
      var data = $(".form_product_item").serialize().split("&");

      var obj = {};
      for (var key in data) {
        obj[data[key].split("=")[0]] = data[key].split("=")[1];
      }

      fetch('/add_cart_item/', {
          method: 'POST',
          body: new URLSearchParams($.param(obj))
        })
        .then(data => {

          return data.json();
        })
        .then(data => {
          console.log(data);
          $('.product__control .add_basket').text('Тoвар в корзині');
          $('.basket__count span').text(data.cart_items_quantity);
          console.log($('.basket__count .items_counter'));
          $('.product__control .add_basket').addClass('btn-disable');
          $('.product__group_plus').on('click',function(){
            change_item_amount()
          });
          $('.product__group_minus').on('click',function(){
            change_item_amount()
          });
        })
    }


  }

  fetch('/get_cart_items/', {
      method: 'POST',
    })
    .then(data => {

      return data.json();
    })
    .then(data => {
      if (data.items_amount > 0) {
        $('.basket__count span').text(data.items_amount);
        console.log("crash");
      }

      forEach(data.cart_items, function(index, value) {

        if ($('.form_product_item').length > 0) {
          if ($('.item_id')[0].value == value.item.id) {
            $('.product__control .add_basket').addClass('btn-disable');
            $('.product__control .add_basket').text('Тoвар в корзині');

          }

        }

      })

    })

  // *************** catalog

  // profille

  $('.profil__navigation_link').on('click', function() {
    $('.profil__navigation_link').removeClass('profil__navigation_link-active');
    $('.profil__content ').removeClass('profil__content-active');
    $(this).addClass('profil__navigation_link-active');
    $('#' + $(this).data('nav')).addClass('profil__content-active');

  });


})

function doSomething() {
  var select__wrap = $(this).parent('.select').find(".select__wrap");
  var field = $(this).parent('.select').find(".field");
  $(select__wrap).toggleClass('select__wrap-active');
  $(field).toggleClass('field-active');
}

$(document).mouseup(function(e) {
  var select = $(e.target).parents('.select'); // тут указываем класс элемента
  if (select.length > 0) {} else {
    $('.select__wrap').removeClass('select__wrap-active');
    $('.field').removeClass('field-active');
  }
  var select = $(e.target).parents('.navbar '); // тут указываем класс элемента
  if (select.length > 0) {} else {
    $('.js-hamburger').removeClass('is-active');
    $('.navbar').removeClass('navbar-active');
    $('.body_bg').removeClass('body_bg-active');
    $('body').removeClass('body__navbar-active');
    $('.navbar__wrap').removeClass('navbar__wrap-active');

    $('.navbar__main').removeClass('navbar__main_next-step');
    $('.navbar__submenu').removeClass('navbar__submenu-active_mob');
  }
});


// ***************** виділення і відкриття меню при ховері
function select_main_menu(item, hhh) {

  forEach(item, function(index, value) {
    value.onmouseleave = function(event) {
      if (value.getElementsByClassName('navbar__submenu').length > 0) {
        value.getElementsByClassName('navbar__submenu')[0].classList.remove('navbar__submenu-active');
      }
    };
    value.onmouseenter = function(event) {
      if (value.getElementsByClassName('navbar__submenu').length > 0) {
        value.getElementsByClassName('navbar__submenu')[0].classList.add('navbar__submenu-active');
      };
    };
  });
}

// ***************** виділення і відкриття меню при ховері
var forEach = function forEach(array, callback, scope) {
  for (var i = 0; i < array.length; i++) {
    callback.call(scope, i, array[i]);
  }
};


function change_item_amount(){

    var data = $(".form_product_item").serialize().split("&");

    var obj = {};
    for (var key in data) {
      obj[data[key].split("=")[0]] = data[key].split("=")[1];
    }

  fetch('/change_item_amount/', {
      method: 'POST',
      body: new URLSearchParams($.param(obj))
    })
    .then(data => {

      return data.json();
    })
    .then(data => {
      console.log(data);
      $('.product__control .add_basket').text('Тoвар в корзині');
      $('.basket__count span').text(data.cart_items_quantity);
      console.log($('.basket__count .items_counter'));
      $('.product__control .add_basket').addClass('btn-disable');
    })
}



function change_cart_item_amount(e) {

  if (e.target.classList.contains('plus-btn')) {
    var input = e.target.nextElementSibling;
    var quantity = parseInt(input.value) + 1;
    if (isNaN(quantity) || quantity < 1) {
      quantity = 1;
    }
  } else if (e.target.classList.contains('minus-btn')) {
    var input = e.target.previousElementSibling;
    var quantity = parseInt(input.value) - 1;
    if (isNaN(quantity) || quantity < 1) {
      quantity = 1;
    }
  } else {
    var input = e.target;
    var quantity = parseInt(input.value);
    if (isNaN(quantity) || quantity < 1) {
      quantity = 1;
    }
  }
  id = input.dataset.id;
  input.value = quantity;



}
