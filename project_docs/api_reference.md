# Space Conquest Game API Reference

This document describes the REST API endpoints for the Space Conquest game.

## Base URLs

- Development: `http://localhost:8000`
- All game management endpoints are prefixed with `/api/play/`
- All celestial body endpoints are prefixed with `/api/`

## Authentication

*To be implemented*

## Common Response Formats

### Success Response
```json
{
    "data": {
        // Response data specific to the endpoint
    }
}
```

### Error Response
```json
{
    "error": "Error message describing what went wrong"
}
```

## Game Management

### Start New Game
- **URL**: `/api/play/games/start/`
- **Method**: `POST`
- **Description**: Creates a new game with specified parameters
- **Request Body**:
  ```json
  {
    "player_empire_name": "string",
    "computer_empire_count": "integer",
    "galaxy_size": "string (tiny|small|medium|large)"
  }
  ```
- **Galaxy Size Details**:
  - `tiny`: 2 star systems
  - `small`: 5 star systems
  - `medium`: 10 star systems
  - `large`: 15 star systems
- **Success Response** (201 Created):
  ```json
  {
    "id": "integer",
    "turn": 1,
    "empires": [
      {
        "id": "integer",
        "name": "string",
        "player": {
          "id": "integer",
          "player_type": "string"
        },
        "race": {
          "id": "integer",
          "name": "string"
        }
      }
    ],
    "systems": [
      {
        "id": "integer",
        "x": "integer",
        "y": "integer",
        "star": {
          "id": "integer",
          "star_type": "string"
        }
      }
    ]
  }
  ```
- **Error Responses**:
  - 400 Bad Request:
    ```json
    {
      "error": "Missing required field: field_name"
    }
    ```
    ```json
    {
      "error": "Invalid galaxy size: size_name"
    }
    ```

### List Games
- **URL**: `/api/play/games/`
- **Method**: `GET`
- **Description**: Returns a list of all games
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "turn": "integer",
      "empires": [],
      "systems": []
    }
  ]
  ```

### Get Game Details
- **URL**: `/api/play/games/{game_id}/`
- **Method**: `GET`
- **Description**: Returns details of a specific game
- **Success Response** (200 OK):
  ```json
  {
    "id": "integer",
    "turn": "integer",
    "empires": [],
    "systems": []
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Game not found"
  }
  ```

### End Turn
- **URL**: `/api/play/games/{game_id}/end-turn/`
- **Method**: `POST`
- **Description**: Ends the current turn and processes end-of-turn actions
- **Success Response** (200 OK):
  ```json
  {
    "status": "turn ended",
    "new_turn": "integer"
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Game not found"
  }
  ```

### Delete Game
- **URL**: `/api/play/games/{game_id}/`
- **Method**: `DELETE`
- **Description**: Deletes a game and all associated data
- **Response**: 204 No Content
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Game not found"
  }
  ```

## Empire Management

### List Empires
- **URL**: `/api/play/empires/`
- **Method**: `GET`
- **Description**: Returns a list of all empires
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "player": "integer",
      "race": "integer",
      "game": "integer",
      "planets": ["integer"],
      "asteroid_belts": ["integer"],
      "mineral_storage": "decimal",
      "organic_storage": "decimal",
      "radioactive_storage": "decimal",
      "exotic_storage": "decimal",
      "resource_capacities": {
        "mineral_capacity": "decimal",
        "organic_capacity": "decimal",
        "radioactive_capacity": "decimal",
        "exotic_capacity": "decimal"
      }
    }
  ]
  ```

### Create Empire
- **URL**: `/api/play/empires/`
- **Method**: `POST`
- **Description**: Creates a new empire
- **Request Body**:
  ```json
  {
    "name": "string",
    "player": "integer",
    "race": "integer",
    "game": "integer",
    "planets": [],
    "asteroid_belts": [],
    "mineral_storage": "decimal",
    "organic_storage": "decimal",
    "radioactive_storage": "decimal",
    "exotic_storage": "decimal"
  }
  ```
- **Success Response** (201 Created): Same format as list item
- **Error Response** (400 Bad Request):
  ```json
  {
    "error": "Invalid field: error_details"
  }
  ```

### Get Empire Details
- **URL**: `/api/play/empires/{empire_id}/`
- **Method**: `GET`
- **Description**: Returns details of a specific empire
- **Success Response** (200 OK): Same format as list item
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Empire not found"
  }
  ```

### Update Empire
- **URL**: `/api/play/empires/{empire_id}/`
- **Method**: `PUT/PATCH`
- **Description**: Updates empire details
- **Request Body**: Same format as create (PUT) or partial (PATCH)
- **Success Response** (200 OK): Same format as list item
- **Error Responses**:
  - 404 Not Found:
    ```json
    {
      "error": "Empire not found"
    }
    ```
  - 400 Bad Request:
    ```json
    {
      "error": "Invalid field: error_details"
    }
    ```

