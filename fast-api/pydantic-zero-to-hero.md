# Pydantic Zero to Hero

A compact Pydantic guide with practical examples for common and advanced use cases.

## 1. Install

```bash
pip install pydantic
```

## 2. Basic model definition

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

user = User(id=1, name='Alice', email='alice@example.com')
print(user)
```

## 3. Data validation and coercion

Pydantic converts strings to the correct types where possible.

```python
user = User(id='1', name='Alice', email='alice@example.com')
assert user.id == 1
```

## 4. Optional fields and defaults

```python
from typing import Optional

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.0

prod = Product(name='Book')
assert prod.description is None
assert prod.price == 0.0
```

## 5. Constrained types and field metadata

```python
from pydantic import Field, PositiveInt, constr

class Order(BaseModel):
    quantity: PositiveInt
    sku: constr(min_length=3, strip_whitespace=True) = Field(..., alias='product_sku')

order = Order(quantity='5', product_sku='  ABC  ')
assert order.sku == 'ABC'
```

## 6. Nested models

```python
class Address(BaseModel):
    street: str
    city: str
    zipcode: str

class Customer(BaseModel):
    name: str
    address: Address

customer = Customer(
    name='Bob',
    address={'street': '1 Main St', 'city': 'NYC', 'zipcode': '10001'}
)
assert customer.address.city == 'NYC'
```

## 7. Lists, tuples, and dictionaries

```python
from typing import List, Dict, Tuple

class Basket(BaseModel):
    items: List[str]
    quantities: Dict[str, int]
    coords: Tuple[float, float]

basket = Basket(items=['apple', 'banana'], quantities={'apple': 3}, coords=('12.34', '56.78'))
assert basket.coords == (12.34, 56.78)
```

## 8. Immutable models

```python
class ConfiguredModel(BaseModel):
    x: int

    model_config = {
        'frozen': True,
    }

m = ConfiguredModel(x=1)
# m.x = 2  # raises TypeError
```

## 9. Aliases and field population

```python
class Item(BaseModel):
    item_id: int = Field(..., alias='id')
    name: str

obj = Item.model_validate({'id': 10, 'name': 'Shoes'})
assert obj.item_id == 10
```

## 10. Model serialization

```python
item = Item.model_validate({'id': 10, 'name': 'Shoes'})
print(item.model_dump())
print(item.model_dump_json())
```

## 11. Custom validators

```python
from pydantic import field_validator
from datetime import date

class Event(BaseModel):
    name: str
    date: date

    @field_validator('name')
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('name cannot be blank')
        return value

    @field_validator('date')
    def not_past(cls, value: date) -> date:
        if value < date.today():
            raise ValueError('date cannot be in the past')
        return value
```

## 12. Root validators

```python
from pydantic import root_validator

class Range(BaseModel):
    start: int
    end: int

    @root_validator
    def check_range(cls, values):
        start, end = values.get('start'), values.get('end')
        if start is not None and end is not None and start > end:
            raise ValueError('start must be <= end')
        return values
```

## 13. Settings management with BaseSettings

```python
from pydantic import BaseSettings

class AppSettings(BaseSettings):
    app_name: str = 'My App'
    debug: bool = False

settings = AppSettings()
print(settings.app_name)
```

## 14. Parsing data from environment

```bash
export APP_NAME='Test App'
python -c "from app import AppSettings; print(AppSettings().app_name)"
```

## 15. Model inheritance and reuse

```python
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
```

## 16. ORM mode

```python
class UserORM(BaseModel):
    id: int
    username: str

    model_config = {
        'from_attributes': True,
    }

class UserObject:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username

user_obj = UserObject(id=1, username='john')
user = UserORM.model_validate(user_obj)
```

## 17. Custom types and validators

```python
from pydantic import BaseModel, EmailStr, AnyUrl

class Contact(BaseModel):
    email: EmailStr
    website: AnyUrl

contact = Contact(email='user@example.com', website='https://example.com')
```

## 18. Date and time handling

```python
from datetime import datetime

class EventTime(BaseModel):
    start: datetime

event = EventTime(start='2024-01-01T12:00:00Z')
```

## 19. Error details and validation exceptions

```python
from pydantic import ValidationError

try:
    User.model_validate({'id': 'x', 'name': '', 'email': 'invalid'})
except ValidationError as exc:
    print(exc)
    print(exc.errors())
```

## 20. Extra fields and strictness

```python
class StrictItem(BaseModel):
    name: str

    model_config = {
        'extra': 'forbid',
    }

# StrictItem.model_validate({'name': 'x', 'price': 5})  # raises ValidationError
```

## 21. Model copy and update

```python
item = Item.model_validate({'id': 10, 'name': 'Shoes'})
new_item = item.model_copy(update={'name': 'Boots'})
```

## 22. Json encoding customization

```python
from decimal import Decimal
from pydantic import BaseModel

class PriceData(BaseModel):
    cost: Decimal

print(PriceData(cost='12.50').model_dump_json())
```

## 23. Working with generic models

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    status: str

class Message(BaseModel):
    text: str

response = Response[Message](data={'text': 'OK'}, status='success')
```

## 24. Recommended workflow

- Start with `BaseModel` for domain shapes
- Use `Field(...)` for metadata and constraints
- Prefer `field_validator` for property validation
- Use `BaseSettings` for config values
- Keep models small and reusable
- Use `.model_dump()` / `.model_dump_json()` for output

## 25. FastAPI integration notes

- fastapi automatically uses Pydantic models for request body validation
- response models are serialized with `model_dump`
- nested models, lists, and optional fields work out of the box

```python
from fastapi import FastAPI

app = FastAPI()

@app.post('/users', response_model=User)
async def create_user(user: User):
    return user
```

---

This guide is designed as a rapid reference for the most useful Pydantic features used in modern Python APIs.