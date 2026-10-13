# Generated initial migration for the Nkript starter project.
import decimal
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(blank=True, max_length=200)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="projects/covers/")),
                ("category", models.CharField(choices=[("website", "Website"), ("ecommerce", "E-commerce"), ("software", "Software"), ("marketing", "Digital Marketing"), ("redesign", "Website Redesign"), ("other", "Other")], default="website", max_length=30)),
                ("live_url", models.URLField(blank=True)),
                ("technologies", models.CharField(blank=True, max_length=300)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-is_featured", "-created_at"]},
        ),
        migrations.CreateModel(
            name="WebsiteCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "name"], "verbose_name_plural": "Website categories"},
        ),
        migrations.CreateModel(
            name="WebsitePackage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("short_description", models.CharField(blank=True, max_length=250)),
                ("min_price", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ("max_price", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="packages/")),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="packages", to="core.websitecategory")),
            ],
            options={"ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="QuoteRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("company", models.CharField(blank=True, max_length=200)),
                ("tier", models.CharField(choices=[("min", "Starter"), ("max", "Advanced"), ("custom", "Custom")], default="min", max_length=10)),
                ("base_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("additional_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12)),
                ("estimated_total", models.DecimalField(decimal_places=2, max_digits=12)),
                ("requirements", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("new", "New"), ("reviewing", "Reviewing"), ("sent", "Quotation Sent"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="new", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("package", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="quote_requests", to="core.websitepackage")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="PackageFeature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("included_in_min", models.BooleanField(default=False)),
                ("included_in_max", models.BooleanField(default=False)),
                ("additional_price", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ("is_selectable", models.BooleanField(default=False)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("package", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="features", to="core.websitepackage")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="ProjectScreenshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="projects/screenshots/")),
                ("caption", models.CharField(blank=True, max_length=200)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="screenshots", to="core.project")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="QuoteRequestFeature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("feature_name", models.CharField(max_length=200)),
                ("price_at_quote", models.DecimalField(decimal_places=2, max_digits=12)),
                ("quote", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="selected_features", to="core.quoterequest")),
            ],
        ),
    ]
