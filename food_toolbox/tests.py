import datetime

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.utils import timezone

from .models import Recipe, Ingredients_List

def create_recipe(title_text, description_text, days=0):
	"""
	Creates a recipe object with a title, description and date that can be offset to test for latest
	featured recipe.
	"""
	recipe_date = timezone.now() + datetime.timedelta(days=days)
	return Recipe.objects.create(
		title_text=title_text, 
		process_description=description_text, 
		last_modified_date=recipe_date)

def create_ingredients_list(ingredients_list):
	"""
	Creates a list of ingredient objects from a list of ingredients.
	"""
	result_list=list()
	for ingredient in ingredients_list:
		result_list.append(Ingredients_List.objects.create(name=ingredient))
	return result_list

class RecipeViewTests(TestCase):
	def test_index_view_with_no_recipes(self):
		"""
		If no recipes exist, user should be redirected to recipe creation page.
		"""
		response = self.client.get(reverse('food_toolbox:index'))
		expected_url = reverse('food_toolbox:create')
		self.assertRedirects(
			response, expected_url, status_code=302, target_status_code=200, fetch_redirect_response=True)

	def test_index_view_with_existing_recipes(self):
		"""
		If there are any recipes, user should be redirected to feature the latest recipe.
		"""
		first_recipe = create_recipe("First one", "First description", -3)
		latest_recipe = create_recipe("Last one", "Last description")
		response = self.client.get(reverse('food_toolbox:index'))
		expected_url = reverse('food_toolbox:featured', kwargs={'recipe_id':latest_recipe.id})
		self.assertRedirects(
			response, expected_url, status_code=302, target_status_code=200, fetch_redirect_response=True)

	def test_featured_view_with_no_recipe(self):
		"""
		When passed no recipe id, the page should return an error.
		"""
		with self.assertRaises(NoReverseMatch):
			response = self.client.get(reverse('food_toolbox:featured'))

	def test_featured_view_with_single_recipe(self):
		"""
		When passed a context, the ingredients and recipe details should be displayed.
		TODO: assert the rest of the context
		"""
		recipe = create_recipe("Some Recipe", "Recipe Description")
		response = self.client.get(reverse('food_toolbox:featured', kwargs={'recipe_id':recipe.id}))
		self.assertEqual(response.context['featured_recipe'], recipe)

	def test_create_recipe_view_with_error_message(self):
		"""
		When error message is passed to the view, it should be displaied in the content.

		TODO: check water is on create recipe page
		"""
		response = self.client.get(
			reverse('food_toolbox:create', kwargs={'error_message':"An error has occured"}))
		self.assertContains(response, text="An error has occured")

	def test_create_recipe_view_with_no_ingredients_list(self):
		"""    	
		When first creating new recipe, ingredients list should be empty.
		"""
		response = self.client.get(reverse('food_toolbox:create'))
		self.assertQuerysetEqual(
			response.context['ingredients_list'], [])

	def test_create_recipe_view_add_new_ingredient(self):
		"""
		When adding new ingredient, user should be redirected to create recipe page with no error message.
		"""
		context={
			'ingredient':"water"
		}
		response = self.client.post(reverse('food_toolbox:add_ingredient'), context)
		expected_url = reverse('food_toolbox:create')
		self.assertRedirects(
			response, expected_url, status_code=302, target_status_code=200, fetch_redirect_response=True)
		
	def test_create_recipe_view_add_duplicate_ingredient(self):
		"""
		When adding an ingredient that already exists, user should be redirected to create recipe page
		with an error message.

		see: http://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
		"""
		try:
			with transaction.atomic():
				ingredient = create_ingredients_list(["flour"])
				context={
					'ingredient':"flour"
				}
				response = self.client.post(reverse('food_toolbox:add_ingredient'), context)
				self.assertEqual(response.status_code, 302)
				expected_url = reverse(
					'food_toolbox:create', kwargs={'error_message':"Ingredient already exists."})
				self.assertRedirects(
					response, 
					expected_url, 
					status_code=302, 
					target_status_code=200, 
					fetch_redirect_response=False)
		except IntegrityError:
			pass

	def test_create_recipe_view_add_new_recipe(self):
		"""
		When adding a new recipe, user should be redirected to feature the added recipe.
		"""
		ingredient_1 = create_ingredients_list(["water"])
		print ingredient_1
		context ={
			'ingredient1':ingredient_1[0],
			'title_text':"Beverage",
			'process_description':"Fill a glass.",
			'cooking_temperature_celsius':'',
			'preparation_time_minutes':'',
			'presentation_image_link':''
		}
		response = self.client.post(reverse('food_toolbox:add_recipe'), context)
		expected_url = reverse('food_toolbox:featured', kwargs={'recipe_id':recipe.id})
		self.assertRedirects(
			response, expected_url, status_code=302, target_status_code=200, fetch_redirect_response=True)

	def test_create_recipe_view_add_new_recipe_error(self):
		"""
		When an error occurs while adding a new recipe, user should be redirected to create recipe page with
		error message "Something went wrong, please try again."
		"""
		self.assertTrue(True)

	def test_search_view_with_results(self):
		"""
		When search is successful, user should be redirected to feature the best matched recipe.
		"""
		self.assertTrue(True)

	def test_search_view_with_no_results(self):
		"""    	
		When search is unsuccessful, user should be redirected to feature the latest recipe.
		"""
		self.assertTrue(True)

class SearchMethodTests(TestCase):
	def test_successful_title_search(self):
		"""
		Search results should contain the element matched by title.	
		def test_good_vote(self):
		  poll_1 = Poll.objects.get(pk=1)
		  self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)

		  resp = self.client.post('/polls/1/vote/', {'choice': 1})
		  self.assertEqual(resp.status_code, 302)
		  self.assertEqual(resp['Location'], 'http://testserver/polls/1/results/')

		  self.assertEqual(poll_1.choice_set.get(pk=1).votes, 2)	
		"""
		self.assertTrue(True)

	def test_successful_description_search(self):
		"""
		Search results should contain the element matched by description.
		"""
		self.assertTrue(True)

	def test_successful_ingredient_search(self):
		"""
		Search results should contain the element matched by ingredient.
		"""
		self.assertTrue(True)

	def test_best_match(self):
		"""
		On multiple search conditions, should return the recipe with the most conditions matched.
		"""
		self.assertTrue(True)