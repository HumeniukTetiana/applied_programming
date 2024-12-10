from datetime import datetime
import re
from enum import Enum

class PaymentType(Enum):
    CREDIT_CARD = "Card"
    CASH = "Cash"
    PAYPAL = "PayPal"

class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

class DeliveryStatus(Enum):
    PENDING = "Awaiting shipment"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    RETURNED = "Returned"

#клас для присвоєння ід
class Base:
    _id_counter = 0

    def __init__(self):
        Base._id_counter += 1
        self._id = Base._id_counter

    @property
    def id(self):
        return self._id

class Person(Base):
    def __new__(cls, first_name: str, last_name: str, phone: str | None, email: str, *args, **kwargs):
        if email and not cls.is_valid_email(email):
            raise ValueError("Invalid email format")
        if phone and not cls.is_valid_phone(phone):
            raise ValueError("Invalid phone format")
        return super().__new__(cls)

    def __init__(self, first_name: str, last_name: str, phone: str | None, email: str):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self._phone = phone
        self.email = email

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return bool(re.match(r"^\+?\d{10,15}$", phone))

    #Метод що буде перевизначатись
    def show_info(self):
        pass

class AbstractCustomer():
    def change_password(self, old_password: str, new_password: str):
        if self._password != old_password:
            raise ValueError("Збфгається зі старим паролем")
        if len(new_password) < 8:
            raise ValueError("Новий пароль повинен містити не менше 8 символів")
        self._password = new_password
        return "Пароль успішно змінено."



class Customer(Person, AbstractCustomer):
    def __new__(cls, first_name: str, last_name: str, email: str, phone: str | None, date_of_birth: str | None = None, *args, **kwargs):
        if date_of_birth and not cls.is_valid_date_of_birth(date_of_birth):
            raise ValueError("Invalid date of birth format")
        return super().__new__(cls, first_name, last_name, phone, email, *args, **kwargs)

    def __init__(self, first_name: str, last_name: str, email: str, phone: str | None, date_of_birth: str | None = None, password: str = 'password'):
        super().__init__(first_name, last_name, phone, email)
        self._date_of_birth = date_of_birth
        self._password = password
        self.orders = []

    @staticmethod
    def is_valid_date_of_birth(date_of_birth: str) -> bool:
        return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_of_birth))

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" 

    def add_order(self, order):
        self.orders.append(order)

    def show_info(self):
        """Показує замовлення для цього клієнта"""
        if not self.orders:
            return f"{self.first_name} {self.last_name} has no orders."
        orders_info = "\n".join([f"Order ID: {order.id}, Date: {order.order_date}, Total: {order.total_amount}" for order in self.orders])
        return f"Orders for {self.first_name} {self.last_name}:\n{orders_info}"

class Supplier(Person):
    def __init__(self, supplier_name: str, first_name: str, last_name: str, phone: str, email: str):
        super().__init__(first_name, last_name, phone, email)
        self.supplier_name = supplier_name
        self.ingredients = [] 

    def add_ingredient(self, ingredient):
        """Додає інгредієнт до списку цього постачальника"""
        self.ingredients.append(ingredient)

    def show_info(self):
        """Показує інгредієнти для цього постачальника"""
        if not self.ingredients:
            return f"{self.supplier_name} has no ingredients."
        
        ingredients_info = "\n".join([f"Ingredient Name: {ingredient.ingredient_name}, Price per kg: {ingredient.price_per_kg}" for ingredient in self.ingredients])
        return f"Ingredients supplied by {self.supplier_name}:\n{ingredients_info}"


class Category(Base):
    def __init__(self, category_name: str):
        super().__init__()
        self.category_name = category_name

class Product(Base):
    def __init__(self, category: Category, product_name: str, price: float, description: str):
        super().__init__()
        self._category_id = category.id
        self.product_name = product_name
        self._price = price
        self.description = description

class Full_Order(Base):
    def __init__(self, customer: Customer, payment_type: PaymentType, payment_status: PaymentStatus, total_amount: float, points_used: int = 0):
        super().__init__()
        self._customer_id = customer.id
        self.order_date = datetime.now()
        self.payment_type = payment_type
        self.payment_status = payment_status
        self.total_amount = total_amount
        self._points_used = points_used
        customer.add_order(self)

class Delivery:
    def __init__(self, customer: Customer, delivery_date: str, delivery_address: str, delivery_status: DeliveryStatus, full_order: Full_Order, points_used: int = 0):
        self.full_order = full_order
        self.delivery_date = delivery_date
        self.delivery_address = delivery_address
        self.delivery_status = delivery_status

class Ingredient(Base):
    def __init__(self, ingredient_name: str, supplier: Supplier, price_per_kg: float):
        super().__init__()
        self.ingredient_name = ingredient_name
        self._supplier_id = supplier.id
        self.price_per_kg = price_per_kg
        supplier.add_ingredient(self)

class Product_Ingredient:
    def __init__(self, product: Product, ingredient: Ingredient, quantity_in_grams: int):
        self.product = product
        self.ingredient = ingredient
        self.quantity_in_grams = quantity_in_grams

