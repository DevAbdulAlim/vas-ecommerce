from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class LoginRequiredMixin:

    @method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch') 
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)