from django.db import models
from sections.models import Section, Student_class
from django.contrib.auth.models import AbstractUser, BaseUserManager



# Create user manager
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    # Add your custom fields here
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to="Admin_pictures", height_field=None, width_field=None, max_length=None, blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name="Section", on_delete=models.CASCADE, blank=True, null=True)
    m_class = models.ForeignKey(Student_class, verbose_name="Class master of", on_delete=models.CASCADE, blank=True, null=True)
    # Users status 
    is_admin = models.BooleanField(default=False, verbose_name="Admin", blank=True)
    is_principal = models.BooleanField(default=False, verbose_name="Principal", blank=True)
    is_admission = models.BooleanField(default=False, verbose_name="Admission office", blank=True)
    is_class_master = models.BooleanField(default=False, verbose_name="Class Master", blank=True)
    is_exam = models.BooleanField(default=False, verbose_name="Examination office", blank=True)
    is_account = models.BooleanField(default=False, verbose_name="Account Department", blank=True)
    is_student = models.BooleanField(default=False, verbose_name="Student", blank=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()
