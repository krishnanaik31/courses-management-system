from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


class Topic(models.Model):
    CATEGORY_CHOICES = [('Development', "Development"), ('Business', "Business"), ('IT', 'IT & Software'),
                        ('Health & Fitness', 'Health & Fitness'), ('Finance & Accounting', 'Finance & Accounting')]
    name = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default='Development')

    def __str__(self):
        return self.name


def limit(val):
    if not 100 <= val <= 200:
        raise ValidationError(('Please enter value between 100 and 200 , %(value)  is not in the range '),
                              params={'value': val}, )


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[limit])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    hours = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    interested_to = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name

    def discount(self):
        return float(self.price) * 0.9


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
                    ('CG', 'Calgary'),
                    ('MR', 'Montreal'),
                    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to='profile_photo', null=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 250px; height:250px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.get_full_name()


class Order(models.Model):
    ORDER_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, related_name='orders', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField()

    def __str__(self):
        return str(self.course)

    def total_cost(self):
        cname = Course.objects.get(name=self.course)
        total_price = self.total_price + cname.price
        return self.total_price
