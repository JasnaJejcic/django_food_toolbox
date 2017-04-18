from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Recipe, Ingredients_List, RecipeForm, Recipe_Ingredient

def index(request):
	latest_recipe = Recipe.objects.order_by('-last_modified_date')[:1]

	if latest_recipe:
		return redirect('food_toolbox:featured', recipe_id=(latest_recipe[0].id))
	else:
		return redirect('food_toolbox:create')

def featured(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	context = {
			'ingredients_list' : Ingredients_List.objects.order_by('name'),
			'featured_recipe' : recipe,
			'featured_recipe_ingredients' : Recipe_Ingredient.objects.filter(recipe_id=recipe_id)
	}
	return render(request, 'food_toolbox/index.html', context)

def create_recipe(request, error_message=None):
	context = {
			'ingredients_list' : Ingredients_List.objects.order_by('name'),
			'recipe_form' : RecipeForm
	}
	if error_message:
		context['error_message'] = error_message

	return render(request, 'food_toolbox/create.html', context)

def add_recipe(request):
	new_recipe_id = None
	try:
		new_recipe = Recipe(
			title_text = request.POST['title_text'],
			last_modified_date = timezone.now(),
			process_description = request.POST['process_description'])

		if (request.POST['cooking_temperature_celsius']):
			new_recipe.cooking_temperature_celsius = request.POST['cooking_temperature_celsius']
		if (request.POST['preparation_time_minutes']):
			new_recipe.preparation_time_minutes = request.POST['preparation_time_minutes']
		new_recipe.presentation_image_link = request.POST['presentation_image_link']

		new_recipe.save()
		new_recipe_id = new_recipe.id

		for key in request.POST.keys():
			if key.startswith('ingredient'):
				recipe_ingredient = Recipe_Ingredient()
				recipe_ingredient.recipe = new_recipe
				recipe_ingredient.ingredient_name = Ingredients_List(pk=request.POST[key])
				recipe_ingredient.ingredient_quantity = request.POST[request.POST[key]]

				recipe_ingredient.save()

	except IntegrityError as e:
		# TODO Improve error message
		return redirect('food_toolbox:create', error_message="Something went wrong, please try again.")
	else:
		return redirect('food_toolbox:featured', recipe_id=(new_recipe_id))

def add_ingredient(request):
	new_ingredient = Ingredients_List()
	new_ingredient.name = request.POST['ingredient']
	try:
		new_ingredient.save()
	except(IntegrityError):
		return redirect('food_toolbox:create', error_message="Ingredient already exists.")
	else:
		return redirect('food_toolbox:create')

def search(request):
	recipe_relevance_counter = dict()

	for key in request.GET:
		if key.startswith('ingredient'):
			#search by ingredient
			recipe_ingredients_list = Recipe_Ingredient.objects.filter(ingredient_name = request.GET[key])
			for recipe_ingredient in recipe_ingredients_list:
				if recipe_ingredient.recipe.id in recipe_relevance_counter:
					recipe_relevance_counter[recipe_ingredient.recipe.id] += 1
				else:
					recipe_relevance_counter[recipe_ingredient.recipe.id] = 1
		else:
			#search by title/description
			if (request.GET['word_search']):
				recipe_list = Recipe.objects.filter(
					Q(title_text__icontains = request.GET['word_search']) | 
					Q(process_description__icontains = request.GET['word_search']))
				for recipe in recipe_list:
					if recipe.id in recipe_relevance_counter:
						recipe_relevance_counter[recipe.id] += 1
					else:
						recipe_relevance_counter[recipe.id] = 1
	
	if (recipe_relevance_counter):			
		# get last or most relevant
		relevance_values = list(recipe_relevance_counter.values())
		relevance_keys = list(recipe_relevance_counter.keys())
		featured_recipe = relevance_keys[relevance_values.index(max(relevance_values))]

		return redirect('food_toolbox:featured', recipe_id=(featured_recipe))
	else:
		return redirect('food_toolbox:index')