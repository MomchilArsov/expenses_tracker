import os

from django import forms

from expenses_tracker.web.models import Profile, Expense


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('budget', 'first_name', 'last_name', 'image')
        labels = {
            'first_name': 'First Name',
            'last_name': ' Last Name',
            'image': 'Profile Image', # как да се показват! може да се направи в моделите с ( verbose_name='Alabala')
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('budget', 'first_name', 'last_name', 'image')


class DeleteProfileForm(forms.ModelForm):

    def save(self, commit=True): # оувъррайдваме save метода, като му казваме да трие(запомни изтриването)
        image_path = self.instance.image.path #  image path
        self.instance.delete()       # delete profile
        Expense.objects.all().delete() # трие вс експенси
        os.remove(image_path)  # delete image! it is after delete profile. ако по някаква прична не можем да изтрием профила, де не изтрием снимката
        return self.instance

    class Meta:
        model = Profile
        fields = ()


class CreateExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('title', 'description', 'image', 'price')


class EditExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('title', 'description', 'image', 'price')


class DeleteExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):     # така се прави да са дисейбълд полетата !
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Expense
        fields = ('title', 'description', 'image', 'price')