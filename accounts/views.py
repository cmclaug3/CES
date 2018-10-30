from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import PreSetAuthorizedUserForm, SetNewUserPasswordForm
from accounts.models import PreSetAuthorizedUser, User, Employee
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError




class RegisterAuthorizedUserView(View):

    def get(self, request):
        context = {
            'form': PreSetAuthorizedUserForm()
        }
        return render(request, 'register_authorized_user_form.html', context)

    def post(self, request):
        form = PreSetAuthorizedUserForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'register_authorized_user_form.html', context)

        first_name = form.cleaned_data['first_name'].capitalize()
        last_name = form.cleaned_data['last_name'].capitalize()
        email = form.cleaned_data['email']
        code = form.cleaned_data['code']

        try:
            correct_user = PreSetAuthorizedUser.objects.get(first_name=first_name,
                                                            last_name=last_name,
                                                            email=email,
                                                            code=code)

        # Registration may proceed (credentials are correct)
            type_of_user = correct_user.type

            if type_of_user == 'employee':
                new_user = User.objects.create_user(email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)

            elif type_of_user == 'admin':
                new_user = User.objects.create_staff_user(email=email,
                                                          first_name=first_name,
                                                          last_name=last_name)

            messages.add_message(request, messages.SUCCESS, 'Awesome you are authorized to signup')
            return redirect(reverse('set_new_user_password', kwargs={'new_user_id': new_user.id}))

        except PreSetAuthorizedUser.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Incorrect Credentials, cannot register')
            return redirect(reverse('home'))

        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'You have already registered, please log in normally')
            return redirect(reverse('home'))




class SetNewUserPasswordView(View):

    def get(self, request, new_user_id):
        context = {
            'form': SetNewUserPasswordForm()
        }
        return render(request, 'set_new_user_password_form.html', context)

    def post(self, request, new_user_id):
        form = SetNewUserPasswordForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'set_new_user_password_form.html', context)

        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        new_user = User.objects.get(id=new_user_id)

        if password1 == password2:
            new_user.set_password(password1)
            new_user.save()

        else:
            messages.add_message(request, messages.ERROR, 'passwords do not match try again')
            return redirect(reverse('set_new_user_password', kwargs={'new_user_id': new_user.id}))


        if new_user.is_admin == False:

            new_employee = Employee.objects.create(user=new_user)
            new_employee.save()

        messages.add_message(request, messages.SUCCESS, 'password setup you can now log in normally from now on')
        return redirect(reverse('home'))








