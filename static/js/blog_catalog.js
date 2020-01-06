$(document).ready(function() {
  var namber_page = 1,
    last_page;

  $('.blog-catalog__pagen-item').on('click', function() {
    $('.blog-catalog__pagen-item').removeClass('blog-catalog__pagen-item-active');
    $(this).addClass('blog-catalog__pagen-item-active');

  })

  $('.blog_search input').on('click', function() {
    $(this).parents('.search__form').addClass('search__form-blog');
    $(this).parents('.search__form').addClass('search__form-focus ');
  })
  $('.blog_search .search').on('click', function() {
    if ($(this).val() === '') {
      $(this).parents('.search__form').removeClass('search__form-blog')
      $(this).parents('.search__form').removeClass('search__form-focus')
    }
  })






  $('.blog_search-next').on('click', function() {
    if ($(this).parents('.search__form')[0].querySelector('input').value === '') {
      $('.search__form').removeClass('search__form-focus')
    } else {
      var querySearch = $(this).parents('.search__form')[0].querySelector('input').value;
      sessionStorage.setItem('search__blog', querySearch);

      if (querySearch !== '') {

        var post_categorie = $('.post_categorie').val()
        // Сірі картки для анімації початок
        var list_card_animation = document.createDocumentFragment();
        for (let i = 0; i < 4; i++) {
          var card_animation = document.createElement('div');
          card_animation.classList.add('card', 'tile', 'tile-active');
          list_card_animation.appendChild(card_animation);
        }
        document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(list_card_animation);
        // Сірі картки для анімації кінець

        fetch('/search_posts/', {
            method: 'POST',
            body: new URLSearchParams($.param({
              q: querySearch,
              category: post_categorie,
            }))
          })
          .then(data => {
            return data.json();
          })
          .then(data => {
            update_past_card(data.posts);
            $('.btn_more').remove();
          })
      }
    }
  });


  $('.blog_search .search__input_blog').on('keydown', function(e) {
    if ($(this).val() !== '' && e.keyCode === 13) {
      e.preventDefault();
      var querySearch = $(this).val();
        sessionStorage.setItem('search__blog', querySearch);
      if (querySearch !== '') {

        var post_categorie = $('.post_categorie').val()
        // Сірі картки для анімації початок
        var list_card_animation = document.createDocumentFragment();
        for (let i = 0; i < 4; i++) {
          var card_animation = document.createElement('div');
          card_animation.classList.add('card', 'tile', 'tile-active');
          list_card_animation.appendChild(card_animation);
        }
        document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(list_card_animation);
        // Сірі картки для анімації кінець

        fetch('/search_posts/', {
            method: 'POST',
            body: new URLSearchParams($.param({
              q: querySearch,
              category: post_categorie,
            }))
          })
          .then(data => {
            return data.json();
          })
          .then(data => {
            update_past_card(data.posts);
          $('.btn_more').remove();
          })
      }

    }
  });



  if ($('.post_categorie').length > 0) {
    // Сірі картки для анімації початок
    var post_categorie = $('.post_categorie').val()
    console.log($('.post_categorie').val());
    if ($('.post_categorie').val() !== '') {
      var list_card_animation = document.createDocumentFragment();
      for (let i = 0; i < 4; i++) {
        var card_animation = document.createElement('div');
        card_animation.classList.add('card', 'tile', 'tile-active');
        list_card_animation.appendChild(card_animation);
      }
      document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(list_card_animation);
      // Сірі картки для анімації кінець


      fetch('/get_posts/', {
          method: 'POST',
          body: new URLSearchParams($.param({
            category: post_categorie,

          }))
        })
        .then(data => {
          return data.json();
        })
        .then(data => {

          console.log(data.page_posts);
          update_past_card(data.page_posts);
          last_page = data.last_page;
          if (last_page >= namber_page) {
            namber_page++;

          }
          if (last_page < namber_page || last_page == namber_page) {
            $('.btn_more').remove();
          }
        })
    }


  }


  if ($('.blog_page').length > 0) {
    $('.btn_more').on('click', function() {
      $('.btn_more').toggleClass('btn_more-active');
      var post_categorie = $('.post_categorie').val()
      // Сірі картки для анімації початок
      var list_card_animation = document.createDocumentFragment();
      for (let i = 0; i < 4; i++) {
        var card_animation = document.createElement('div');
        card_animation.classList.add('card', 'tile', 'tile-active');
        list_card_animation.appendChild(card_animation);
      }
      document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(list_card_animation);
      // Сірі картки для анімації кінець


      fetch('/get_posts/', {
          method: 'POST',
          body: new URLSearchParams($.param({
            category: post_categorie,
            page_number: namber_page,

          }))
        })
        .then(data => {
          return data.json();
        })
        .then(data => {
          last_page = data.last_page;
          if (last_page >= namber_page) {
            namber_page++;

          }


          var product = data.page_posts;
          var fragment = document.createDocumentFragment();
          var cur_step = 0;
          for (var key in product) {
            cur_step = cur_step + 0.3;
            var creat_card1 = creat_card_blog(product[key], cur_step);
            fragment.appendChild(creat_card1);
          }
          $('.tile').remove();
          document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(fragment);

          scrol_cart = $($('.card-anime')[0]).offset().top

          $("html, body").animate({
            scrollTop: scrol_cart - $('.card-anime').height()
          }, "slow");

          $('.blog-catalog__item').removeClass('card-anime');
          $('.blog-catalog__item').removeClass('block');
          $('.btn_more').toggleClass('btn_more-active');

          if (last_page < namber_page || last_page == namber_page) {
            $('.btn_more').remove();
          }
        })
    });

  }

  function update_past_card(product_items) {
    $('.blog-catalog__item').remove();

    // Сірі картки для анімації початок
    var list_card_animation = document.createDocumentFragment();
    for (let i = 0; i < 4; i++) {
      var card_animation = document.createElement('div');
      card_animation.classList.add('card', 'tile', 'tile-active');
      list_card_animation.appendChild(card_animation);
    }
    document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(list_card_animation);
    // Сірі картки для анімації кінець


    var product = product_items;
    var fragment = document.createDocumentFragment();
    var cur_step = 0;
    for (var key in product) {
      cur_step = cur_step + 0.3;
      var creat_card1 = creat_card_blog(product[key], cur_step);
      console.log(creat_card1);
      fragment.appendChild(creat_card1);
    }
    $('.tile').remove();

    document.getElementsByClassName('blog-catalog__wrap')[0].appendChild(fragment);

    scrol_cart = $($('.card-anime')[0]).offset().top

    $("html, body").animate({
      scrollTop: scrol_cart - $('.card-anime').height()
    }, "slow");

    $('.blog-catalog__item').removeClass('card-anime');
    $('.blog-catalog__item').removeClass('block');
    $('.btn_more').removeClass('btn_more-active');





  }

  function creat_card_blog(product, step) {

    var card_blog = document.createElement('div');
    card_blog.style.setProperty('animation-delay', (step) + 's', '');
    card_blog.classList.add('blog-catalog__item', 'block', 'card-anime');



    var card_blog__img = document.createElement('div');
    card_blog__img.classList.add('blog-catalog__item_img');
    var card_blog_photo = document.createElement('img');
    // console.log(product.images.length);
    // if (product.img.length > 0) {
    // console.log(product.images[0]);
    card_blog_photo.setAttribute('src', product.image);
    // card__img_phoro.setAttribute('alt', product.images[0].alt);
    // }
    var card_blog_phoro_bg = document.createElement('div');
    card_blog_phoro_bg.classList.add('blog-catalog__item_img-bg');
    card_blog__img.appendChild(card_blog_phoro_bg);
    card_blog__img.appendChild(card_blog_photo);

    card_blog.appendChild(card_blog__img);



    var card_main = document.createElement('div');
    card_main.classList.add('blog-catalog__item_main');
    //
    var card_main__date = document.createElement('div');
    card_main__date.classList.add('blog-catalog__item_date');
    card_main__date.textContent = product.updated;

    var card_main__title = document.createElement('div');
    card_main__title.classList.add('blog-blog-catalog__item_title');
    card_main__title.textContent = product.title;

    var card_main__href = document.createElement('a');
    card_main__href.classList.add('blog-catalog__item_read-on');
    card_main__href.setAttribute(`href`, `/post/${product.slug}/`);


    var card_main__href_title = document.createElement('span');
    card_main__href_title.innerHTML = "Читати далі";

    var card_main__href_icon = document.createElement('span');
    card_main__href_icon.classList.add('icon');
    card_main__href_icon.innerHTML = '<svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="arrow-right" class="svg-inline--fa fa-arrow-right fa-w-14" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"> <path fill="currentColor" d="M190.5 66.9l22.2-22.2c9.4-9.4 24.6-9.4 33.9 0L441 239c9.4 9.4 9.4 24.6 0 33.9L246.6 467.3c-9.4 9.4-24.6 9.4-33.9 0l-22.2-22.2c-9.5-9.5-9.3-25 .4-34.3L311.4 296H24c-13.3 0-24-10.7-24-24v-32c0-13.3 10.7-24 24-24h287.4L190.9 101.2c-9.8-9.3-10-24.8-.4-34.3z"> </path> </svg>';

    card_main__href.appendChild(card_main__href_title);
    card_main__href.appendChild(card_main__href_icon);

    card_main.appendChild(card_main__date);
    card_main.appendChild(card_main__title);
    card_main.appendChild(card_main__href);

    card_blog.appendChild(card_main);
    //
    // card_product.appendChild(card_main);
    return card_blog;
  }



})
