$(function() {

  Onload();
})

/**
 * valide_form - Валідація форм
 * @param {selector form} ID Форми на яку підвішують валідацію
 * @param {class name} class групи куди виводять помилки
 * @param {bull} true Чи виводи вспливайку пісял відповіді ajax
 *
 **/

function Onload() {

  valide_form('#basket_form', '.group_box', false);
  valide_form('#contact__form', '.form__row', true);
  valide_form('#create_review', '.group_box', true);


  valide_form('#form-register', '.group_box', false);
  valide_form('#form-login', '.group_box', false);
  valide_form('#contact-us__form', '.form__row', true);
  valide_form('#form-order-credit', '.group_box', true);

}

function location_leng() {
  return location.pathname.split('/')[1];
}

function valide_form(id_form, append_error_box, check_request) {
  var check_request = check_request;
  if ($(id_form).length > 0) {

    var lang_site;
    var errore_text = {};

    lang_site = location_leng();
    console.log(id_form);
    switch (lang_site) {
      case 'uk':
        errore_text.required = 'Поле обов\'язково для заповнення';
        errore_text.email = 'Поле має містити email';
        break;
      case 'ru':
        errore_text.required = 'Поле обязательно для заполнения';
        errore_text.email = 'Поле должно содержать email';
        break;
      case 'en':
        errore_text.required = 'The field is required';
        errore_text.email = 'The field must contain an email';
        break;
      default:
        errore_text.required = 'Поле обов\'язково для заповнення.';
        errore_text.email = 'Поле має містити email.';
    }

    $(id_form).validate({
      errorPlacement: function(event, validator) {
        $(validator).parents(append_error_box).append($(event));
      },
      rules: {
        name: {
          required: true,
        },
        email: {
          required: true,
          email: true,
        },
        user_last_name: {
          required: true,
        },
        payment: {
          required: true,
        },
        phone: {
          required: true,
        },
        address: {
          required: true,
        },
        pass: {
          required: true,
        },
        repeat_pass: {
          required: true,
        },
        text: {
          required: true,
        },
      },

      messages: {
        name: {
          required: errore_text.required,
          email: errore_text.email
        },
        email: {
          required: errore_text.required,
        },
        user_last_name: {
          required: errore_text.required,
        },
        payment: {
          required: errore_text.required,
        },
        phone: {
          required: errore_text.required,
        },
        address: {
          required: errore_text.required,
        },
        pass: {
          required: errore_text.required,
        },
        repeat_pass: {
          required: errore_text.required,
        },
        text: {
          required: errore_text.required,
        },
      },

      submitHandler: function(form) {

        $('.loader_all').addClass('loader_all-active');
        var loader = '<div class="lds-default"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>';
        document.getElementById('loader_all__wrap').innerHTML = loader;''
        console.log($(form).serialize());
        console.log($(form).serializeArray());
        // var  data = $(form).serializeArray();
         var form_input = $(form).serializeArray();
        // var data = $(form).serialize().split("&");
        var url_form = form.action;
        var form_json = {};
        // for (var key in data) {
        //   obj[data[key].split("=")[0]] = data[key].split("=")[1];
        // }
        $(form_input).each(function(index, obj) {
          console.log(obj);
          console.log(index);
          form_json[obj.name] = obj.value;

          console.log(form_json);
        });

console.log(form_json);
        if(url_form != ''){

          fetch(url_form, {
            method: 'POST',
            body: new URLSearchParams($.param(form_json))
          })
          .then(data => {

            return data.json();
          })
          .then(data => {
            if(data.status=='OK' && typeof data['status'] !== "undefined"){
                sayHi();
            }
            if(typeof data['url'] !== "undefined" && data.url!=''){
                sayHi();
                location.href=data.url;
            }
            if(typeof data['review'] !== "undefined" ){
                sayHi_rewis();


             document.getElementsByClassName('product_reviews-list')[0].appendChild(creat_reviews(data.review));

            }


          })

        }else {
          console.log("forn_not_actions");
        }

        function sayHi() {
          $('.loader_all').removeClass('loader_all-active');
          $.fancybox.close();
          if (check_request === true) {
            $.fancybox.open({
              src: '#form_send_ok',
            });

            var form_inputs = $(form)[0].querySelectorAll('input');
            if (form_inputs.length > 0) {
              for (var key in form_inputs) {
              if (form_inputs.hasOwnProperty(key) && /^0$|^[1-9]\d*$/.test(key) && key <= 4294967294) {
                  if (form_inputs[key].type !== 'submit') {
                    form_inputs[key].value = '';
                  }
                }

              }
            }

            var form_textaria = $(form)[0].querySelectorAll('textarea');
            if (form_textaria.length > 0) {
              form_textaria[0].value = '';
            }

          }
        }
        function sayHi_rewis() {
          $('.loader_all').removeClass('loader_all-active');
          $.fancybox.close();
          if (check_request === true) {
            $.fancybox.open({
              src: '#form_send_ok_rewis',
            });

            var form_inputs = $(form)[0].querySelectorAll('input');
            if (form_inputs.length > 0) {
              for (var key in form_inputs) {
              if (form_inputs.hasOwnProperty(key) && /^0$|^[1-9]\d*$/.test(key) && key <= 4294967294) {
                  if (form_inputs[key].type !== 'submit') {
                    form_inputs[key].value = '';
                  }
                }

              }
            }

            var form_textaria = $(form)[0].querySelectorAll('textarea');
            if (form_textaria.length > 0) {
              form_textaria[0].value = '';
            }

          }
        }

        function creat_reviews(props){
          console.log(props);
           var reviews = document.createElement("div");
              reviews.classList.add('reviews');
           var reviews_header = document.createElement("div");
              reviews_header.classList.add('reviews-header');
           var reviews__left_part = document.createElement("div");
              reviews__left_part.classList.add('reviews__left-part');

           var reviews_author = document.createElement("div");
              reviews_author.classList.add('reviews-author');
              reviews_author.textContent = props.name;
           var reviews_date = document.createElement("div");
              reviews_date.classList.add('reviews-date');
              reviews_date.textContent = props.created;


              reviews__left_part.appendChild(reviews_author);
              reviews__left_part.appendChild(reviews_date);
            reviews_header.appendChild(reviews__left_part);
          reviews.appendChild(reviews_header);

           var right__right_part = document.createElement("div");
              right__right_part.classList.add('right__right-part');

           var info__star = document.createElement("div");
              info__star.classList.add('info__star');
           var info__star_wrap = document.createElement("div");
              info__star_wrap.classList.add('info__star_wrap');
           var info__star_item = document.createElement("div");
              info__star_item.classList.add('info__star_item');

           var info__star_icon = document.createElement("img");
              info__star_icon.src = '/static/img/svg/star.svg';

              // info__star_item.appendChild(info__star_icon);
              info__star_wrap.appendChild(info__star_item);
            info__star.appendChild(info__star_wrap);

  right__right_part.appendChild(info__star);
    reviews_header.appendChild(right__right_part);
            var reviews_main = document.createElement("div");
               reviews_main.classList.add('reviews-main');
               reviews_main.textContent = props.text;
            reviews.appendChild(reviews_main);


            return reviews;

        }


      }
    });
  }

}
