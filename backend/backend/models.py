from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator, RegexValidator

class User(models.Model):
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()]
    )
    password_hash = models.CharField(max_length=128)
    

    pan_id = models.CharField(max_length=11, null=True, blank=True)
    tax_id = models.CharField(max_length=20, null=True, blank=True)
    
    
    filing_status = models.CharField(max_length=20, null=True, blank=True)
    contact_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=10, default='en')

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id'])
        ]

    
    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    
    @property
    def masked_pan_id(self):
        if self.pan_id:
            return f"XXX-XX-{self.pan_id[-4:]}"
        return None

    @property
    def masked_tax_id(self):
        if self.tax_id:
            return f"XX-XXX{self.tax_id[-4:]}"
        return None

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, name):
        parts = name.split()
        self.first_name = parts[0]
        self.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

    