from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class WebsiteCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "Website categories"

    def __str__(self):
        return self.name


class WebsitePackage(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(WebsiteCategory, on_delete=models.PROTECT, related_name="packages")
    short_description = models.CharField(max_length=250, blank=True)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    max_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    cover_image = models.ImageField(upload_to="packages/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def clean(self):
        super().clean()
        if self.max_price is not None and self.min_price is not None and self.max_price < self.min_price:
            raise ValidationError({"max_price": "Maximum price must be at least the minimum price."})

    def __str__(self):
        return self.name


class PackageFeature(models.Model):
    package = models.ForeignKey(WebsitePackage, on_delete=models.CASCADE, related_name="features")
    name = models.CharField(max_length=200)
    included_in_min = models.BooleanField(default=False)
    included_in_max = models.BooleanField(default=False)
    additional_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(0)])
    is_selectable = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.package.name} - {self.name}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("website", "Website"),
        ("ecommerce", "E-commerce"),
        ("software", "Software"),
        ("marketing", "Digital Marketing"),
        ("redesign", "Website Redesign"),
        ("other", "Other"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/covers/")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="website")
    live_url = models.URLField(blank=True)
    technologies = models.CharField(max_length=300, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to="projects/screenshots/")
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.project.title} screenshot"


class QuoteRequest(models.Model):
    TIER_CHOICES = [("min", "Starter"), ("max", "Advanced"), ("custom", "Custom")]
    STATUS_CHOICES = [
        ("new", "New"), ("reviewing", "Reviewing"), ("sent", "Quotation Sent"),
        ("accepted", "Accepted"), ("rejected", "Rejected"),
    ]
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    package = models.ForeignKey(WebsitePackage, on_delete=models.PROTECT, related_name="quote_requests")
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="min")
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    additional_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2)
    requirements = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Quote #{self.pk} - {self.name}"


class QuoteRequestFeature(models.Model):
    quote = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name="selected_features")
    feature_name = models.CharField(max_length=200)
    price_at_quote = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.feature_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'Contact message'}"
