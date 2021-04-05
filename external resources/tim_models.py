from django.db import models
from django.contrib.auth.models import User # improt the user model
# Create your models here.


# Creating a database object (To do list), inheriting models.Model
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="todolist", null = True)  # specify foreign key, so that every todolist will be linked to a user
    # first field is name, with a CharField of length 200
    name = models.CharField(max_length=200)

    ## just for printing out    
    def __str__(self):
        return self.name


## Creating a database object : Item
class Item(models.Model):
    # specify the foreign key is another object, on_delete: remove all Items once the todolist is removed
    todolist = models.ForeignKey(ToDoList, on_delete = models.CASCADE)
    text = models.CharField(max_length=200)     # need to specify max_length when creation
    complete = models.BooleanField()            # a boolean true / false

    # same, just for printing out
    def __str__(self):
        return self.text

