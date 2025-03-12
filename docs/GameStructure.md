# Game Structure

This document outlines the main components and architecture of our 4X Space Empire game.

## Architecture Overview

The game follows a modern three-tier architecture with a Phaser.js frontend, FastAPI backend, and PostgreSQL database.

```
┌─────────────────────────────────────────────────────────────┐
│                      Game Frontend                          │
│                                                            │
│    ┌─────────────────┐     ┌─────────────────────┐        │
│    │  Game Instance  │     │   UI Components     │        │
│    │   (Phaser.js)   │     │  - Custom Buttons   │        │
│    └────────┬────────┘     │  - Resource Display │        │
│             │              │  - Modal Windows     │        │
│    ┌────────┴────────┐     │  - Context Menus    │        │
│    │  Scene Manager  │     │  - Tooltips         │        │
│    └────────┬────────┘     └─────────────────────┘        │
│             │                                             │
│    ┌────────┴────────┐     ┌─────────────────────┐       │
│    │     Scenes      │     │    Game Systems     │       │
│    │  - Startup      │     │  - Empire Manager   │       │
│    │  - Main         │     │  - Resource System  │       │
│    │  - Galaxy       │     │  - Fleet Manager    │       │
│    │  - System       │     │  - Tech Tree        │       │
│    │  - Planet       │     │  - Map Generator    │       │
│    │  - Combat       │     └─────────────────────┘       │
│    └────────┬────────┘                                   │
└─────────────┼────────────────────────────────────────────┘
              │
              │ HTTP/REST
              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Game Backend                           │
│                                                            │
│    ┌─────────────────┐     ┌─────────────────────┐        │
│    │   FastAPI App   │     │   Game Services     │        │
│    │  - CORS         │     │  - Game State       │        │
│    │  - Middleware   │     │  - Player Actions   │        │
│    └────────┬────────┘     │  - Combat System    │        │
│             │              └─────────────────────┘        │
│    ┌────────┴────────┐     ┌─────────────────────┐       │
│    │     Routes      │     │     Repository      │       │
│    │  - New Game     │     │  - Game Data        │       │
│    │  - Load Game    │     │  - Player Data      │       │
│    │  - Settings     │     │  - Galaxy Data      │       │
│    │  - Game State   │     │  - System Data      │       │
│    └────────┬────────┘     └────────┬────────────┘       │
└─────────────┼────────────────────────┼────────────────────┘
              │                         │
              │         SQLAlchemy      │
              ▼                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     PostgreSQL Database                      │
│                                                            │
│    ┌─────────────────┐     ┌─────────────────────┐        │
│    │   Game State    │     │    Game Entities    │        │
│    │  - Sessions     │     │  - Players          │        │
│    │  - Settings     │     │  - Empires          │        │
│    └─────────────────┘     │  - Galaxies         │        │
│                            │  - Star Systems      │        │
│    ┌─────────────────┐     │  - Planets          │        │
│    │   Resources     │     │  - Fleets           │        │
│    │  - Player       │     └─────────────────────┘        │
│    │  - Planet       │                                    │
│    └─────────────────┘                                    │
└────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Frontend (Phaser.js)**
   - Game engine for rendering and scene management
   - Custom UI components for game interface
   - State management for local game state
   - Asset pipeline for resource loading
   - WebSocket client for real-time updates (planned)

2. **Backend (FastAPI)**
   - RESTful API endpoints for game operations
   - Game state management and persistence
   - Player authentication and session handling
   - Game logic processing
   - WebSocket server for real-time updates (planned)

3. **Database (PostgreSQL)**
   - Persistent storage for game state
   - Player profiles and progress
   - Galaxy and star system data
   - Resource and technology tracking
   - Empire and diplomatic relations

### Data Flow

1. User interacts with the Phaser.js frontend
2. Frontend processes local game state changes
3. API requests are sent to the FastAPI backend
4. Backend validates and processes game logic
5. Database updates are performed via SQLAlchemy
6. Updated game state is returned to frontend
7. Frontend renders the updated game state

## Scene Details

### Startup Scene
- Initial loading and game setup
- Asset preloading
- Configuration initialization

### Main Scene
- Main menu and game settings
- Options for:
  - New Game
  - Load Game
  - Settings
  - Exit

### Galaxy Scene
- Strategic galaxy-level view
- Overview of multiple star systems
- Empire territory management
- Interstellar fleet movement
- Resource overview
- Empire-wide management

### System Scene
- Detailed view of individual star systems
- Shows all celestial bodies (planets, moons, etc.)
- System-level fleet management
- Resource distribution
- Local infrastructure

### Planet Scene
- Individual planet management
- Colony development
- Resource production
- Population management
- Building and improvements
- Local defense systems

### Combat Scene (Coming Soon)
- Space battle interface
- Fleet tactical management
- Real-time combat resolution
- Battle statistics and outcomes

## Core Game Systems

1. **Empire Management**
   - Resource tracking
   - Population control
   - Territory expansion
   - Diplomatic relations

2. **Resource System**
   - Resource gathering
   - Production chains
   - Trade routes
   - Storage management

3. **Fleet Management**
   - Ship construction
   - Fleet movement
   - Combat operations
   - Trade missions

4. **Technology**
   - Research progression
   - Tech tree advancement
   - Scientific discoveries
   - Technological advantages

5. **Map Generation**
   - Procedural galaxy creation
   - System layout
   - Resource distribution
   - Strategic points

## Navigation

Players can navigate between scenes through:
- Direct object interaction (clicking on systems, planets)
- UI navigation controls
- Shortcut keys (to be implemented)
- Context menus

## Future Expansions

Planned features and improvements:
- Enhanced combat system
- Advanced AI opponents
- Expanded tech tree
- Deeper diplomatic relations
- Additional victory conditions
- Multiplayer support
