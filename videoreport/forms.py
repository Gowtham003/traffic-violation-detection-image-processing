from django import forms

class ReportForm(forms.Form):
    officer_name = forms.CharField(label='Officer name ',widget=forms.TextInput(attrs={'placeholder': 'in-charge of reporting official'}), max_length=100)
    red_duration = forms.IntegerField(label='Red Signal Duration ', widget=forms.TextInput(attrs={'placeholder': 'Red Signal Duration in seconds)'}), max_value=200)
    yellow_duration = forms.IntegerField(label='Yellow Signal Duration ', widget=forms.TextInput(attrs={'placeholder': 'Yellow Signal Duration in seconds)'}), max_value=50)
    green_duration = forms.IntegerField(label='Green Signal Duration ', widget=forms.TextInput(attrs={'placeholder': 'Green Signal Duration in seconds)'}), max_value=200)
    start_time = forms.IntegerField(label='Start Time ', widget=forms.TextInput(attrs={'placeholder': 'red signal starting on video'}),min_value=0, max_value=59)
    video_taken_time = forms.DateTimeField(label='Video captured at ', widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy hh:mm:ss'}))
    video = forms.FileField()
    position = forms.CharField(max_length=10, widget=forms.Select(choices=(('near', 'Near'),('medium','Medium'), ('far', 'Far') )))