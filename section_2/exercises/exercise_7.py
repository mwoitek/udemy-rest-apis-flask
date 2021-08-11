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

    @classmethod
    def franchise(cls, store):
        return cls(store.name + " - franchise")

    @staticmethod
    def store_details(store):
        return "".join(
            [
                store.name,
                ", total stock price: ",
                str(store.stock_price()),
            ]
        )


store = Store("Test")
store.add_item("Item 1", 10)
store.add_item("Item 2", 30)
store.add_item("Item 3", 60)

store_franchise = Store.franchise(store)
print(store_franchise.name)
print(store_franchise.items)

print(Store.store_details(store))