### Delete Empire
- **URL**: `/api/play/empires/{empire_id}/`
- **Method**: `DELETE`
- **Description**: Deletes an empire
- **Response**: 204 No Content
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Empire not found"
  }
  ```

## Player Management

### List Players
- **URL**: `/api/play/players/`
- **Method**: `GET`
- **Description**: Returns a list of all players
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "player_type": "string (human|computer)"
    }
  ]
  ```

### Create Player
- **URL**: `/api/play/players/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "player_type": "human"  // or "computer"
  }
  ```

### Get Player Details
- **URL**: `/api/play/players/{id}/`
- **Method**: `GET`
- **Success Response** (200 OK):
  ```json
  {
    "id": "integer",
    "player_type": "human"
  }
  ```

### Update Player
- **URL**: `/api/play/players/{id}/`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
    "player_type": "computer"
  }
  ```

### Delete Player
- **URL**: `/api/play/players/{id}/`
- **Method**: `DELETE`
- **Response**: 204 No Content

## Race Management

### List Races
- **URL**: `/api/play/races/`
- **Method**: `GET`
- **Description**: Returns a list of all races
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "name": "string"
    }
  ]
  ```

### Create Race
- **URL**: `/api/play/races/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "string"
  }
  ```

### Get Race Details
- **URL**: `/api/play/races/{id}/`
- **Method**: `GET`
- **Success Response** (200 OK):
  ```json
  {
    "id": "integer",
    "name": "string"
  }
  ```

### Update Race
- **URL**: `/api/play/races/{id}/`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
    "name": "string"
  }
  ```

### Delete Race
- **URL**: `/api/play/races/{id}/`
- **Method**: `DELETE`
- **Response**: 204 No Content

## Celestial Bodies

### Planet Resource

#### List Planets
- **URL**: `/api/planets/`
- **Method**: `GET`
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "mineral_production": "decimal",
      "organic_production": "decimal",
      "radioactive_production": "decimal",
      "exotic_production": "decimal",
      "mineral_storage_capacity": "decimal",
      "organic_storage_capacity": "decimal",
      "radioactive_storage_capacity": "decimal",
      "exotic_storage_capacity": "decimal",
      "orbit": "integer"
    }
  ]
  ```

#### Create Planet
- **URL**: `/api/planets/`
- **Method**: `POST`
- **Request Body**: Same format as list item
- **Success Response** (201 Created): Same format as list item
- **Error Response** (400 Bad Request):
  ```json
  {
    "error": "Invalid orbit: Must be between 1 and 5"
  }
  ```

#### Get Planet Details
- **URL**: `/api/planets/{id}/`
- **Method**: `GET`
- **Success Response** (200 OK): Same format as list item
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Planet not found"
  }
  ```

#### Update Planet
- **URL**: `/api/planets/{id}/`
- **Method**: `PUT/PATCH`
- **Request Body**: Same format as list item (PUT) or partial (PATCH)
- **Success Response** (200 OK): Same format as list item
- **Error Responses**:
  - 404 Not Found:
    ```json
    {
      "error": "Planet not found"
    }
    ```
  - 400 Bad Request:
    ```json
    {
      "error": "Invalid field: error_details"
    }
    ```

#### Delete Planet
- **URL**: `/api/planets/{id}/`
- **Method**: `DELETE`
- **Response**: 204 No Content
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Planet not found"
  }
  ```

### Star Resource

#### List Stars
- **URL**: `/api/stars/`
- **Method**: `GET`
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "star_type": "string"
    }
  ]
  ```

#### Create Star
- **URL**: `/api/stars/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "star_type": "string"  // blue, white, yellow, orange, brown
  }
  ```
- **Success Response** (201 Created): Same format as list item
- **Error Response** (400 Bad Request):
  ```json
  {
    "error": "Invalid star_type: Must be one of [blue, white, yellow, orange, brown]"
  }
  ```

#### Get Star Details
- **URL**: `/api/stars/{id}/`
- **Method**: `GET`
- **Success Response** (200 OK): Same format as list item
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Star not found"
  }
  ```

#### Update Star
- **URL**: `/api/stars/{id}/`
- **Method**: `PUT/PATCH`
- **Request Body**: Same format as create
- **Success Response** (200 OK): Same format as list item
- **Error Responses**:
  - 404 Not Found:
    ```json
    {
      "error": "Star not found"
    }
    ```
  - 400 Bad Request:
    ```json
    {
      "error": "Invalid star_type: Must be one of [blue, white, yellow, orange, brown]"
    }
    ```

#### Delete Star
- **URL**: `/api/stars/{id}/`
- **Method**: `DELETE`
- **Response**: 204 No Content
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "Star not found"
  }
  ```

### Asteroid Belt Resource

#### List Asteroid Belts
- **URL**: `/api/asteroid-belts/`
- **Method**: `GET`
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "mineral_production": "decimal",
      "organic_production": "decimal",
      "radioactive_production": "decimal",
      "exotic_production": "decimal",
      "orbit": "integer"
    }
  ]
  ```

