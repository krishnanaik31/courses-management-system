from django import forms
from myapp.models import Course, Order, Student, User
from django.forms import CheckboxSelectMultiple


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('student', 'course', 'levels', 'order_date')
    courses = Course.objects.all()
    students = Student.objects.all()
    # student = forms.ChoiceField(choices=[(choice.id, choice) for choice in students], widget=forms.RadioSelect)
    student = forms.RadioSelect()
    # course = forms.ChoiceField(choices=[(choice.id, choice.name) for choice in courses])
    levels = forms.IntegerField(initial=1)
    order_date = forms.DateField(widget=forms.SelectDateWidget)


class InterestForm(forms.Form):
    class Meta:
        model = Course
        fields = ('interested', 'levels', 'comments')

    interested = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('1', 'Yes'), ('0', 'No')])
    levels = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'city',
            'password',
            'username',
            'interested_in'
        ]
        widgets = {
            'interested_in': CheckboxSelectMultiple()
        }
