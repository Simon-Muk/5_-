<!-- Создать проект (shop_api) с одним приложением (product). Будут три модели:

1.Category

    name

2.Product

    title
    description
    price
    category(ForeignKey)

3.Review

    text
    product(ForeignKey)

 

    Вывести список категориев /api/v1/categories/
    Вывести одну категорию      /api/v1/categories/<int:id>/

 

    Вывести список товаров      /api/v1/products/
    Вывести один товар             /api/v1/products/<int:id>/

 

    Вывести список отзывов       /api/v1/reviews/

Вывести один отзыв              /api/v1/reviews/<int:id>/ -->
Запуск проекта:

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver