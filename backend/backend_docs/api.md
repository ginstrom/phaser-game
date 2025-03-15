# API Documentation

## Planet Resource

Base URL: `/api/planets/`

### List Planets
- **Method**: GET
- **URL**: `/api/planets/`
- **Response**: List of planet objects
```json
[
    {
        "id": 1,
        "mineral_production": "75.50",
        "organic_production": "25.25",
        "radioactive_production": "60.75",
        "exotic_production": "40.25",
        "mineral_storage_capacity": "150.50",
        "organic_storage_capacity": "200.75",
        "radioactive_storage_capacity": "175.25",
        "exotic_storage_capacity": "125.75",
        "orbit": 3
    }
]
```

### Create Planet
- **Method**: POST
- **URL**: `/api/planets/`
- **Body**: Planet object
```json
{
    "mineral_production": "80.50",
    "organic_production": "30.25",
    "radioactive_production": "65.75",
    "exotic_production": "45.25",
    "mineral_storage_capacity": "160.50",
    "organic_storage_capacity": "210.75",
    "radioactive_storage_capacity": "185.25",
    "exotic_storage_capacity": "135.75",
    "orbit": 2
}
```
- **Response**: Created planet object with ID

### Retrieve Planet
- **Method**: GET
- **URL**: `/api/planets/{id}/`
- **Response**: Single planet object

### Update Planet
- **Method**: PATCH/PUT
- **URL**: `/api/planets/{id}/`
- **Body**: Partial (PATCH) or complete (PUT) planet object
```json
{
    "mineral_production": "90.50",
    "orbit": 4
}
```
- **Response**: Updated planet object

### Delete Planet
- **Method**: DELETE
- **URL**: `/api/planets/{id}/`
- **Response**: 204 No Content

### Field Specifications

All resource values are decimal numbers with 2 decimal places precision.

| Field | Type | Description | Default |
|-------|------|-------------|----------|
| mineral_production | decimal | Base mineral production per turn | 50.00 |
| organic_production | decimal | Base organic production per turn | 50.00 |
| radioactive_production | decimal | Base radioactive production per turn | 50.00 |
| exotic_production | decimal | Base exotic production per turn | 50.00 |
| mineral_storage_capacity | decimal | Maximum mineral storage capacity | 100.00 |
| organic_storage_capacity | decimal | Maximum organic storage capacity | 100.00 |
| radioactive_storage_capacity | decimal | Maximum radioactive storage capacity | 100.00 |
| exotic_storage_capacity | decimal | Maximum exotic storage capacity | 100.00 |
| orbit | integer | Orbital position from star (1 being closest) | 1 |

## Star Resource

Base URL: `/api/stars/`

### List Stars
- **Method**: GET
- **URL**: `/api/stars/`
- **Response**: List of star objects
```json
[
    {
        "id": 1,
        "star_type": "blue"
    }
]
```

### Create Star
- **Method**: POST
- **URL**: `/api/stars/`
- **Body**: Star object
```json
{
    "star_type": "yellow"
}
```
- **Response**: Created star object with ID

### Retrieve Star
- **Method**: GET
- **URL**: `/api/stars/{id}/`
- **Response**: Single star object

### Update Star
- **Method**: PATCH/PUT
- **URL**: `/api/stars/{id}/`
- **Body**: Partial (PATCH) or complete (PUT) star object
```json
{
    "star_type": "white"
}
```
- **Response**: Updated star object

### Delete Star
- **Method**: DELETE
- **URL**: `/api/stars/{id}/`
- **Response**: 204 No Content

### Field Specifications

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| star_type | string | The type of star | blue, white, yellow, orange, brown | 

## AsteroidBelt Resource

Base URL: `/api/asteroid-belts/`

### List Asteroid Belts
- **Method**: GET
- **URL**: `/api/asteroid-belts/`
- **Response**: List of asteroid belt objects
```json
[
    {
        "id": 1,
        "mineral_production": "75.50",
        "organic_production": "25.25",
        "radioactive_production": "60.75",
        "exotic_production": "40.25",
        "orbit": 4
    }
]
```

### Create Asteroid Belt
- **Method**: POST
- **URL**: `/api/asteroid-belts/`
- **Body**: Asteroid Belt object
```json
{
    "mineral_production": "80.50",
    "organic_production": "30.25",
    "radioactive_production": "65.75",
    "exotic_production": "45.25",
    "orbit": 2
}
```
- **Response**: Created asteroid belt object with ID

### Retrieve Asteroid Belt
- **Method**: GET
- **URL**: `/api/asteroid-belts/{id}/`
- **Response**: Single asteroid belt object

### Update Asteroid Belt
- **Method**: PATCH/PUT
- **URL**: `/api/asteroid-belts/{id}/`
- **Body**: Partial (PATCH) or complete (PUT) asteroid belt object
```json
{
    "mineral_production": "90.50",
    "orbit": 5
}
```
- **Response**: Updated asteroid belt object

### Delete Asteroid Belt
- **Method**: DELETE
- **URL**: `/api/asteroid-belts/{id}/`
- **Response**: 204 No Content

### Field Specifications

All resource values are decimal numbers with 2 decimal places precision.

| Field | Type | Description | Default |
|-------|------|-------------|----------|
| mineral_production | decimal | Base mineral production per turn | 50.00 |
| organic_production | decimal | Base organic production per turn | 50.00 |
| radioactive_production | decimal | Base radioactive production per turn | 50.00 |
| exotic_production | decimal | Base exotic production per turn | 50.00 |
| orbit | integer | Orbital position from star (1 being closest) | 1 | 