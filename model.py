users = {}
balances = {}
groups = {}  
group_members = {}

def add_user(user_id, name, email, mobile):
    users[user_id] = {'name': name, 'email': email, 'mobile': mobile}    


def add_expense(payer_id, amount, split_type, shares, involved_users):
    if split_type == 'EQUAL':
        each_share = round(amount / len(involved_users), 2)
        last_share = round(amount - (each_share * (len(involved_users) - 1)), 2)
        for i, user in enumerate(involved_users):
            if user != payer_id:
                update_balance(user, payer_id, last_share if i == len(involved_users) - 1 else each_share)

    elif split_type == 'EXACT':
        if sum(shares) != amount:
            return "Error: Shares do not sum up to the total amount"
        for share, user in zip(shares, involved_users):
            if user != payer_id:
                update_balance(user, payer_id, share)

    elif split_type == 'PERCENT':
        if sum(shares) != 100:
            return "Error: Percentages do not sum up to 100"
        for percent, user in zip(shares, involved_users):
            if user != payer_id:
                share = round((amount * (percent / 100)), 2)
                update_balance(user, payer_id, share)

    return f"Expense added successfully {display_balances()}"

def update_balance(owed_user, owing_user, amount):
    if (owing_user, owed_user) in balances:
        existing_balance = balances[(owing_user ,owed_user)]
        if existing_balance > amount:
            balances[(owing_user, owed_user)] = round(existing_balance - amount, 2)
        elif existing_balance < amount:
            balances.pop((owing_user, owed_user))
            balances[(owed_user, owing_user)] = round(amount - existing_balance, 2)
        else:
            balances.pop((owing_user, owed_user))
    else:
        balances[(owed_user, owing_user)] = round(balances.get((owed_user, owing_user), 0) + amount, 2)

def display_balances():
    formatted_balances = {}
    for (owed_user, owing_user), amount in balances.items():
        if amount > 0:  
            if owing_user not in formatted_balances:
                formatted_balances[owing_user] = []
            formatted_balances[owing_user].append(f"{owed_user} owes {owing_user}: Rs {amount:.2f}")
    return formatted_balances

def simplify_balances(balances):
    bal = {}
    for (user_owed, user_owing), amount in balances.items():
        if user_owed not in bal:
            bal[user_owed] = {}
        if user_owing not in bal:
            bal[user_owing] = {}
        bal[user_owed][user_owing] = bal[user_owed].get(user_owing, 0) + amount
        bal[user_owing][user_owed] = bal[user_owing].get(user_owed, 0) - amount

    
    for user in list(bal.keys()):
        for debtor in list(bal[user].keys()):
            if bal[user][debtor] > 0:
                debt_amount = bal[user][debtor]
                for creditor in list(bal[debtor].keys()):
                    if creditor != user and bal[debtor][creditor] > 0:
                        transfer_amount = min(debt_amount, bal[debtor][creditor])
                        bal[user][creditor] = bal[user].get(creditor, 0) + transfer_amount
                        bal[debtor][creditor] -= transfer_amount
                        bal[user][debtor] -= transfer_amount
                        if bal[debtor][creditor] == 0:
                            del bal[debtor][creditor]
                        if bal[user][debtor] == 0:
                            del bal[user][debtor]


    new_balances = {}
    for user, debts in bal.items():
        for debtor, amount in debts.items():
            if amount > 0:
                new_balances[(user, debtor)] = amount

    return new_balances
