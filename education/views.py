from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import *
from .models import *
from users.models import *

from youtubesearchpython import VideosSearch
import wikipedia
import requests


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'
    form_class = MessageForm
    redirect_authenticated_user = True

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:  
            return redirect('dashboard')
        return super(HomeView, self).get(*args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = reverse_lazy('login')

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     print(self.request.user.id)
    #     context['book_list'] = self.request.user
    #     return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = reverse_lazy('login')

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'profile-update.html'
    login_url = reverse_lazy('login')

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user)

        if user_form.is_valid() and profile_form.is_valid():    
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'education/notes.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['notes'] = context['notes'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context


class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('notes')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('notes')
    login_url = reverse_lazy('login')


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    context_object_name = 'note'
    success_url = reverse_lazy('notes')
    login_url = reverse_lazy('login')


@login_required(login_url="login")
def UdemyView(request):
    if request.method == "POST":
        search_input = request.POST['search-area']
        url = "https://www.udemy.com/api-2.0/courses/?search="+search_input+"&price=price-free&language=en&ordering=relevance"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Basic {BASE64_ENCODED(CLIENT_ID:CLIENT_SECRET)}",
            "Content-Type": "application/json;charset=utf-8"
        }
        r = requests.get(url, headers=headers)
        answer = r.json()

        result_list = []

        for i in range(12):
            result_dict = {
                'title': answer['results'][i]['title'],
                'url': answer['results'][i]['url'],
                'price': answer['results'][i]['price'],
                'instructors': answer['results'][i]['visible_instructors'][0]['display_name'],
                'headline': answer['results'][i]['headline'],
                'image': answer['results'][i]['image_480x270'],
            }

            result_list.append(result_dict)
        context = {
            'courses': result_list,
        }
        return render(request, "education/udemy.html", context)
    
    url = "https://www.udemy.com/api-2.0/courses/?price=price-free&language=en&ordering=relevance"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Basic {BASE64_ENCODED(CLIENT_ID:CLIENT_SECRET)}",
        "Content-Type": "application/json;charset=utf-8"
    }
    r = requests.get(url, headers=headers)
    answer = r.json()

    result_list = []

    for i in range(12):
        result_dict = {
            'title': answer['results'][i]['title'],
            'url': answer['results'][i]['url'],
            'price': answer['results'][i]['price'],
            'instructors': answer['results'][i]['visible_instructors'][0]['display_name'],
            'headline': answer['results'][i]['headline'],
            'image': answer['results'][i]['image_480x270'],
        }

        result_list.append(result_dict)
    context = {
        'courses': result_list,
    }
    return render(request, "education/udemy.html", context)



@login_required(login_url="login")
def YouTubeView(request):
    # template_name = 'education/youtube.html'
    # context_object_name = 'videos'

    # def post(self, request):
    if request.method == "POST":
        search_input = request.POST['search-area']

        videos = VideosSearch(search_input, limit=9)
        result_list = []
        for i in videos.result()['result']:
            result_dict = {
                'input': search_input,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                # 'channel': i['channel']['name'],
                'link': i['link'],
                # 'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            # desc = ''
            # if i['descriptionSnippet']:
            #     for j in i['descriptionSnippet']:
            #         desc += j['text']
            # result_dict['description'] = desc
            result_list.append(result_dict)

        context = {
            'videos': result_list
        }
        return render(request, "education/youtube.html", context)

    return render(request, "education/youtube.html")

    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


@login_required(login_url="login")
def BooksView(request):
    # template_name = 'education/books.html'
    # context_object_name = 'books'

    # def post(self, request):
    if request.method == "POST":
        search_input = request.POST['search-area']
        url = "https://www.googleapis.com/books/v1/volumes?q="+search_input
        r = requests.get(url)
        answer = r.json()

        result_list = []

        for i in range(9):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                # 'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                # 'description': answer['items'][i]['volumeInfo'].get('description'),
                # 'author': answer['items'][i]['volumeInfo'].get('authors'),
                # 'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('averageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }

            result_list.append(result_dict)

        context = {
            'books': result_list
        }
        return render(request, "education/books.html", context)

    return render(request, "education/books.html")

    # def get(self, request):
    #     return self.post(request)


@login_required(login_url="login")
def DictionaryView(request):
    # template_name = 'education/dictionary.html'
    # context_object_name = 'books'
    # http_method_names = ['get', 'post']

    # def post(self, context):
    if request.method == "POST":
        search_input = request.POST['search-area']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+search_input
        r = requests.get(url)
        answer = r.json()

        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            partOfSpeech = answer[0]['meanings'][0]['partOfSpeech']
            origin = answer[0]['origin']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
                'input': search_input,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'partOfSpeech': partOfSpeech,
                'origin': origin,
                'example': example,
                'synonyms': synonyms,
            }
        except:
            context = {
                'input': ''
            }
        return render(request, "education/dictionary.html", context)

    return render(request, "education/dictionary.html")


@login_required(login_url="login")
def WikiView(request):

    if request.method == "POST":
        search_input = request.POST['search-area']
        
        search = wikipedia.page(search_input)

        context = {
            'title': search.title,
            'link': search.url,
            'details': search.summary,
        }
        return render(request, "education/wiki.html", context)

    return render(request, "education/wiki.html")


def sendEmail(request):
    
    if request.method == 'POST':    
        template = render_to_string('email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['body'],
			})
            
        email = EmailMessage(
			request.POST['phone_number'],
			template,
			settings.EMAIL_HOST_USER,
			['codenameberyl@gmail.com']
			)
            
        email.fail_silently=False
        email.send()

        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, 'Thank you for contacting us, We will get back to you shortly.')
        
    return redirect('home')


# Error Views
def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)

# def error_500(request):
#         data = {}
#         return render(request,'500.html', data)

# def error_403(request, exception):
#         data = {}
#         return render(request,'403.html', data)

# def error_400(request,  exception):
#         data = {}
#         return render(request,'400.html', data)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    fields = '__all__'
    redirect_authenticated_user = True

    def form_valid(self, form):

        remember_me = form.cleaned_data['remember_me'] # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0) # if remember me is self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')


class SignUpView(FormView):
    template_name = 'register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:  
            return redirect('dashboard')
        return super(SignUpView, self).get(*args, **kwargs)
