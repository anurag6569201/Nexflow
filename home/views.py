from django.shortcuts import render, redirect, get_object_or_404
from home import models
from .forms import READMEForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import markdown2



@login_required
def home(request):
    readme, _ = models.UserProfileREADME.objects.get_or_create(user=request.user)
    # Convert Markdown content to HTML
    readme_html = markdown2.markdown(
        readme.content, 
        extras=["fenced-code-blocks", "tables", "images"]
    )

    user_profile_data, _ = models.UserProfile.objects.get_or_create(user=request.user)
    context={
        'readme_html': readme_html,
        'user_profile_data':user_profile_data,
    }
    print(readme)
    return render(request, 'apps/home/profile.html',context)

@login_required
def readme_edit(request):
    readme, created = models.UserProfileREADME.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = READMEForm(request.POST, instance=readme)
        if form.is_valid():
            form.save()
            messages.success(request, "README updated successfully.")
            return redirect('home:home')
    else:
        form = READMEForm(instance=readme)
    return render(request, 'apps/home/readme_edit.html', {'form': form})
