from menu.models import Cart, Dish
from rest_framework import status
import pytest
from model_bakery import baker

# GET Menu
@pytest.mark.django_db
class TestRetrieveMenu:
    def test_if_user_is_anonymous_returns_200(self, api_client):
        response = api_client.get('/menu/')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_if_menu_has_no_dishes_returns_404(self, api_client, authenticate):
        #create empty menu
        cart = baker.make(Cart)
        
        response = api_client.get(f'/menu/{cart.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

# POST Menu
@pytest.fixture
def create_menu(api_client):
    def do_create_menu(menu):
        return api_client.post('/menu/', menu)
    return do_create_menu

@pytest.mark.django_db
class TestCreateMenu:
    def test_if_user_is_anonymous_returns_401(self, create_menu):
        response = create_menu({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_menu):
        authenticate()

        response = create_menu({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_menu):
        authenticate(is_staff=True)

        response = create_menu({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_menu):
        authenticate(is_staff=True)

        response = create_menu({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

# PUT Menu
@pytest.mark.django_db
class TestUpdateMenu:
    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate()
        cart = baker.make(Cart)
        dish = baker.make(Dish)

        response = api_client.post(f'/dishes/', {'title': 'a', "cart": cart.id, "description": "random description", "price": 6.99, "preparation_time": "00:10:00", "is_vegetarian": False})

        response = api_client.put(f'/menu/{cart.id}/', {'title':'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        cart = baker.make(Cart)
        dish = baker.make(Dish)

        response = api_client.post(f'/dishes/', {'title': 'a', "cart": cart.id, "description": "random description", "price": 6.99, "preparation_time": "00:10:00", "is_vegetarian": False})

        response = api_client.put(f'/menu/{cart.id}/', {'title':'a'})

        assert response.status_code == status.HTTP_200_OK


# GET Cart
@pytest.mark.django_db
class TestRetrieveCart:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/carts/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_staff_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True)

        response = api_client.get('/carts/')

        assert response.status_code == status.HTTP_200_OK

# POST Cart
@pytest.fixture
def create_cart(api_client):
    def do_create_cart(cart):
        return api_client.post('/carts/', cart)
    return do_create_cart


@pytest.mark.django_db
class TestCreateCart:
    def test_if_user_is_anonymous_returns_401(self, create_cart):
        response = create_cart({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_cart):
        authenticate()

        response = create_cart({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_cart):
        authenticate(is_staff=True)

        response = create_cart({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_cart):
        authenticate(is_staff=True)

        response = create_cart({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

# DEL Cart
@pytest.mark.django_db
class TestDeleteCart:
    def test_if_admin_can_delete_not_empty_menu_returns_405(self, authenticate, api_client):
        authenticate(is_staff=True)
        cart = baker.make(Cart)
        dish = baker.make(Dish)

        response = api_client.post(f'/dishes/', {'title': 'am', "cart": cart.id, "description": "random descriptionn", "price": 6.88, "preparation_time": "00:10:00", "is_vegetarian": False})

        assert response.status_code == status.HTTP_201_CREATED

        response = api_client.delete(f'/carts/{cart.id}/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# GET Dish
@pytest.mark.django_db
class TestRetrieveDish:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/dishes/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_staff_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True)

        response = api_client.get('/dishes/')

        assert response.status_code == status.HTTP_200_OK


# POST Dish
@pytest.fixture
def create_dish(api_client):
    def do_create_dish(dish):
        return api_client.post('/dishes/', dish)
    return do_create_dish


@pytest.mark.django_db
class TestCreateDish:
    def test_if_user_is_anonymous_returns_401(self, create_dish):
        response = create_dish({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_dish):
        authenticate()

        response = create_dish({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_dish):
        authenticate(is_staff=True)

        response = create_dish({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_dish):
        authenticate(is_staff=True)
        cart = baker.make(Cart)

        response = create_dish({'title': 'a', "cart": cart.id, "description": "random description", "price": 6.99, "preparation_time": "00:10:00", "is_vegetarian": False})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

# PUT Dish
@pytest.mark.django_db
class TestUpdateDish:
    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate()
        dish = baker.make(Dish)
        cart = baker.make(Cart)

        response = api_client.put(f'/dishes/{dish.id}/', {'title': 'a', "cart": cart.id, "description": "random description", "price": 6.99, "preparation_time": "00:10:00", "is_vegetarian": False})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        dish = baker.make(Dish)
        cart = baker.make(Cart)

        response = api_client.put(f'/dishes/{dish.id}/', {'title': 'a', "cart": cart.id, "description": "random description", "price": 6.99, "preparation_time": "00:10:00", "is_vegetarian": False})

        assert response.status_code == status.HTTP_200_OK
