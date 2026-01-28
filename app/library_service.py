import os

class LibrarySystem:
    def __init__(self, data):
        self.data = data
        self.inventory_map = {}
        self.load_inventory()

    def load_inventory(self):
        filepath = os.path.join(self.data, "current_inventory.txt")
        try:
            with open(filepath, "rt") as f:  
                for line in f:
                    if line.strip():
                        isbn, title, author, status = line.split(",")
                        self.inventory_map[isbn] = {
                            "title": title,
                            "author": author,
                            "status": status.strip()
                        }
        except FileNotFoundError:
            self.inventory_map = {}


    def save_inventory(self):
        filepath = os.path.join(self.data, "current_inventory.txt")
        with open(filepath, "w") as f:  
            for isbn, book in self.inventory_map.items():
                f.write(f"{isbn},{book['title']},{book['author']},{book['status']}\n")

    def get_inventory(self):
        return {
            'books': [
                {'isbn': isbn, **book}
                for isbn, book in self.inventory_map.items()
            ],
            'total_books': len(self.inventory_map),
            'available': sum(1 for b in self.inventory_map.values() if b['status'] == 'available'),
            'checked_out': sum(1 for b in self.inventory_map.values() if b['status'] == 'checked_out')
        }

    def add_book(self, title, author, isbn):
        self.inventory_map[isbn] = {
            'title': title,
            'author': author,
            'status': "available"
        }
        self.save_inventory()
        return True

    def checkout(self, isbn):
        if isbn not in self.inventory_map:
            return False
        elif self.inventory_map[isbn]["status"] == "checked_out":
            return False
        else:
            self.inventory_map[isbn]["status"] = "checked_out"
            self.save_inventory()
            return True

    def search(self, search_input):
        search_input = search_input.lower().strip()
        books = []
        for isbn, book_details in self.inventory_map.items():
            author_info = book_details.get("author", "").lower()
            title_info = book_details.get("title", "").lower()
            if search_input in author_info or search_input in title_info:
                books.append({
                    "isbn": isbn,
                    "title": book_details["title"],
                    "author": book_details["author"],
                    "status": book_details["status"]
                })
        return books

    def remove_book(self, isbn):
        if isbn not in self.inventory_map:
            return False
        else:
            del self.inventory_map[isbn]
            self.save_inventory()
            return True

    def return_book(self, isbn):
        if isbn not in self.inventory_map:
            return False
        self.inventory_map[isbn]["status"] = "available"
        self.save_inventory()
        return True


