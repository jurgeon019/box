// from django.core.management.base import BaseCommand

// from box.shop.item.utils import get_categories_from_csv


// class Command(BaseCommand):

//   def add_arguments(self, parser):
//     parser.add_argument(
//       'file_name',
//       type=str,
//       help='File, that contains the main item\'s information'
//     )

//   def handle(self, *args, **kwargs):
//     filename = kwargs['file_name']
//     status   = read_categories_from_csv(filename)
//     if status:
//       self.stdout.write(self.style.SUCCESS('Data imported successfully'))
//     else:
//       self.stdout.write(self.style.ERROR('Data import FAILED'))



























function create_cards(e){
    // $.ajax({
    //     url:'mottoex.com.ua/get_items/',
    //     method:'POST',
    //     async: true,
    //     success: function(data){
    //         console.log(data)
    //     }
    // })
    var items = [
        {
            title: "Трактор 1",
            price: "24.333 $",
            image: "img/sellings/14905.png",
            id:1
        },
        {
            title: "Трактор 2",
            price: "14.333 $",
            image: "img/sellings/14905.png",
            id:2
        },
        {
            title: "Трактор 3",
            price: "124.333 $",
            image: "img/sellings/14905.png",
            id:3
        },
        {
            title: "Трактор 4",
            price: "124.444 $",
            image: "img/sellings/14905.png",
            id:4
        },
    ]
    var box = document.querySelector('.catalog-selling-cards');
    var content = '';
    items.forEach(function(item){
        content += `
            <div class="catalog-selling-cards__card">
                <img src="${item.image}" alt="traktor" class="catalog-selling-cards__card-img">
                <p class="catalog-selling-cards__card-name">${item.title}</p>
                <p class="catalog-selling-cards__card-price">${item.price}</p>
            </div>
        `;
    })
    box.innerHTML += content
}
document.addEventListener('DOMContentLoaded', function(e){
    var load_more_btn = document.querySelector('.catalog-selling-cards__btn')
    load_more_btn.addEventListener('click', create_cards)
})


