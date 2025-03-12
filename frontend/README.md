# Space Empire 4X Game Frontend

A turn-based 4X space strategy game built with Phaser 3 and TypeScript, offering an immersive empire-building experience in space.

## Tech Stack

- **Game Engine**: Phaser 3
- **Language**: TypeScript 4.x
- **Build Tool**: Webpack 5
- **Testing**: Jest with React Testing Library
- **State Management**: Custom game state manager
- **UI Framework**: Custom UI components built with Phaser
- **Asset Loading**: Phaser Asset Pipeline
- **Development Server**: Webpack Dev Server

## Architecture Overview

```
┌─────────────────────┐
│    Game Instance    │
└─────────────┬───────┘
              │
┌─────────────┴───────┐
│    Scene Manager    │
└─────────────┬───────┘
              │
┌─────────────┴───────┐
│      Scenes         │
├─────────────────────┤
│ • MainMenu         │
│ • Galaxy           │
│ • Combat           │
│ • Colony           │
│ • Research         │
└─────────────────────┘
```

## Core Components

1. **Scene System**
   - MainMenuScene: Game entry point and settings
   - GalaxyScene: Main strategic view
   - CombatScene: Tactical battle interface
   - ColonyScene: Planet management
   - ResearchScene: Technology development

2. **Game Systems**
   - Empire Management
   - Resource Tracking
   - Combat Resolution
   - Tech Tree Progression
   - Map Generation

3. **UI Components**
   - Custom Button System
   - Resource Display
   - Modal Windows
   - Context Menus
   - Tooltips

## Asset Structure

```
assets/
├── sprites/     # Game entity sprites
├── ui/          # UI elements
├── maps/        # Galaxy templates
├── audio/       # Sound effects and music
└── config/      # Game configuration files
```

## Development Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Testing

Run tests using the project's test script:
```bash
./test.sh frontend
```

## Key Features

- Procedurally generated galaxies
- Dynamic combat system
- Advanced AI opponents
- Comprehensive tech tree
- Resource management
- Diplomatic relations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Targets

- 60 FPS on modern browsers
- < 100ms response time for game actions
- < 2s initial load time
- < 500KB initial bundle size 