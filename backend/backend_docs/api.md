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
        "exotic_storage_capacity": "125.75"
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
    "exotic_storage_capacity": "135.75"
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
    "mineral_production": "90.50"
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