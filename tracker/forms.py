from django import forms
from tracker.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "Any"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done")
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "form-control"})
