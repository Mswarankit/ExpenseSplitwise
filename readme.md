#### Create Groups
Payloads: (create_groups)

{
 "group_id": 1,
 "group_name": "Splits1",
 "user_id": "1"
}
#### Adding groups
Payloads: (adding groups)

{
 "group_id": 1,
 "user_id": "2",
 "payer_id": "1" 
}

#### Adding Users
Payloads(add_user)
{
  "userid": "123456",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890"
}

#### Expenses(Ex1, Ex2, Ex3)
Payloads: (add_expenses)

{
  "payer_id": "u1",
  "amount": 1000,
  "split_type": "EQUAL",
  "shares": [],
  "involved_users": ["u1", "u2", "u3", "u4"]
}

{
  "payer_id": "u1",
  "amount": 1250,
  "split_type": "EXACT",
  "shares": [370, 880],
  "involved_users": ["u2", "u3"]
}

{
  "payer_id": "u4",
  "amount": 1200,
  "split_type": "PERCENT",
  "shares": [40, 20, 20, 20],
  "involved_users": ["u1", "u2", "u3", "u4"]
}

#### Simplify
Payloads: (simplyfy)
{
 "balances": {
    "user1_user2": 250,
    "user2_user3": 200
 }
}



## User Management, Expense Management and Balance Simplification


## Function Design
#### User

- **Properties**: `user_id`, `name`, `email`, `mobile`
- **Methods**: `add_user()`, `get_user()`

#### Expense

- **Properties**: `payer_id`, `amount`, `split_type`, `shares`, `involved_users`
- **Methods**: `add_expense()`, `get_expense()`

#### Balance

- **Properties**: `user1_user2`
- **Methods**: `add_balance()`, `get_balance()`, `simplify_balances()`


## Parameter Schema

### Users

- `user_id` (Primary Key)
- `name`
- `email`
- `mobile`

### Expenses

- `expense_id` (Primary Key)
- `payer_id` (Foreign Key referencing Users)
- `amount`
- `split_type`
- `shares`
- `involved_users`

### Balances

- `user1_user2` (Primary Key)
- `amount`

### Frameworks Flask
From flask, `(main -> router -> model)`