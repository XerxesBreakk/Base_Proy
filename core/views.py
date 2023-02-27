from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages

class IndexView(TemplateView):
    template_name="pages/index.html"

class LoginPageView(LoginView):
    template_name="pages/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))