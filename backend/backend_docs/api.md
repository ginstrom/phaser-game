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

## Systems API

### List Systems
`GET /api/systems/`

Returns a list of all star systems in the galaxy.

Response:
```json
[
    {
        "id": 1,
        "x": 1,
        "y": 1,
        "star": {
            "id": 1,
            "star_type": "yellow"
        },
        "planets": [
            {
                "id": 1,
                "mineral_production": "50.00",
                "organic_production": "50.00",
                "radioactive_production": "50.00",
                "exotic_production": "50.00",
                "mineral_storage_capacity": "100.00",
                "organic_storage_capacity": "100.00",
                "radioactive_storage_capacity": "100.00",
                "exotic_storage_capacity": "100.00",
                "orbit": 1
            }
        ],
        "asteroid_belts": [
            {
                "id": 1,
                "mineral_production": "50.00",
                "organic_production": "50.00",
                "radioactive_production": "50.00",
                "exotic_production": "50.00",
                "orbit": 2
            }
        ]
    }
]
```

### Create System
`POST /api/systems/`

Creates a new star system.

Request:
```json
{
    "x": 1,
    "y": 1,
    "star": {
        "star_type": "yellow"
    }
}
```

### Retrieve System
`GET /api/systems/{id}/`

Returns details of a specific star system.

### Update System
`PUT /api/systems/{id}/`

Updates a star system.

Request:
```json
{
    "x": 2,
    "y": 2,
    "star": {
        "star_type": "blue"
    }
}
```

### Delete System
`DELETE /api/systems/{id}/`

Deletes a star system.

### Add Planet to System
`POST /api/systems/{id}/add_planet/`

Adds a planet to a star system.

