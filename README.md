# Library System Web Application (Flask)

## API Endpoints

### 1. Health Check
**GET** `/api/health`  
Returns service status and inventory count.

### 2. View Inventory
**GET** `/api/inventory`  
Returns all books in the library and their status.

### 3. Add a Book
**POST** `/api/add`  
curl -X POST http://127.0.0.1:5001/api/add \
  -H "Content-Type: application/json" \
  -d '{"title":"Dune","author":"Frank Herbert","isbn":"9780441013593"}'

### 4. Search a Book
**POST** `/api/search`
curl -X POST http://127.0.0.1:5001/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Dune"}'

### 5. Checkout a Book
**POST** `/api/checkout`
curl -X POST http://127.0.0.1:5001/api/checkout \
  -H "Content-Type: application/json" \
  -d '{"isbn":"9780441013593"}'