# Inventory API

A Flask-based API for managing inventory with PostgreSQL database.

# Inventory Application



## Run the dang thing

```sh
sudo yum install git
git clone https://github.com/jamby1100/amazon-q-incident-resolution-demo.git

export POSTGRES_HOST="product-inventory-rds.cpj0axh5w3vv.ap-southeast-1.rds.amazonaws.com"
export POSTGRES_PORT=5432
export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
# note that this changes often coz of Secrets Manager
export POSTGRES_PASSWORD='FO99G]MM~UuR$nq-AfLQODWnlSBZ'
export INVENTORY_SERVICE_URL="inventory-alb-2128711399.ap-southeast-1.elb.amazonaws.com"

# run it on port 5000
python main.py
```

## Running after first install

```sh
source venv/bin/activate
```

## Jamby's corner

```sh
cd amazon-q-incident-resolution-demo/
cd inventory-api/

python3 -m venv venv
source venv/bin/activate

pip install psycopg2-binary
pip install Flask
pip freeze > requirements.txt

pip install -r requirements.txt

export POSTGRES_HOST="product-inventory-rds.cpj0axh5w3vv.ap-southeast-1.rds.amazonaws.com"
export POSTGRES_PORT=5432
export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD="e4_:~SqklKVTj?nk.|oj*Uy6yRip"

# run it on port 5000
python app.py


        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        dbname=os.getenv('POSTGRES_DB', 'inventory_db'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
```

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