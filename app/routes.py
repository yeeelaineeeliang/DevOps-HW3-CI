from flask import jsonify, request
from app.library_service import LibrarySystem


def register_routes(app):

    @app.get("/")
    def home():
        return {"message": "Library API is running."}, 200

    @app.before_request
    def before_request():
        if not hasattr(app, "library_service"):
            app.library_service = LibrarySystem(app.config["DATA_DIR"])

    @app.route("/api/health", methods=["GET"])
    def health():
        return (
            jsonify(
                {
                    "status": "healthy",
                    "service": "library-api",
                    "inventory_count": len(app.library_service.inventory_map),
                }
            ),
            200,
        )

    # inventory
    @app.route("/api/inventory", methods=["GET"])
    def get_inventory():
        inventory = app.library_service.get_inventory()
        return jsonify(inventory), 200

    # add
    @app.route("/api/add", methods=["POST"])
    def add_book():
        data = request.get_json()

        if not all(k in data for k in ["title", "author", "isbn"]):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Missing required fields: title, author, isbn",
                    }
                ),
                400,
            )

        success = app.library_service.add_book(
            data["title"], data["author"], data["isbn"]
        )

        if success:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"{data['title']} by {data['author']} added",
                        "book": {
                            "isbn": data["isbn"],
                            "title": data["title"],
                            "author": data["author"],
                            "status": "available",
                        },
                    }
                ),
                201,
            )
        else:
            return jsonify({"success": False, "error": "Failed to add book"}), 500

    # checkout
    @app.route("/api/commands/checkout", methods=["POST"])
    def checkout_book():
        data = request.get_json()

        if "isbn" not in data:
            return (
                jsonify({"success": False, "error": "Missing required field: isbn"}),
                400,
            )

        isbn = data["isbn"]
        success = app.library_service.checkout(isbn)

        if success:
            book = app.library_service.inventory_map[isbn]
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"{book['title']} checked out successfully in the inventory",
                        "book": {
                            "isbn": isbn,
                            "title": book["title"],
                            "status": "checked_out",
                        },
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Book not found or already checked out",
                        "isbn": isbn,
                    }
                ),
                400,
            )

    # search
    @app.route("/api/commands/search", methods=["POST"])
    def search_books():
        data = request.get_json()

        if "query" not in data:
            return (
                jsonify({"success": False, "error": "Missing required field: query"}),
                400,
            )

        results = app.library_service.search(data["query"])

        return (
            jsonify(
                {
                    "success": True,
                    "query": data["query"],
                    "results": results,
                    "count": len(results),
                }
            ),
            200,
        )

    # return
    @app.route("/api/commands/return", methods=["POST"])
    def return_book():
        data = request.get_json()

        if "isbn" not in data:
            return (
                jsonify({"success": False, "error": "Missing required field: isbn"}),
                400,
            )

        isbn = data["isbn"]
        success = app.library_service.return_book(isbn)

        if success:
            book = app.library_service.inventory_map[isbn]
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"{book['title']} returned successfully",
                        "book": {
                            "isbn": isbn,
                            "title": book["title"],
                            "status": "available",
                        },
                    }
                ),
                200,
            )
        else:
            return (
                jsonify({"success": False, "error": "Book not found", "isbn": isbn}),
                404,
            )

    # remove
    @app.route("/api/commands/remove", methods=["POST"])
    def remove_book():
        data = request.get_json()

        if "isbn" not in data:
            return (
                jsonify({"success": False, "error": "Missing required field: isbn"}),
                400,
            )

        isbn = data["isbn"]

        # Get book title before removing
        if isbn in app.library_service.inventory_map:
            title = app.library_service.inventory_map[isbn]["title"]
        else:
            return (
                jsonify({"success": False, "error": "Book not found", "isbn": isbn}),
                404,
            )

        success = app.library_service.remove_book(isbn)

        if success:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"{title} removed successfully",
                        "isbn": isbn,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {"success": False, "error": "Failed to remove book", "isbn": isbn}
                ),
                500,
            )
