import datetime

from django.db import models
from django.forms import ModelForm
from django.utils import timezone


class Recipe(models.Model):
    title_text = models.CharField(max_length=200)
    last_modified_date = models.DateField('last modified')
    process_description = models.TextField()
    cooking_temperature_celsius = models.IntegerField(blank=True, null = True)
    preparation_time_minutes = models.IntegerField(blank=True, null = True)
    presentation_image_link = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.title_text

class Ingredients_List(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Recipe_Ingredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	ingredient_name = models.ForeignKey(Ingredients_List, on_delete=models.CASCADE)
	ingredient_quantity = models.CharField(max_length=100, blank=True, null=True)
    # def __str__(self):              # __unicode__ on Python 2
    #     return "%s (%s)" % (
    #         self.name,
    #         ", ".join(topping.name for topping in self.toppings.all()),
    #     )

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title_text', 'process_description', 'cooking_temperature_celsius', 'preparation_time_minutes', 'presentation_image_link']
        # labels = {
        #     'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }

