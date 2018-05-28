from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import login, authenticate,logout
from hood.forms import SignUpForm,EditForm,HoodForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from hood.tokens import account_activation_token
from .models import Profile,Business,Neighborhood
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MY HOOD Account'
            message = render_to_string('registration/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('registration/account_activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/account_activation_invalid.html')
def account_activation_sent(request):
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('intro')
    return render(request, 'registration/account_activation_sent.html')

@login_required(login_url='/login')
def index(request):
    current_user = request.user
    profile = Profile.objects.all()


    return render(request, 'index.html')

@login_required(login_url='/login')
def profile(request):
    current_user = request.user
    profile_info = User.objects.get(id=current_user.id)

    edit_form = EditForm(instance=current_user)

    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('user_photo','location', 'bio','national_identity'))
    formset = ProfileInlineFormset(instance=current_user)

    if current_user.is_authenticated() and request.user.id == current_user.id:
        if request.method == "POST":
            edit_form = EditForm(request.POST,request.FILES,instance=current_user)
            formset = ProfileInlineFormset(request.POST,request.FILES,instance=current_user)

            if edit_form.is_valid():
                created_user = edit_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST,request.FILES,instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(current_user)
        return render(request, 'profile.html', {'profile_data': profile_info, "formset": formset, 'created_user': edit_form})
    else:
        raise PermissionDenied

@login_required(login_url='/login')
def profile_info(request):
    current_user = request.user

    profile_info = Profile.objects.filter(user_profile=current_user.id).all()
    for p in profile_info:
        print(p.email_confirmed)
    return render(request, 'prof_display.html', {'profile_data': profile_info})
# @login_required(login_url='/login')
# def business(request):
#     current_user = request.user
#     user_profile = Profile.objects.get(user_profile=current_user)
#     profile_instance = Profile.objects.get(id=request.user.id)
#     #n_instance = Neighborhood.objects.filter(name=user_profile.neighborhood.name)
#
#     if request.method == 'POST':
#         form = BusinessForm(request.POST, request.FILES)
#         if form.is_valid():
#             business = form.save(commit=False)
#             business.user_profile = user_profile
#
#             business.save()
#         return redirect(index)
#     else:
#         form = BusinessForm()
#     return render(request, 'business.html', {"form": form})
@login_required(login_url='/login')
def hood(request):
    current_user = request.user
    user_profile = Profile.objects.get(user_profile=current_user)
    profile_instance = Profile.objects.get(id=request.user.id)


    if request.method == 'POST':
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user_profile = user_profile

            hood.save()
        return redirect(index)
    else:
        form = HoodForm()
    return render(request, 'hood.html', {"form": form})
