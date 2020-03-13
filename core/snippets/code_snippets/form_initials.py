def edit(request, id):
    if request.method == 'GET':
        obj = Database.objects.get(id=id)


        #!!!

        # form = DataForm({'first_name':obj.first_name,
        #                 'last_name':obj.last_name,
        #                 'age':obj.age
        #                   }
        # )
        # form = DataForm(initial={
        #                     'first_name':obj.first_name,
        #                     'last_name':obj.last_name,
        #                     'age':obj.age
        #                 }
        # )
        form = DataForm(instance=obj)

        #!!!


        print(obj)
        # print(form.instance)
        return render(request, 'app/edit.html', {'obj':obj, 'form':form})
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            # obj = Database.objects.get(id=id)
            # obj.first_name = form.cleaned_data.get('first_name')
            # form.save()
            # obj.last_name = form.cleaned_data.get('last_name')
            # obj.age = form.cleaned_data.get('age')
            # obj.save()
            form.save()
            return redirect(reverse('index'))