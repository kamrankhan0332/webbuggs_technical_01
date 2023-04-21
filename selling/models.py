from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    CUSTOMER = 'CU'
    SELLER = 'SE'
    USER_ROLES = [
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
    ]
    role = models.CharField(max_length=2, choices=USER_ROLES, default=CUSTOMER)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Color(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='sub_category_images/', blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_categories_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_categories_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    colors = models.ManyToManyField(Color)

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate SKU when creating a new object
            date_str = timezone.now().strftime('%Y%m%d')
            slugified_title = slugify(self.title)
            self.sku = f'prod-{date_str}-{slugified_title}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
