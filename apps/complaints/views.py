from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .forms import ComplaintForm, AnswerForm
from .models import Complaint
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
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

class ComplaintAllView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = "complaints_all.html"
    context_object_name = "complaints"
    login_url = "/signin/"

    def get_queryset(self):
        return Complaint.objects.all().order_by("status")


class ComplaintAnswerView(UserPassesTestMixin, UpdateView):
    model = Complaint
    form_class = AnswerForm
    template_name = "answer_complaint.html"
    success_url = "/complaints/list"
    login_url = "/signin/"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.status = "Cerrado"
        return super().form_valid(form)

    
    