Request:
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
    "orbit": 1
}
```

### Add Asteroid Belt to System
`POST /api/systems/{id}/add_asteroid_belt/`

Adds an asteroid belt to a star system.

Request:
```json
{
    "mineral_production": "80.50",
    "organic_production": "30.25",
    "radioactive_production": "65.75",
    "exotic_production": "45.25",
    "orbit": 2
}
```

### System Constraints
- Each system must have unique x,y coordinates in the galaxy
- Each system has exactly one star
- Each system can have up to MAX_ORBITS (5) planets and/or asteroid belts
- Each orbit (1 to MAX_ORBITS) can be occupied by either a planet or an asteroid belt, but not both
- Attempting to add a celestial body to an occupied orbit will result in a 400 Bad Request error
- Attempting to add more than MAX_ORBITS celestial bodies will result in a 400 Bad Request error 

## Player API

### Endpoints

#### List Players
- **URL**: `/api/play/players/`
- **Method**: GET
- **Response**: List of player objects
```json
[
    {
        "id": 1,
        "player_type": "human"
    },
    {
        "id": 2,
        "player_type": "computer"
    }
]
```

#### Create Player
- **URL**: `/api/play/players/`
- **Method**: POST
- **Data**:
```json
{
    "player_type": "human"  // or "computer"
}
```
- **Response**: Created player object
```json
{
    "id": 1,
    "player_type": "human"
}
```

#### Get Player
- **URL**: `/api/play/players/{id}/`
- **Method**: GET
- **Response**: Player object
```json
{
    "id": 1,
    "player_type": "human"
}
```

#### Update Player
- **URL**: `/api/play/players/{id}/`
- **Method**: PUT
- **Data**:
```json
{
    "player_type": "computer"
}
```
- **Response**: Updated player object
```json
{
    "id": 1,
    "player_type": "computer"
}
```

#### Delete Player
- **URL**: `/api/play/players/{id}/`
- **Method**: DELETE
- **Response**: 204 No Content

### Field Specifications

#### Player
- `id` (integer, read-only): Unique identifier for the player
- `player_type` (string, required): Type of player
  - Allowed values: "human", "computer"
  - Default: "human" 

## Race API

### List Races
- **URL**: `/api/races/`
- **Method**: GET
- **Description**: Retrieve a list of all races
- **Response**: 200 OK
```json
[
    {
        "id": 1,
        "name": "Humans"
    },
    {
        "id": 2,
        "name": "Vulcans"
    }
]
```

### Create Race
- **URL**: `/api/races/`
- **Method**: POST
- **Description**: Create a new race
- **Request Body**:
```json
{
    "name": "Klingons"
}
```
- **Response**: 201 Created
```json
{
    "id": 3,
    "name": "Klingons"
}
```
- **Error Response**: 400 Bad Request (if name already exists)

### Get Race
- **URL**: `/api/races/{id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific race
- **Response**: 200 OK
```json
{
    "id": 1,
    "name": "Humans"
}
```

### Update Race
- **URL**: `/api/races/{id}/`
- **Method**: PUT
- **Description**: Update a specific race
- **Request Body**:
```json
{
    "name": "Updated Race Name"
}
```
- **Response**: 200 OK
```json
{
    "id": 1,
    "name": "Updated Race Name"
}
```
- **Error Response**: 400 Bad Request (if name already exists)

### Delete Race
- **URL**: `/api/races/{id}/`
- **Method**: DELETE
- **Description**: Delete a specific race
- **Response**: 204 No Content 

## Empire Resource

Base URL: `/api/empires/`

### List Empires
- **Method**: GET
- **URL**: `/api/empires/`
- **Response**: List of empire objects
```json
[
    {
        "id": 1,
        "name": "Test Empire",
        "player": 1,
        "race": 1,
        "planets": [1, 2],
        "asteroid_belts": [1],
        "mineral_storage": 0,
        "organic_storage": 0,
        "radioactive_storage": 0,
        "exotic_storage": 0,
        "resource_capacities": {
            "mineral_capacity": 400,
            "organic_capacity": 500,
            "radioactive_capacity": 600,
            "exotic_capacity": 700
        }
    }
]
```

### Create Empire
- **Method**: POST
- **URL**: `/api/empires/`
- **Body**: Empire object
```json
{
    "name": "New Empire",
    "player": 1,
    "race": 1,
    "planets": [],
    "asteroid_belts": [],
    "mineral_storage": 0,
    "organic_storage": 0,
    "radioactive_storage": 0,
    "exotic_storage": 0
}
```
- **Response**: Created empire object with ID

### Retrieve Empire
- **Method**: GET
- **URL**: `/api/empires/{id}/`
- **Response**: Single empire object

### Update Empire
- **Method**: PATCH/PUT
- **URL**: `/api/empires/{id}/`
- **Body**: Partial (PATCH) or complete (PUT) empire object
```json
{
    "name": "Updated Empire",
    "planets": [1, 2],
    "mineral_storage": 100
}
```
- **Response**: Updated empire object

### Delete Empire
- **Method**: DELETE
- **URL**: `/api/empires/{id}/`
- **Response**: 204 No Content

### Field Specifications

| Field | Type | Description | Default |
|-------|------|-------------|----------|
| name | string | Name of the empire | Required |
| player | integer | ID of the player who owns this empire | Required |
| race | integer | ID of the race of this empire | Required |
| planets | array | List of planet IDs belonging to this empire | [] |
| asteroid_belts | array | List of asteroid belt IDs belonging to this empire | [] |
| mineral_storage | integer | Current mineral storage | 0 |
| organic_storage | integer | Current organic storage | 0 |
| radioactive_storage | integer | Current radioactive storage | 0 |
| exotic_storage | integer | Current exotic storage | 0 |
| resource_capacities | object | Read-only object containing total resource capacities | N/A |

### Resource Capacities Object

The `resource_capacities` object is a read-only field that provides the total resource storage capacities from all planets in the empire. It is calculated as follows:

- `mineral_capacity`: Sum of `mineral_storage_capacity` from all planets
- `organic_capacity`: Sum of `organic_storage_capacity` from all planets
- `radioactive_capacity`: Sum of `radioactive_storage_capacity` from all planets
- `exotic_capacity`: Sum of `exotic_storage_capacity` from all planets 

## Game API

### Endpoints

#### GET /api/games/
List all games.

Response:
```json
[
    {
        "id": 1,
        "turn": 1,
        "empires": [1, 2],
        "systems": [1, 2]
    }
]
```

#### POST /api/games/
Create a new game.

Request: Empty body (game starts at turn 1)

Response:
```json
{
    "id": 1,
    "turn": 1,
    "empires": [],
    "systems": []
}
```

#### GET /api/games/{id}/
Get details of a specific game.

Response:
```json
{
    "id": 1,
    "turn": 1,
    "empires": [1, 2],
    "systems": [1, 2]
}
```

#### POST /api/games/{id}/end_turn/
End the current turn and start the next one.

Response:
```json
{
    "status": "turn ended",
    "new_turn": 2
}
```

#### DELETE /api/games/{id}/
Delete a game.

Response: 204 No Content

### Validation
- A game must have at least 2 empires
- A game must have at least 2 star systems
- Systems within a game must have unique coordinates 