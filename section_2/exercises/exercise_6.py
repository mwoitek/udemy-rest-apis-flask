class Store:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, name, price):
        self.items.append(
            {
                "name": name,
                "price": price,
            }
        )

    def stock_price(self):
        total = 0
        for item in self.items:
            total += item["price"]
        return total


store = Store("Test")
print(store.name)
print(store.items)

store.add_item("Item 1", 10)
store.add_item("Item 2", 30)
store.add_item("Item 3", 60)
print(store.items)

print(store.stock_price())
