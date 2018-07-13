# social-network
Solution of test task for StarNavi.


# Used packages for API
  * [djangorestframework](https://github.com/encode/django-rest-framework) - django-rest-framework
  * [django-extra-fields](https://github.com/Hipo/drf-extra-fields) - Для использования поля типа Base64ImageField
  * [django-cors-middleware](https://github.com/zestedesavoir/django-cors-middleware) - Для разрешения междоменных запросов
  * [django-oauth-toolkit](https://github.com/jazzband/django-oauth-toolkit) - Рекомендуемый пакет поддержки OAuth 2.0


# Used documentation
  * [Django REST framework (Home)](http://www.django-rest-framework.org/)
  * [django-rest-framework-russian-documentation (Russian)](https://legacy.gitbook.com/book/ilyachch/django-rest-framework-russian-documentation/)


# Browser - Register an application
  * **Register an application:** http://localhost:8000/o/applications/
  * **Edit applications:** http://localhost:8000/o/applications/

**В целях безопасности, добавлены следующие ограничения:**

  * **Client type:** Only - "confidential"
  * **Authorization Grant Type:** Only - "authorization-code"


# Test OAuth2 provider
  * **Consumer for test:** http://django-oauth-toolkit.herokuapp.com/consumer/


# Unit tests
  * [posts/tests.py](https://github.com/genkosta/social-network/blob/master/posts/tests.py)


# Console
**$ sudo apt install httpie**

  * **Get posts:** http GET 'http://localhost:8000/api/v1/integrations/posts/' 'Authorization:Bearer access_token'
  * **Get post:** http GET 'http://localhost:8000/api/v1/integrations/posts/{id}/' 'Authorization:Bearer access_token'
  * **Like:** http POST 'http://localhost:8000/api/v1/integrations/posts/{id}/like/' 'Authorization:Bearer access_token'
  * **Unlike:** http POST 'http://localhost:8000/api/v1/integrations/posts/{id}/unlike/' 'Authorization:Bearer access_token'
  * **Create post:** http -f POST 'http://localhost:8000/api/v1/integrations/posts/' 'Authorization:Bearer access_token' title='My Post' message='Hello World!' image='image_base64'
  * **Update post:** http -f PUT 'http://localhost:8000/api/v1/integrations/posts/{id}/' 'Authorization:Bearer access_token' title='My Post ' message='Hello World!'
  * **Partial update post:** http -f PATCH 'http://localhost:8000/api/v1/integrations/posts/{id}/' 'Authorization:Bearer access_token' title='My Post ' message='Hello World!'
  * **Delete post:** http DELETE 'http://localhost:8000/api/v1/integrations/posts/{id}/' 'Authorization:Bearer access_token'
  * **Get user posts:** http GET 'http://localhost:8000/api/v1/integrations/posts/owner/' 'Authorization:Bearer access_token'
  * **Get user post:** http GET 'http://localhost:8000/api/v1/integrations/posts/{id}/owner/' 'Authorization:Bearer access_token'
  * **Add comment:** http -f POST 'http://localhost:8000/api/v1/integrations/posts/{id}/comment/' 'Authorization:Bearer access_token' text='Cool post!!!'
  * **Sort by latest (default):** http GET 'http://localhost:8000/api/v1/integrations/posts/?sort=latest' 'Authorization:Bearer access_token'
  * **Sort by rating:** http GET 'http://localhost:8000/api/v1/integrations/posts/?sort=rating' 'Authorization:Bearer access_token'

**Опциональные параметры:**

  * page - номер страницы
  * page_size - количество записей на страницу

**Пример результата запроса:**

http GET 'http://localhost:8000/api/v1/integrations/posts/10280/' 'Authorization:Bearer UfPvyV7WC6mIcf1W4LVqlBmUsXvwow'
![Пример результата запроса](https://github.com/genkosta/social-network/blob/master/screenshots/example_post_list.png?raw=true)


# MIT License
[MIT License](https://github.com/genkosta/social-network/blob/master/LICENSE)
