from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import ComplaintForm
from .models import Complaint

# Create your views here.


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = "add_complaint.html"
    success_url = reverse_lazy("complaints")
    login_url = "/signin/"

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = "complaint_list.html"
    context_object_name = "complaints"
    login_url = "/signin/"

    def get_queryset(self):
        return Complaint.objects.filter(customer=self.request.user.customer)
