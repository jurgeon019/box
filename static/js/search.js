$(document).ready(function() {

  if($('.blog_search ').length>0){
    $('.search__input').val(sessionStorage.search__site);
    $('.secrch_title_requesdt').text(sessionStorage.search__site);
  console.log(sessionStorage.search__site);
  console.log(sessionStorage.search__site);
    if(sessionStorage.search__site !== ''){
      fetch('/get_items/', {
          method: 'POST',
          body: new URLSearchParams($.param({
            q: sessionStorage.search__site,
          }))
        })
        .then(data => {
          return data.json();
        })
        .then(value => {
             if (value.paginated_items.length>0) {
            last_page = value.last_page;
            // console.log(value);
            var product = value.paginated_items;
            var fragment = document.createDocumentFragment();
            var cur_step = 0;
            // console.log(product);
            for (var key in product) {
              cur_step = cur_step + 0.2;
              var creat_card1 = creat_card(product[key], cur_step);
              fragment.appendChild(creat_card1);
            }
            $('.card').remove();
            document.getElementsByClassName('catalog__all')[0].appendChild(fragment);
            // console.log($('.card-anime').height());
           scrol_cart = $($('.card-anime')[0]).offset().top;
            $("html, body").animate({
              scrollTop: scrol_cart - $('.card-anime').height()
            }, "slow");
            $('.card').removeClass('card-anime');
          }else {
            $('.secrch__wrap_container_feil').addClass('secrch__wrap_container_feil-active')
          }

        })
    }

  }
  if($('.secrch').length>0){
    $('.search__input').val(sessionStorage.search__site);
    $('.secrch_title_requesdt').text(sessionStorage.search__site);
  console.log(sessionStorage.search__site);
  console.log(sessionStorage.search__site);
    if(sessionStorage.search__site !== ''){
      fetch('/get_items/', {
          method: 'POST',
          body: new URLSearchParams($.param({
            q: sessionStorage.search__site,
          }))
        })
        .then(data => {
          return data.json();
        })
        .then(value => {
             if (value.paginated_items.length>0) {
            last_page = value.last_page;
            // console.log(value);
            var product = value.paginated_items;
            var fragment = document.createDocumentFragment();
            var cur_step = 0;
            // console.log(product);
            for (var key in product) {
              cur_step = cur_step + 0.2;
              var creat_card1 = creat_card(product[key], cur_step);
              fragment.appendChild(creat_card1);
            }
            $('.card').remove();
            document.getElementsByClassName('catalog__all')[0].appendChild(fragment);
            // console.log($('.card-anime').height());
           scrol_cart = $($('.card-anime')[0]).offset().top;
            $("html, body").animate({
              scrollTop: scrol_cart - $('.card-anime').height()
            }, "slow");
            $('.card').removeClass('card-anime');
          }else {
            $('.secrch__wrap_container_feil').addClass('secrch__wrap_container_feil-active')
          }

        })
    }

  }
  })



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
  title.setAttribute('href', '/product_card.html');
  title.textContent = product.title;

  var price = document.createElement('div');
  price.classList.add('price');
  price.textContent = `${product.price} ${product.currency}`;

  card_main__text.appendChild(subtitle);
  card_main__text.appendChild(title);
  card_main__text.appendChild(price);
  card_main.appendChild(card_main__text);

  card_product.appendChild(card_main);
  return card_product;
}
