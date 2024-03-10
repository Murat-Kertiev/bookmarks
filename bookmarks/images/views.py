from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        cd = form.cleaned_data
        new_image = form.save(commit=False)
        new_image.user = request.user
        new_image.save()
        messages.success(request,
                         'Image added successfully')
        return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    context = {
        'section': 'images',
        'form': form
    }
    return render(request, 'images/image/create.html', context)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    context = {
        'section': 'images',
        'image': image,
    }
    return render(request, 'images/image/detail.html', context)


def image_like(request):
    image = request.POST.get('id')
    action = request.POST.get('action')
    if image and action:
        try:
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
