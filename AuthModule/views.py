from django.urls import reverse_lazy
from django.views.generic import ListView,UpdateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import UserCreateForm



class UserListView(UserPassesTestMixin,ListView):
    template_name='pages/user_listview.html'
    model=User

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']="Usuarios"
        return context
    

class UserUpdateView(UserPassesTestMixin,UpdateView):
    template_name='pages/user_updateview.html'
    model=User
    fields=[
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    ]
    success_url=reverse_lazy('user_listview')

    def test_func(self):
        return self.request.user.is_superuser
    

class UserDeleteView(UserPassesTestMixin,UpdateView):
    template_name='user_deleteview.html'
    model=User
    fields=[
        'is_active',
    ]
    success_url=reverse_lazy('user_listview')

    def test_func(self):
        return self.request.user.is_superuser

class UserCreateView(UserPassesTestMixin, CreateView):
    form_class=UserCreateForm
    template_name = 'pages/user_createview.html'
    success_url = reverse_lazy('user_listview')

    
    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not User.objects.filter(username=form.cleaned_data['username']).exists() and form.is_valid():
                self.object = form.save()
                self.object.is_active=True
                self.object.save()
                #form.send_email()
                print("Graba al usuario")
                response = super(UserCreateView, self).form_valid(form)
            else:
                response = super(UserCreateView, self).form_invalid(form)
                print("algo fallo")
        except Exception as e:
            response = super(UserCreateView, self).form_invalid(form)
            print("entro al except")
        return response

    
    def form_invalid(self, form):
        return super(UserCreateView, self).form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['subtitle']='Crear nuevo usuario'
        context['title']='Crear Usuario'
        return context