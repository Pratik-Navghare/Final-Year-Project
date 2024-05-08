from django import forms

class image_form(forms.Form):
	name = forms.CharField()
	img = forms.ImageField()
