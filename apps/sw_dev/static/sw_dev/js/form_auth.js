var login_form = document.querySelector('.login_form')

if (login_form) {
    login_form.addEventListener('submit', function(e){
        e.preventDefault();
        var data = {}
        var inputs = $(this).serializeArray();
        inputs.forEach(function(input){
            data[input.name] = input.value
        })
        $.ajax({
            url:e.target.action,
            data:data, 
            method:'POST',
            success:function(response){
                console.log(response)
            }
        })
    })
}

var logout_form = document.querySelector('.logout_form')

if (logout_form){
    logout_form.addEventListener('submit', function(e){
        e.preventDefault();
        $.ajax({
            url:e.target.action,
            method:'POST',
            success:function(response){
                console.log(response)
            }
        })
    })
}

var register_form = document.querySelector('.register_form')

if (register_form){
    register_form.addEventListener('submit', function(e){
        e.preventDefault();
        var data = {}
        var inputs = $(this).serializeArray()
        inputs.forEach(function(input){
            data[input.name] = input.value
        })
        console.log($(this)[0].action)
        $.ajax({
            url:e.target.action,
            method:'POST',
            data:data, 
            success:function(response){
                console.log(response)
            }
        })
    })
}
