from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# forms.ModelForm대신 UserCreationForm사용가능


class SignUpForm(forms.ModelForm):
    # 모든 ModelForm은  save method를 가지고 있다.에러가 있으면 저장을 하고, 다시 돌아가는 느낌적인 느낌?..
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    # first_name = forms.CharField(max_length=80)
    # last_name = forms.CharField(max_length=80)
    # email = forms.EmailField()
    # password-Check: password1
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이메일 중복, 다른 이메일로 해주세요", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        # commit=False? object(user)를 생성하지만 DB에는 commit이 되지 않는것
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

    # def clean_email(self):
    #     # vaildation email
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email=email)
    #         raise forms.ValidationError("User already exists with the email")
    #     except models.User.DoesNotExist:
    #         return email

    # def save(self):
    # 계정을 생성후 바로 로그인
    # first_name = self.cleaned_data.get("first_name")
    # last_name = self.cleaned_data.get("last_name")
    # email = self.cleaned_data.get("email")
    # password = self.cleaned_data.get("password")

    # # models.User.objects.create()로는 암호화가 불가능...따라서
    # user = models.User.objects.create_user(email, password=password,)
    # user.first_name = first_name
    # user.last_name = last_name
    # user.save()

