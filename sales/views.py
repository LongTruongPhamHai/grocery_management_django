from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Invoice, InvoiceDetail
from .forms import InvoiceForm, InvoiceDetailForm


# ---------- INVOICE ----------
def invoice_list(request):
    invoices = Invoice.objects.all().order_by("-created_at")
    return render(request, "sales/invoice_list.html", {"invoices": invoices})


def invoice_create(request):
    invoice = Invoice.objects.create()
    messages.success(request, f"Đã tạo hóa đơn #{invoice.pk}")
    return redirect("sales:invoice_update", pk=invoice.pk)


def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    details = invoice.details.select_related("product").all()
    if request.method == "POST":
        form = InvoiceDetailForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.invoice = invoice
            detail.save()
            messages.success(request, "Đã thêm chi tiết hóa đơn!")
            return redirect("sales:invoice_update", pk=invoice.pk)
    else:
        form = InvoiceDetailForm()
    return render(
        request,
        "sales/invoice_form.html",
        {"invoice": invoice, "details": details, "form": form},
    )


def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        messages.success(request, "Đã xóa hóa đơn!")
        return redirect("sales:invoice_list")
    return render(request, "sales/invoice_confirm_delete.html", {"invoice": invoice})
