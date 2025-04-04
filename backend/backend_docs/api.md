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
- **URL**: `/api/games/{id}/end-turn/`
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

### List Game Empires
- **Method**: GET
- **URL**: `/api/games/{id}/empires/`
- **Description**: Get all empires in a specific game
- **Response**: List of empire objects
```json
[
    {
        "id": 1,
        "name": "Human Empire",
        "player": 1,
        "race": 1,
        "mineral_storage": "100.00",
        "organic_storage": "150.00",
        "radioactive_storage": "125.00",
        "exotic_storage": "75.00"
    }
]
```
- **Error Responses**:
  - 404 Not Found: Game with specified ID does not exist

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

## Empire API

### Endpoints

#### List Empires
- **URL**: `/api/empires/`
- **Method**: GET
- **Response**: List of empire objects
```json
[
    {
        "id": 1,
        "name": "Human Empire",
        "player": 1,
        "race": 1,
        "mineral_storage": "100.00",
        "organic_storage": "150.00",
        "radioactive_storage": "125.00",
        "exotic_storage": "75.00"
    }
]
```

#### Create Empire
- **URL**: `/api/empires/`
- **Method**: POST
- **Data**:
```json
{
    "name": "Human Empire",
    "player_id": 1,
    "race_id": 1
}
```
- **Response**: Created empire object

#### Get Empire
- **URL**: `/api/empires/{id}/`
- **Method**: GET
- **Response**: Empire object

#### Update Empire
- **URL**: `/api/empires/{id}/`
- **Method**: PUT
- **Data**: Empire object
- **Response**: Updated empire object

#### Delete Empire
- **URL**: `/api/empires/{id}/`
- **Method**: DELETE
- **Response**: 204 No Content

#### Get Empire Planets
- **URL**: `/api/empires/{id}/planets/`
- **Method**: GET
- **Description**: Get all planets belonging to this empire
- **Response**: List of planet objects
```json
[
    {
        "id": 1,
        "orbit": 1,
        "mineral_production": "50.00",
        "organic_production": "50.00",
        "radioactive_production": "50.00",
        "exotic_production": "50.00",
        "mineral_storage_capacity": "100.00",
        "organic_storage_capacity": "100.00",
        "radioactive_storage_capacity": "100.00",
        "exotic_storage_capacity": "100.00"
    }
]
```

#### Get Empire Asteroid Belts
- **URL**: `/api/empires/{id}/asteroid-belts/`
- **Method**: GET
- **Description**: Get all asteroid belts belonging to this empire
- **Response**: List of asteroid belt objects
```json
[
    {
        "id": 1,
        "orbit": 2,
        "mineral_production": "50.00",
        "organic_production": "50.00",
        "radioactive_production": "50.00",
        "exotic_production": "50.00"
    }
]
```

## Research API

### Technology Resource

Base URL: `/api/technologies/`

### List Technologies
- **Method**: GET
- **URL**: `/api/technologies/`
- **Response**: List of technology objects
```json
[
    {
        "id": 1,
        "name": "Advanced Mining",
        "description": "Improves mineral extraction efficiency",
        "cost": "100.00",
        "category": "production",
        "prerequisites": [2, 3]
    }
]
```

### Create Technology
- **Method**: POST
- **URL**: `/api/technologies/`
- **Body**: Technology object
```json
{
    "name": "Advanced Mining",
    "description": "Improves mineral extraction efficiency",
    "cost": "100.00",
    "category": "production"
}
```
- **Response**: Created technology object with ID

### Retrieve Technology
- **Method**: GET
- **URL**: `/api/technologies/{id}/`
- **Response**: Single technology object

### Update Technology
- **Method**: PATCH/PUT
- **URL**: `/api/technologies/{id}/`
- **Body**: Partial (PATCH) or complete (PUT) technology object
```json
{
    "cost": "150.00",
    "description": "Updated description"
}
```
- **Response**: Updated technology object

### Delete Technology
- **Method**: DELETE
- **URL**: `/api/technologies/{id}/`
- **Response**: 204 No Content

### Add Prerequisite
- **Method**: POST
- **URL**: `/api/technologies/{id}/add_prerequisite/`
- **Description**: Add a prerequisite technology that must be researched before this technology
- **Body**:
```json
{
    "prerequisite_id": 1
}
```
- **Response**: Updated technology object with new prerequisite
- **Error Responses**:
  - 400 Bad Request: Missing prerequisite_id
  - 404 Not Found: Prerequisite technology not found

### Remove Prerequisite
- **Method**: POST
- **URL**: `/api/technologies/{id}/remove_prerequisite/`
- **Description**: Remove a prerequisite technology
- **Body**:
```json
{
    "prerequisite_id": 1
}
```
- **Response**: Updated technology object
- **Error Responses**:
  - 400 Bad Request: Missing prerequisite_id
  - 404 Not Found: Prerequisite technology not found

### Field Specifications

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| name | string | Name of the technology | Any string |
| description | string | Detailed description | Any string |
| cost | decimal | Research points needed | Positive decimal |
| category | string | Technology category | production, military, science |
| prerequisites | array | IDs of required technologies | Array of technology IDs |

## Empire Technology Resource

Base URL: `/api/empire-technologies/`

### List Empire Technologies
- **Method**: GET
- **URL**: `/api/empire-technologies/`
- **Response**: List of empire technology objects
```json
[
    {
        "id": 1,
        "empire": 1,
        "technology": 1,
        "research_points": "50.00",
        "is_complete": false
    }
]
```

### Create Empire Technology
- **Method**: POST
- **URL**: `/api/empire-technologies/`
- **Body**: Empire Technology object
```json
{
    "empire": 1,
    "technology": 1
}
```
- **Response**: Created empire technology object
- **Error Responses**:
  - 400 Bad Request: Duplicate empire-technology combination
  - 404 Not Found: Empire or technology not found

### Retrieve Empire Technology
- **Method**: GET
- **URL**: `/api/empire-technologies/{id}/`
- **Response**: Single empire technology object

### Update Empire Technology
- **Method**: PATCH/PUT
- **URL**: `/api/empire-technologies/{id}/`
- **Body**: Partial (PATCH) or complete (PUT) empire technology object
- **Response**: Updated empire technology object

### Delete Empire Technology
- **Method**: DELETE
- **URL**: `/api/empire-technologies/{id}/`
- **Response**: 204 No Content

### Add Research Points
- **Method**: POST
- **URL**: `/api/empire-technologies/{id}/add_research_points/`
- **Description**: Add research points to progress the technology research
- **Body**:
```json
{
    "points": "25.50"
}
```
- **Response**: Updated empire technology object
- **Error Responses**:
  - 400 Bad Request: Invalid points value
  - 400 Bad Request: Research already complete

### Prerequisites Status
- **Method**: GET
- **URL**: `/api/empire-technologies/{id}/prerequisites_status/`
- **Description**: Get the research status of all prerequisites for this technology
- **Response**:
```json
[
    {
        "technology_id": 1,
        "name": "Basic Mining",
        "is_complete": true,
        "research_points": "100.00",
        "cost": "100.00"
    },
    {
        "technology_id": 2,
        "name": "Resource Management",
        "is_complete": false,
        "research_points": "50.00",
        "cost": "150.00"
    }
]
```

### Field Specifications

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| empire | integer | ID of the empire | Required |
| technology | integer | ID of the technology | Required |
| research_points | decimal | Current research progress | 0.00 |
| is_complete | boolean | Whether research is complete | false |