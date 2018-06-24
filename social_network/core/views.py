from django.contrib.auth import login, authenticate
from ..forms import SignUpForm
from django.shortcuts import render, redirect


def signup(request):
    """
    Sign up new users.
    :param request:
    :return:
    """

    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        next_page = request.POST.get('next')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(next_page or 'home')

    return render(request, 'registration/signup.html', {'form': form})
