from django import forms
from .models import *
from django.forms.widgets import NumberInput
from datetime import datetime
from django.forms import inlineformset_factory


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
                "class": "form-control"
            }
        ))

    details = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Details",
                "class": "form-control",
                'rows': '3'
            }
        ))

    total_target = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Total Target",
                "class": "form-control",
                "onkeypress": "return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))"
            }
        ))

    start_time = forms.DateTimeField(
        widget=NumberInput(
            attrs={
                'placeholder': 'Start date & time',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    end_time = forms.DateTimeField(
        widget=NumberInput(
            attrs={
                'placeholder': 'End date & time',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))



    # category = forms.ChoiceField(
    #     choices=[(catogrey.id, catogrey.name) for catogrey in Catogrey.objects.all()],
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )




    # tags = forms.MultipleChoiceField(
    #     choices=[(tag.id, tag.name) for tag in Tag.objects.all()],
    #     widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    #     required=False
    # )
    # category = forms.ModelChoiceField(queryset=Catogrey.objects.all(),
    #                                   widget=forms.Select(
    #                                       attrs={
    #                                           "class": "form-control"
    #                                       }
    #                                   ))

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.SelectMultiple(
                                              attrs={
                                                  "class": "form-control"
                                              }
                                          ), required=False)
    category = forms.ModelChoiceField(queryset=Catogrey.objects.all(),
                                      widget=forms.Select(
                                          attrs={
                                              "class": "form-control"
                                          }
                                      ), required=False)

    # category = forms.ChoiceField(
    #     choices=[(catogrey.id, catogrey.name) for catogrey in Catogrey.objects.all()],
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )


    class Meta:
        model = Image  # Replace with your actual Image model
        fields = ['images_before', 'images_after']

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'style': 'display: none'}),
        label="Images",  # Changed label to plural
        required=False  # If you want to make it optional
    )


    class Meta:
        model = Project
        fields = ('title',
                  'details',
                  'total_target',
                  'start_time',
                  'end_time',
                  'category',
                  'tags')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_time")
        end_date = cleaned_data.get("end_time")
        today_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        if today_date.date() > end_date.date():
            msg = "End date should be greater than Current date [ Should be after today !]."
            self._errors["end_time"] = self.error_class([msg])
        else:
            if end_date <= start_date:
                msg = "End date should be greater than start date."
                self._errors["end_time"] = self.error_class([msg])


class PicturesForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['images_before', 'images_after']


class Report_form(forms.ModelForm):
    class Meta:
        model = Project_Report
        fields = ['report']


class Comment_report_form(forms.ModelForm):
    class Meta:
        model = Comment_Report
        fields = ['report']


class Reply_form(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']


# class Category_form(forms.ModelForm):
#     class Meta:
#         model = Catogrey
#         fields = ['name']
#
# Catogries =forms.ChoiceField(choices= [ (catogrey.id, catogrey.name) for catogrey in Catogrey.objects.all() ] )
#
# class Meta:
#     model = Project
#     fields = ['title', 'details', 'total_target', 'start_time', 'end_time','tags']
#     widgets = {

#         'start_time': forms.TextInput(attrs={'type': 'datetime-local'}),
#         'end_time': forms.TextInput(attrs={'type': 'datetime-local'}),
#     }
# def __init__(self, *args, **kwargs):
#         super(ProjectForm, self).__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs.update({'class': 'form-control'})
#         self.fields['details'].widget.attrs.update({'class': 'form-control'})
#         self.fields['total_target'].widget.attrs.update({'class': 'form-control'})
#         self.fields['start_time'].widget.attrs.update({'class': 'form-control'})
#         self.fields['end_time'].widget.attrs.update({'class': 'form-control'})
#         # self.fields['category'].widget.attrs.update({'class': 'form-control'})
#         self.fields['tags'].widget.attrs.update({'class': 'form-control'})