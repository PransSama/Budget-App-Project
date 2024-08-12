class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            items += f"{item['description'][:23]:23}{item['amount']:>7.2f}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    # Calculate total withdrawals and percentages
    total_withdrawn = 0
    category_spending = []
    for category in categories:
        withdrawals = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        category_spending.append(withdrawals)
        total_withdrawn += withdrawals

    percentages = [(spending / total_withdrawn) * 100 for spending in category_spending]

    # Create chart string
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for percentage in percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    # Add category names vertically
    max_length = max(len(category.name) for category in categories)
    for i in range(max_length):
        chart += "     "
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        chart += "\n"

    return chart.rstrip("\n")


# Example Usage
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")

clothing = Category("Clothing")
clothing.deposit(500, "initial deposit")
clothing.withdraw(50.89, "clothes")

entertainment = Category("Entertainment")
entertainment.deposit(300, "initial deposit")
entertainment.withdraw(89.99, "movies and games")

food.transfer(50, clothing)

print(food)
print(clothing)
print(entertainment)
print(create_spend_chart([food, clothing, entertainment]))