#### Create Asteroid Belt
- **URL**: `/api/asteroid-belts/`
- **Method**: `POST`
- **Request Body**: Same format as list item

#### Get Asteroid Belt Details
- **URL**: `/api/asteroid-belts/{id}/`
- **Method**: `GET`
- **Success Response** (200 OK): Same format as list item

#### Update Asteroid Belt
- **URL**: `/api/asteroid-belts/{id}/`
- **Method**: `PUT/PATCH`
- **Request Body**: Same format as list item (PUT) or partial (PATCH)

#### Delete Asteroid Belt
- **URL**: `/api/asteroid-belts/{id}/`
- **Method**: `DELETE`
- **Response**: 204 No Content

### System Resource

#### List Systems
- **URL**: `/api/systems/`
- **Method**: `GET`
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": "integer",
      "x": "integer",
      "y": "integer",
      "star": {
        "id": "integer",
        "star_type": "string"
      },
      "planets": [
        {
          "id": "integer",
          "mineral_production": "decimal",
          "organic_production": "decimal",
          "radioactive_production": "decimal",
          "exotic_production": "decimal",
          "mineral_storage_capacity": "decimal",
          "organic_storage_capacity": "decimal",
          "radioactive_storage_capacity": "decimal",
          "exotic_storage_capacity": "decimal",
          "orbit": "integer"
        }
      ],
      "asteroid_belts": [
        {
          "id": "integer",
          "mineral_production": "decimal",
          "organic_production": "decimal",
          "radioactive_production": "decimal",
          "exotic_production": "decimal",
          "orbit": "integer"
        }
      ]
    }
  ]
  ```

#### Create System
- **URL**: `/api/systems/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "x": "integer",
    "y": "integer",
    "star": {
      "star_type": "string"  // blue, white, yellow, orange, brown
    }
  }
  ```
- **Success Response** (201 Created): Same format as list item
- **Error Response** (400 Bad Request):
  ```json
  {
    "error": "A system with these coordinates already exists in this game"
  }
  ```

#### Get System Details
- **URL**: `/api/systems/{id}/`
- **Method**: `GET`
- **Success Response** (200 OK): Same format as list item
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "System not found"
  }
  ```

#### Update System
- **URL**: `/api/systems/{id}/`
- **Method**: `PUT`
- **Request Body**: Same format as create
- **Success Response** (200 OK): Same format as list item
- **Error Responses**:
  - 404 Not Found:
    ```json
    {
      "error": "System not found"
    }
    ```
  - 400 Bad Request:
    ```json
    {
      "error": "A system with these coordinates already exists in this game"
    }
    ```

#### Delete System
- **URL**: `/api/systems/{id}/`
- **Method**: `DELETE`
- **Response**: 204 No Content
- **Error Response** (404 Not Found):
  ```json
  {
    "error": "System not found"
  }
  ```

#### Add Planet to System
- **URL**: `/api/systems/{id}/add_planet/`
- **Method**: `POST`
- **Request Body**: Same format as Planet create
- **Success Response** (201 Created): Same format as Planet list item
- **Error Responses**:
  - 404 Not Found:
    ```json
    {
      "error": "System not found"
    }
    ```
  - 400 Bad Request:
    ```json
    {
      "error": "System cannot have more than 5 occupied orbits"
    }
    ```
    ```json
    {
      "error": "Orbit 3 is already occupied by another celestial body"
    }
    ```

#### Add Asteroid Belt to System
- **URL**: `/api/systems/{id}/add_asteroid_belt/`
- **Method**: `POST`
- **Request Body**: Same format as Asteroid Belt create
- **Success Response** (201 Created): Same format as Asteroid Belt list item
- **Error Responses**:
  - 404 Not Found:
    ```json
    {
      "error": "System not found"
    }
    ```
  - 400 Bad Request:
    ```json
    {
      "error": "System cannot have more than 5 occupied orbits"
    }
    ```
    ```json
    {
      "error": "Orbit 3 is already occupied by another celestial body"
    }
    ```

## Field Specifications

### Resource Values
All resource values (production and storage) are decimal numbers with 2 decimal places precision.

### Default Values
- Planet/Asteroid Belt production: 50.00
- Planet storage capacity: 100.00
- Empire resource storage: 0
- Game turn: 1
- Player type: "human"
- Orbit: 1

### Constraints
- Each system must have unique x,y coordinates within a game
- Each system has exactly one star
- Each system can have up to MAX_ORBITS (5) planets and/or asteroid belts
- Each orbit (1 to MAX_ORBITS) can be occupied by either a planet or an asteroid belt, but not both
- A game must have at least 2 empires
- A game must have at least 2 star systems
- Race names must be unique
- Star types must be one of: blue, white, yellow, orange, brown
- Orbit must be between 1 and 5 (inclusive)
- All resource values must have exactly 2 decimal places 