class Order_Details:
    def __init__(self, product: Product, full_order: Full_Order, quantity: int, price: float):
        self._product_id = product.id  # Встановлюємо ID продукту
        self._full_order_id = full_order.id  # Встановлюємо ID замовлення
        self.quantity = quantity
        self.price = price

class Promotion(Base):
    def __init__(self, promotion_name: str, discount_percentage: float, beginning_date: str, end_date: str):
        super().__init__()
        self.promotion_name = promotion_name
        self.discount_percentage = discount_percentage
        self.beginning_date = beginning_date
        self.end_date = end_date

class Promotion_Product:
    def __init__(self, promotion: Promotion, product: Product, quantity: int):
        self.promotion = promotion
        self.product = product
        self.quantity = quantity

class Review(Base):
    def __init__(self, customer: Customer, product: Product, rating: int, review_comment: str | None = None):
        super().__init__()
        self._customer_id = customer.id
        self.product_id = product.id
        self.rating = rating
        self.review_comment = review_comment

class LoyaltyProgram(Base):
    def __init__(self, customer: Customer, full_order: Full_Order, points_earned: int, points_to_use: int):
        super().__init__()
        self._customer_id = customer.id
        self._full_order_id = full_order.id
        self.points_earned = points_earned
        self.points_to_use = points_to_use


customer1 = Customer(
    first_name="Olexandr",
    last_name="Tkach",
    email="oleksandr.tkach@gmail.com",
    phone="0631234567",
    date_of_birth="1990-04-05",
    password="secure_pass1"
)

customer2 = Customer(
    first_name="Maria",
    last_name="Yakovleva",
    email="maria3849@gmail.com",
    phone="0672345678",
    date_of_birth="1988-06-10",
    password="secure_pass2"
)

customer3 = Customer(
    first_name="Anna",
    last_name="Sydorchuk",
    email="anna.sydorenko@gmail.com",
    phone="0953456789",
    date_of_birth="1992-03-12",
    password="secure_pass3"
)

print(customer1.full_name)

category1 = Category(category_name="Cakes")
category2 = Category(category_name="Cupcakes")
category3 = Category(category_name="Mousse Cakes")
category4 = Category(category_name="Cookies")
category5 = Category(category_name="Cheesecakes")


product1 = Product(
    category=category1, 
    product_name="Fruit Cake",
    price=350.00,
    description="Cake with assorted fruits and light cream."
)


product2 = Product(
    category=category1,
    product_name="Napoleon Cake",
    price=280.00,
    description="Traditional cake made with puff pastry."
)

product3 = Product(
    category=category2,
    product_name="Lemon Cupcake",
    price=75.00,
    description="Refreshing cupcake with lemon cream."
)

supplier1 = Supplier(
    supplier_name="Best Ingredients",
    first_name="John",
    last_name="Doe",
    phone="+380631234567",
    email="bestingredients@gmail.com"
)

ingredient1 = Ingredient(
    ingredient_name="Flour",
    supplier=supplier1,
    price_per_kg=12.00
)

product_ingredient1 = Product_Ingredient(
    product=product1,
    ingredient=ingredient1,
    quantity_in_grams=200
)

promotion1 = Promotion(
    promotion_name="Summer Discount",
    discount_percentage=10.00,
    beginning_date="2024-06-01",
    end_date="2024-08-31"
)

promotion_product = Promotion_Product(promotion1, product1, 1)
promotion_product = Promotion_Product(promotion1, product3, 6)

full_order1 = Full_Order(
    customer=customer1,
    payment_type=PaymentType.CREDIT_CARD,
    payment_status=PaymentStatus.COMPLETED,
    total_amount=700.00,
    points_used=0
)

order_detail1 = Order_Details(
    product=product1,
    full_order=full_order1,
    quantity=1,
    price=350.00
)

order_detail2 = Order_Details(
    product=product2,
    full_order=full_order1,
    quantity=1,
    price=280.00
)

order_detail3 = Order_Details(
    product=product3,
    full_order=full_order1,
    quantity=1,
    price=75.00
)

full_order2 = Full_Order(
    customer=customer2,
    payment_type=PaymentType.PAYPAL,
    payment_status=PaymentStatus.COMPLETED,
    total_amount=150.00,
    points_used=0
)

order_detail4 = Order_Details(
    product=product3,
    full_order=full_order2,
    quantity=2,
    price=150.00
)

delivery1 = Delivery(
    full_order = full_order1,
    customer=customer1,
    delivery_date="2024-12-01",
    delivery_address="123 Main St, Kyiv",
    delivery_status=DeliveryStatus.PENDING,
)

delivery2 = Delivery(
    full_order = full_order2,
    customer=customer2,
    delivery_date="2024-11-15",
    delivery_address="456 Maple Ave, Lviv",
    delivery_status=DeliveryStatus.SHIPPED,
)

#демонстрація поліморфізму
print(customer1.show_info()) 
print(supplier1.show_info())  

print(customer1.change_password("secure_pass1", "new_secure_pass1"))
