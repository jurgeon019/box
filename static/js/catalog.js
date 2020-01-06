$(document).ready(function() {

  var namber_page = 1,
    last_page;

  var catalog_categories = document.getElementsByClassName("category_slug")[0].value; // категорія товару помістити в ajax при загрузці сторінок
// console.log( document.getElementsByClassName("category_slug")[0]);
  upadate_card_product({
    category: catalog_categories,
    // per_page: namber_page
  }, false)

  $('.btn_more').on('click', function() {
    $('.btn_more').toggleClass('btn_more-active');

    // Сірі картки для анімації початок
    var list_card_animation = document.createDocumentFragment();
    for (let i = 0; i < 4; i++) {
      var card_animation = document.createElement('div');
      card_animation.classList.add('card', 'tile', 'tile-active');
      list_card_animation.appendChild(card_animation);
    }
    document.getElementsByClassName('catalog__all')[0].appendChild(list_card_animation);
    // Сірі картки для анімації кінець

    fetch('/get_items/', {
        method: 'POST',
        body: new URLSearchParams($.param({
          category: catalog_categories,
          // per_page: namber_page
        }))
      })
      .then(data => {
        return data.json();
      })
      .then(data => {
        last_page = data.last_page;
        if (last_page >= namber_page) {
          namber_page++;
          fetch('/get_items/', {
            method: 'POST',
            body: new URLSearchParams($.param({
              category: catalog_categories,
              // per_page: 1,
              page: namber_page
            }))
          })
          .then(data => {
            return data.json();
          })
          .then(value => {

            var product = value.paginated_items;
            var fragment = document.createDocumentFragment();
            var cur_step = 0;
            for (var key in product) {
              cur_step = cur_step + 0.3;
              var creat_card1 = creat_card(product[key], cur_step);
              fragment.appendChild(creat_card1);
            }
            $('.tile').remove();
            document.getElementsByClassName('catalog__all')[0].appendChild(fragment);

            scrol_cart = $($('.card-anime')[0]).offset().top

            $("html, body").animate({
              scrollTop: scrol_cart - $('.card-anime').height()
            }, "slow");

            $('.card').removeClass('card-anime');
            $('.card').removeClass('block');
            $('.btn_more').toggleClass('btn_more-active');


            if (last_page < namber_page || last_page == namber_page) {
              $('.btn_more').remove();
            }
          })
        }
      })
  });

  $('.sort_select_item').on('click', function() {
    $('.card').remove();
    console.log($('.sort_select_item').data('id'));
    upadate_card_product({ category: catalog_categories,   per_page: namber_page }, true)
  })
})

function upadate_card_product(param_fetch, delete_prev_card) {
  // param_fetch // - json to send server
  // delete_prev_card // -- delete prev card in catalog
  let data_json = new URLSearchParams($.param(param_fetch))

  if (delete_prev_card === true) {
    // Сірі картки для анімації початок
    var list_card_animation = document.createDocumentFragment();
    for (let i = 0; i < 4; i++) {
      var card_animation = document.createElement('div');
      card_animation.classList.add('card', 'tile', 'tile-active');
      list_card_animation.appendChild(card_animation);
    }
    document.getElementsByClassName('catalog__all')[0].appendChild(list_card_animation);
    // Сірі картки для анімації кінець
  }

  fetch('/get_items/', {
      method: 'POST',
      body: data_json
    })
    .then(data => {
      return data.json();
    })
    .then(value => {
    if (value.paginated_items.length>0) {
      last_page = value.last_page;
      console.log(value);
      var product = value.paginated_items;
      var fragment = document.createDocumentFragment();
      var cur_step = 0;
      for (var key in product) {
        cur_step = cur_step + 0.3;
        var creat_card1 = creat_card(product[key], cur_step);
        fragment.appendChild(creat_card1);
      }
      $('.card').remove();
      document.getElementsByClassName('catalog__all')[0].appendChild(fragment);
      console.log($('.card-anime').height());
      console.log(scrol_cart = $($('.card-anime')[0]).offset().top);
      $("html, body").animate({
        scrollTop: scrol_cart - $('.card-anime').height()
      }, "slow");
      $('.card').removeClass('card-anime');

}else {
  $('.btn_more').hide();
  $('.secrch__wrap_container_feil').addClass('secrch__wrap_container_feil-active')
}
    })
}
function creat_card(product, step) {
// console.log(product);
// console.log(step  );
  var card_product = document.createElement('div');
  card_product.style.setProperty('animation-delay', (step) + 's', '');

  card_product.classList.add('card', 'block', 'card-anime');
  var card__img = document.createElement('div');
  card__img.classList.add('card__img');
  var card__img_phoro = document.createElement('img');
// console.log(product.images.length);
  if (product.images.length > 0) {
    // console.log(product.images[0]);
    card__img_phoro.setAttribute('src', product.images[0].image);
    card__img_phoro.setAttribute('alt', product.images[0].alt);
  }


  card__img.appendChild(card__img_phoro);
  card_product.appendChild(card__img);

  var card_main = document.createElement('div');
  card_main.classList.add('card_main');

  var card_main__text = document.createElement('div');
  card_main__text.classList.add('card_main__text', 'card__related_main__text');

  var subtitle = document.createElement('div');
  subtitle.classList.add('subtitle');
  subtitle.textContent = product.subname;

  var title = document.createElement('a');
  title.classList.add('title');
  title.classList.add('title-card_list');
  title.setAttribute(`href`, `/item/${product.slug}`);
  title.textContent = product.title;

  var price = document.createElement('div');
  price.classList.add('price');
  price.textContent = product.price + ' грн';

  card_main__text.appendChild(subtitle);
  card_main__text.appendChild(title);
  card_main__text.appendChild(price);
  card_main.appendChild(card_main__text);

  card_product.appendChild(card_main);
  return card_product;
}
