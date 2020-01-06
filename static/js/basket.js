$(document).ready(function() {

      // ************Корзина
      $('.btn-next-step').on('click', function() {
        $('.contact_user').toggleClass('contact_user-active');
        $('.basket').toggleClass('basket-active');
        $('.step-one').addClass('step-done');
        $('.step-two').addClass('step-action');
      })
      $('.step-two').on('click', function() {
        $('.contact_user').addClass('contact_user-active');
        $('.basket').removeClass('basket-active');
        $('.step-one').addClass('step-done');
        $('.step-two').addClass('step-action');
      });
      $('.step-one').on('click', function() {
        if ($(this).hasClass('step-done')) {
          $('.step-one').removeClass('step-done');
          $('.contact_user').toggleClass('contact_user-active');
          $('.basket').toggleClass('basket-active');
          $('.step-two').removeClass('step-action');
        };
      })



      if ($('.basket__main').length > 0) {
        fetch('/get_cart_items/', {
            method: 'POST',
          })
          .then(data => {
            return data.json();
          })
          .then(data => {
            // console.log(data);
            // console.log(data);
            // console.log(data.cart_items_quantity);

            if (data.cart_items_quantity > 0) {
              $('.basket__count span').text(data.items_amount);
              $('.filled_basket').addClass('basket_wrap-active');
              $('.not_filled_basket').removeClass('basket_wrap-active');
              $('.basket__footer_price-value').text(data.cart_total_price+ ' грн');
            }else {
              $('.filled_basket').removeClass('basket_wrap-active');
              $('.not_filled_basket').addClass('basket_wrap-active');
            }






            forEach(data.cart_items, function(index, value) {
              console.log(value);
              document.querySelectorAll('.basket-active .basket__main')[0].appendChild(basket_add_item(value));


            })
            delete_item();
            count_produtc_upadate();
          })

      }

      function basket_add_item(object) {
        // console.log(object);
        var basket__item = document.createElement('div');
        basket__item.classList.add('basket__item');
        var product__basket_id = document.createElement('input');
        product__basket_id.classList.add('product__basket_id');
        product__basket_id.type = "hidden";
        product__basket_id.setAttribute("name", "cart_item_id");
        product__basket_id.setAttribute("value", object.id);
        basket__item.appendChild(product__basket_id);

        var basket__group_col_1 = document.createElement('div');
        basket__group_col_1.classList.add('basket__group_col-1');

        var basket__item_img = document.createElement('div');
        basket__item_img.classList.add('basket__item_img');
        var basket__item_img_img = document.createElement('img');



        if (object.item.images.length > 0) {
          basket__item_img_img.src = object.item.images[0].image;
          // console.log(object.item.images[0].alt);
          basket__item_img_img.alt = object.item.images[0].alt;
        }

        basket__item_img.appendChild(basket__item_img_img);

        var basket__item_title = document.createElement('div');
        basket__item_title.classList.add('basket__item_title');
        var basket__item_title_div = document.createElement('div');
        if (object.item.title) {
          basket__item_title_div.innerText = object.item.title;
        }

        basket__item_title.appendChild(basket__item_title_div);

        basket__group_col_1.appendChild(basket__item_img);
        basket__group_col_1.appendChild(basket__item_title);

        var basket__group_col_2 = document.createElement('div');
        basket__group_col_2.classList.add('basket__group_col-2');

        var basket__group_col_2_mod = document.createElement('div');
        basket__group_col_2_mod.classList.add('basket__group_col-2_mod');

        var basket__item_quantity = document.createElement('div');
        basket__item_quantity.classList.add('basket__item_quantity');

        var product__quantity_count = document.createElement('input');
        product__quantity_count.type = "text";
        product__quantity_count.classList.add('product__quantity_count', 'product__quantity_count-cadr');
        product__quantity_count.setAttribute("data-id", object.id);
        product__quantity_count.setAttribute("name", "quantity");
        product__quantity_count.setAttribute("value", object.quantity);
        product__quantity_count.setAttribute("min", "1");
        basket__item_quantity.appendChild(product__quantity_count);

        var basket__item_price = document.createElement('div');
        basket__item_price.classList.add('basket__item_price');
        var basket__item_price_div = document.createElement('div');
        basket__item_price_div.innerText = object.item.price;
        basket__item_price.appendChild(basket__item_price_div);
        basket__item_price.appendChild(basket__item_price_div);

        basket__group_col_2_mod.appendChild(basket__item_quantity);
        basket__group_col_2_mod.appendChild(basket__item_price);

        var basket__item_delete = document.createElement('div');
        basket__item_delete.classList.add('basket__item_delete');
        var basket__item_delete_ico = document.createElement('div');
        basket__item_delete_ico.classList.add('basket__item_delete_ico');
        basket__item_delete_ico.innerHTML = '<svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="trash-alt" class="svg-inline--fa fa-trash-alt fa-w-14" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"> <path fill="#cccccc" d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12zM432 80h-82.41l-34-56.7A48 48 0 0 0 274.41 0H173.59a48 48 0 0 0-41.16 23.3L98.41 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0-16-16zM171.84 50.91A6 6 0 0 1 177 48h94a6 6 0 0 1 5.15 2.91L293.61 80H154.39zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12z"> </path> </svg>'
        basket__item_delete.appendChild(basket__item_delete_ico);
        basket__group_col_2_mod.appendChild(basket__item_delete);

        basket__group_col_2.appendChild(basket__group_col_2_mod);

        basket__item.appendChild(basket__group_col_1);
        basket__item.appendChild(basket__group_col_2);

        return basket__item;

      }

      function delete_item() {
        $('.basket__item_delete').on('click', function() {
          var delete_basket_item = $(this).parents('.basket__item');
          var delete_basket_item_id = $(this).parents('.basket__item')[0].querySelector('.product__basket_id').value;

          fetch('/remove_cart_item/', {
              method: 'POST',
              body: new URLSearchParams($.param({
                cart_item_id: delete_basket_item_id
              }))
            })
            .then(data => {
              $(delete_basket_item).remove();

              fetch('/get_cart_items/', {
                  method: 'POST',
                })
                .then(data => {
                  return data.json();
                })
                .then(data => {
                  // console.log(data);
                  if (data.cart_items_quantity > 0) {
                    $('.basket__count span').text(data.cart_items_quantity);
                  }
                  if (data.cart_total_price > 0) {
                    $('.basket__footer_price-value').text(data.cart_total_price);
                  }

                })
            })
        })

      }

      function count_produtc_upadate() {
        $('.product__quantity_count').on('change', function(e) {

            var delete_basket_item_id = $(this).parents('.basket__item')[0].querySelector('.product__basket_id').value;
            change_cart_item_amount(e,delete_basket_item_id,$(this)[0].value);
        })
        function change_cart_item_amount(e,id,quantity) {


          var input = e.target;
          var quantity = parseInt(input.value);
          if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
          }

          id = input.dataset.id;
          input.value = quantity;
          fetch('/change_cart_item_amount/', {
              method: 'POST',
              body: new URLSearchParams($.param({
                cart_item_id: id,
                quantity: quantity
              }))
            })
            .then(data => {
              return data.json();
            })
            .then(data => {

            if (data.cart_total_price > 0) {
              $('.basket__footer_price-value').text(data.cart_total_price + ' грн');
            }
            if (data.cart_items_quantity > 0) {
              $('.basket__count span').text(data.cart_items_quantity );
            }
            })
        }

        }


      });
