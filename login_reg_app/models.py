from django.db import models
import datetime as dt
import bcrypt

class User_Manager(models.Manager):
    def age_of_user(self, post_data):
        birthday = dt.date(post_data["birthday"]).year
        date_today = dt.date.today().year
        age = date_today - birthday
        print(f"Age of User: {age}, Year of Today's Date")
        
        return int(age)

    def sign_in_validator(self, post_data):
        errors = {}
        if len(post_data["email"]) < 2:
            errors["email"] = "Please provide a longer email"
        try:
            user = User.objects.filter(email = post_data["email"])
            if not user:
                errors["email"] = "Invalid email. Please try again"
        except:
            errors["email"] = "Invalid email. Please try again"

        if len(post_data["password"]) < 5:
            errors["password"] = "Invalid password. Please try again"

        return errors
    
    def reg_validator(self, post_data):
        errors = {}

        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        
        if len(post_data["birthday"]) < 1:
            errors["birthday"] = "Please select or enter a birthday"
        if post_data["birthday"].isalpha() == True:
            errors["birthday"] = "Birthday must be a valid date"
        if len(post_data["birthday"]) > 0:
            date_entered = dt.datetime.strptime(post_data["birthday"], "%m/%d/%Y")
            if date_entered > dt.datetime.now():
                errors["birthday"] = 'Birthday should be in the past'
        # if User_Manager.age_of_user(self, post_data["birthday"]) < 13:
        #     errors["birthday"] = "Must be 13 years or older to Register"

        if len(post_data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if post_data["confirm_pass"] != post_data["password"]:
            errors["confirm_pass"] = "Passwords do not match, please try again"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    birthday = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = User_Manager()