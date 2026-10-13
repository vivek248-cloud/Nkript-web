from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .forms import QuoteRequestForm, ContactMessageForm
from .models import Project, WebsiteCategory, WebsitePackage, PackageFeature, QuoteRequest, QuoteRequestFeature


def home(request):
    projects = Project.objects.filter(is_published=True, is_featured=True)[:6]
    categories = WebsiteCategory.objects.filter(is_active=True)
    packages = WebsitePackage.objects.filter(is_active=True).select_related("category")[:3]
    return render(request, "core/home.html", {"projects": projects, "categories": categories, "packages": packages})


def portfolio(request):
    projects = Project.objects.filter(is_published=True)
    category = request.GET.get("category", "")
    if category:
        projects = projects.filter(category=category)
    return render(request, "core/portfolio.html", {
        "projects": projects,
        "category_choices": Project.CATEGORY_CHOICES,
        "selected_category": category,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id, is_published=True)
    return render(request, "core/project_detail.html", {"project": project})


def packages(request):
    categories = WebsiteCategory.objects.filter(is_active=True).prefetch_related("packages__features")
    return render(request, "core/packages.html", {"categories": categories})


def _send_quote_emails(quote):
    feature_lines = "\n".join(
        f"- {f.feature_name}: ₹{f.price_at_quote}" for f in quote.selected_features.all()
    ) or "No optional add-ons selected."
    body = (
        f"Quotation request #{quote.pk}\n\n"
        f"Name: {quote.name}\nEmail: {quote.email}\nPhone: {quote.phone}\n"
        f"Company: {quote.company or '-'}\nPackage: {quote.package.name}\n"
        f"Tier: {quote.get_tier_display()}\nBase price: ₹{quote.base_price}\n"
        f"Add-ons: ₹{quote.additional_total}\nEstimated total: ₹{quote.estimated_total}\n\n"
        f"Selected features:\n{feature_lines}\n\nRequirements:\n{quote.requirements or '-'}\n"
    )
    send_mail(
        subject=f"Nkript quotation request #{quote.pk} received",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[quote.email],
        fail_silently=True,
    )
    send_mail(
        subject=f"New Nkript quotation request #{quote.pk}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=True,
    )


@require_http_methods(["GET", "POST"])
def quote_request(request, package_id):
    package = get_object_or_404(WebsitePackage, pk=package_id, is_active=True)
    features = package.features.all()
    selectable_features = features.filter(is_selectable=True)

    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        selected_ids = request.POST.getlist("features")
        valid_ids = set(selectable_features.values_list("id", flat=True))
        selected_ids = [int(i) for i in selected_ids if i.isdigit() and int(i) in valid_ids]

        if form.is_valid():
            tier = form.cleaned_data["tier"]
            base_price = package.max_price if tier == "max" else package.min_price
            selected_features = list(selectable_features.filter(id__in=selected_ids))
            additional_total = sum((f.additional_price for f in selected_features), Decimal("0.00"))
            estimated_total = base_price + additional_total

            with transaction.atomic():
                quote = form.save(commit=False)
                quote.package = package
                quote.base_price = base_price
                quote.additional_total = additional_total
                quote.estimated_total = estimated_total
                quote.save()
                for feature in selected_features:
                    QuoteRequestFeature.objects.create(
                        quote=quote,
                        feature_name=feature.name,
                        price_at_quote=feature.additional_price,
                    )
            _send_quote_emails(quote)
            request.session["last_quote_id"] = quote.pk
            return redirect("quote_success")
    else:
        form = QuoteRequestForm()

    return render(request, "core/quote_request.html", {
        "package": package, "features": features,
        "selectable_features": selectable_features, "form": form,
    })


def quote_success(request):
    quote_id = request.session.get("last_quote_id")
    quote = QuoteRequest.objects.filter(pk=quote_id).first() if quote_id else None
    return render(request, "core/quote_success.html", {"quote": quote})


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            body = f"Name: {message.name}\nEmail: {message.email}\nSubject: {message.subject}\n\n{message.message}"
            send_mail("New message from Nkript website", body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
            messages.success(request, "Thanks! Your message has been received.")
            return redirect("contact")
    else:
        form = ContactMessageForm()
    return render(request, "core/contact.html", {"form": form})
