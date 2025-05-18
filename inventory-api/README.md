# Inventory API

A Flask-based API for managing inventory with PostgreSQL database.

## API Endpoints

### 1. Health Check
- **URL**: `/`
- **Method**: `GET`
- **Success Response**: `200 OK`
  ```json
  {
    "status": "ok",
    "service": "inventory-api",
    "database": "healthy",
    "timestamp": "2023-01-01T12:00:00"
  }
  ```

### 2. Add Inventory
- **URL**: `/inventory`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "sku": "PROD-001",
    "quantity": 10
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 1,
    "sku": "PROD-001",
    "quantity_added": 10,
    "created_at": "2023-01-01T12:00:00"
  }
  ```

### 3. Get Inventory by SKU
- **URL**: `/inventory/<sku>`
- **Method**: `GET`
- **Success Response**: `200 OK`
  ```json
  {
    "sku": "PROD-001",
    "total_quantity": 10,
    "last_updated": "2023-01-01T12:00:00",
    "entry_count": 1
  }
  ```
- **Error Response**: `404 Not Found`
  ```json
  {
    "error": "SKU not found",
    "sku": "PROD-001",
    "total_quantity": 0
  }
  ```

## Postman Collection

A Postman collection is included in this repository for testing the API:
- `inventory-api-postman-collection.json`

To use the collection:
1. Import the collection into Postman
2. Set the `base_url` variable to your API endpoint (default: `http://localhost:5000`)
3. Run the requests to test the API functionality