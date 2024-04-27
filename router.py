from flask import Blueprint, request, jsonify
from model import add_user,add_expense,simplify_balances, balances, display_balances, users

expense = Blueprint('expense', __name__)
groups = {}
group_members = {}

@expense.route('/add_user', methods=['POST'])
def handle_add_user():
    data = request.json
    add_user(data['user_id'], data['name'], data['email'], data['mobile'])
    return jsonify({"message": "User added successfully"}), 200

@expense.route('/get_users', methods = ['GET'])
def get_all_user_details():
    return jsonify(users), 200

@expense.route('/add_expense', methods=['POST'])
def handle_add_expense():
    data = request.json
    result = add_expense(data['payer_id'], data['amount'], data['split_type'], data['shares'], data['involved_users'])
    return jsonify({"message": result}), 200


@expense.route('/balances', methods=['GET'])
def get_balances():
    balances_str_keys = {str(key): value for key, value in balances.items()}
    return jsonify(balances_str_keys), 200

@expense.route('/simplify', methods=['POST'])
def simplify_expenses():
    data = request.json
    # balances = {eval(key): value for key, value in balances.items()}
    balances = {tuple(key.split('_')): value for key, value in data['balances'].items()}
    new_balances = simplify_balances(balances)
    new_balances_str_keys = {str(key): value for key, value in new_balances.items()}
    return jsonify({"message": "Expenses simplified", "new_balances": new_balances_str_keys})


@expense.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    group_id = data['group_id']
    group_name = data['group_name']
    payer_id = data['user_id']
    
    if payer_id not in users:
        return jsonify({"error": "Payer does not exist"}), 404
    
    groups[group_id] = {'group_name': group_name, 'group_id': group_id, 'payer_id': payer_id}
    group_members[group_id] = [payer_id]  # Add payer as the first member
    return jsonify({"message": "Group created successfully", "group_id": group_id}), 200

@expense.route('/add_user_to_group', methods=['POST'])
def add_user_to_group():
    data = request.json
    group_id = data['group_id']
    user_id = data['user_id']
    
    if group_id not in groups:
        return jsonify({"error": "Group does not exist"}), 404
    if user_id not in users:
        return jsonify({"error": "User does not exist"}), 404
    if groups[group_id]['payer_id'] != request.json.get('payer_id'):
        return jsonify({"error": "Only group payer can add users"}), 403
    
    group_members[group_id].append(user_id)
    return jsonify({"message": "User added to group successfully"}), 200

@expense.route('/list_groups', methods=['GET'])
def list_groups():
    return jsonify(groups), 200