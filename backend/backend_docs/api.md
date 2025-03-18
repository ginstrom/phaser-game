# API Documentation

## Root Endpoint

- URL: `/`
- Method: `GET`
- Description: Serves the game's home page with information about the game and links to API documentation
- Response: HTML page containing:
  - Game description
  - Key 4X gameplay features
  - Links to API documentation and endpoints

## Game API

Base URL: `/api/games/`

### List Games
- **Method**: GET
- **URL**: `/api/games/`
- **Response**: List of game objects
```json
[
    {
        "id": 1,
        "turn": 1,
        "empires": [...],
        "systems": [...]
    }
]
```

### Create Game
- **Method**: POST
- **URL**: `/api/games/`
- **Body**: Empty object (game is created with default settings)
- **Response**: Created game object

### Retrieve Game
- **Method**: GET
- **URL**: `/api/games/{id}/`
- **Response**: Game object
```json
{
    "id": 1,
    "turn": 1,
    "empires": [...],
    "systems": [...]
}
```

### End Turn
- **Method**: POST
- **URL**: `/api/games/{id}/end_turn/`
- **Description**: End the current turn and start the next one. This will:
  - Process resource production from planets and asteroid belts
  - Update empire resources
  - Process any pending actions
  - Increment the turn counter
- **Response**: Updated game object containing:
  - Current turn number
  - List of empires with updated resources
  - List of systems with updated production
  - Other game state information
```json
{
    "id": 1,
    "turn": 2,
    "empires": [
        {
            "id": 1,
            "name": "Human Empire",
            "mineral_storage": "150.00",
            "organic_storage": "200.00",
            "radioactive_storage": "175.00",
            "exotic_storage": "125.00"
        }
    ],
    "systems": [
        {
            "id": 1,
            "x": 0,
            "y": 0,
            "star": {...},
            "planets": [...],
            "asteroid_belts": [...]
        }
    ]
}
```
- **Error Responses**:
  - 404 Not Found: Game with specified ID does not exist
  - 400 Bad Request: Game is in an invalid state for ending turn
  - 403 Forbidden: Player does not have permission to end turn

### Delete Game
- **Method**: DELETE
- **URL**: `/api/games/{id}/`
- **Response**: 204 No Content

## API Endpoints

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
- **URL**: `/api/players/`
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
- **URL**: `/api/players/`
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
- **URL**: `/api/players/{id}/`
- **Method**: GET
- **Response**: Player object
```json
{
    "id": 1,
    "player_type": "human"
}
```

#### Update Player
- **URL**: `/api/players/{id}/`
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
- **URL**: `/api/players/{id}/`

## Game Start Endpoint

### POST /api/games/start/

Start a new game with specified parameters.

#### Request Body
```json
{
    "player_empire_name": "string",
    "computer_empire_count": "integer",
    "galaxy_size": "string (one of: tiny, small, medium, large)"
}
```

#### Response
- Success (201 Created):
```json
{
    "id": "integer",
    "turn": 1,  // First turn after game creation
    "empires": ["integer array of empire IDs"],
    "systems": ["integer array of system IDs"]
}
```

- Error (400 Bad Request):
```json
{
    "galaxy_size": ["Invalid choice. Valid choices are: tiny, small, medium, large"],
    "player_empire_name": ["This field is required"],
    "computer_empire_count": ["This field is required"]
}
```

#### Notes
- Galaxy sizes determine the number of star systems:
  - tiny: 2 systems
  - small: 5 systems
  - medium: 10 systems
  - large: 15 systems
- The game will be created with the specified number of computer empires plus one human empire
- All empires start with basic resources and one home system
- Games start at turn 0 and advance to turn 1 after initialization