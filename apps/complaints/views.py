from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import ComplaintForm, AnswerForm
from .models import Complaint
from django.views.generic import TemplateView

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
        return Complaint.objects.all()

class ComplaintAnswerView(TemplateView):
    def get(self, request, pk):
        if request.user.is_superuser:
            form = AnswerForm()
            complaint = Complaint.objects.get(customer=customer, pk=pk)
            return render(
                request, "complaints/answer_complaint.html", {"complaint": complaint, "form": form}
            )
        else:
            return render(request, "forbidden.html")

    def post(self, request, pk):
        if request.user.is_superuser:
            complaint = Complaint.objects.get(customer=customer, pk=pk)
            form = AnswerForm(request.POST)
            if form.is_valid():
                if form.cleaned_data.get("answer"):
                    complaint.answer = form.cleaned_data.get("answer")
                complaint.save()
                return redirect("/complaints/list")
            else:
                return render(
                    request, "complaints/answer_complaint.html", {"complaint": complaint, "form": form}
                )
        else:
            return render(request, "forbidden.html")

    