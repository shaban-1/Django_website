from gc import get_objects
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from unicodedata import category

from .forms import NewItemForm
from .models import Item

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    context  = {
        'item' : item,
        'related_items' : related_items
    }
    return render(request,  'item/detail.html' , context)

@login_required
def new(request):
    if(request.method == 'POST'):
        form = NewItemForm(request.POST, request.FILES)

        if(form.is_valid()):
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    context = {
        'form' : form,
        'title' : 'New item'
    }
    return render(request, 'item/form.html', context)