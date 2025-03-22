# UI Layout Documentation

## Scene Structure

### Startup Scene
The main menu scene that serves as the entry point to the game.

#### Layout
- **Title**: "SPACE CONQUEST"
  - Position: Centered, y=30% of screen height
  - Style: 48px monospace, green (#00ff00) with glow effect
- **Menu Items**: Vertically stacked, centered
  - "NEW GAME": y=50% of screen height
  - "LOAD GAME": y=60% of screen height
  - Style: 32px monospace, blue (#4444ff)
  - Interactive hover effects (scale and color)

### New Game Scene
Form interface for creating a new game.

#### Layout
- **Title**: "New Game"
  - Position: Centered, y=50px
- **Form Fields**: Left-aligned at x=centerX-200
  - Empire Name: y=150px
  - Computer Count: y=250px
  - Galaxy Size: y=350px
- **Buttons**: Centered horizontally, y=500px
  - Cancel: x=centerX-100
  - Start: x=centerX+100

### Load Game Scene
Displays saved games in a table format.

#### Layout
- **Title**: "Load Game"
  - Position: Centered, y=50px
  - Style: 36px monospace, green (#00ff00)
- **Games Table**: Centered
  - Starts at y=150px
  - Columns: ID, Created, Modified, Actions
- **Back Button**: Bottom left (x=100, y=height-50)

### Galaxy Scene
Displays the game galaxy with a grid of star systems.

#### Layout
- **Top Bar**: Height=60px
  - Turn Counter: Top right, 20px padding
- **Galaxy Grid**: 
  - Padding: 50px from edges
  - Grid Size: 50x50
  - Adjusts for top/bottom bars
- **Bottom Bar**: Height=90px (50px + 2*20px padding)
  - Exit: Bottom left
  - Empire: Second from right
  - End Turn: Bottom right
  - 20px padding from edges

### Empire Scene
Management interface for empire resources and colonies.

#### Layout
- **Top Navigation**: Tabs positioned at y=50
  - Colonies tab (x=125, width=150)
  - Resources tab (x=285, width=150)
- **Content Area**: Starts at y=100
- **Bottom Navigation**: 
  - Galaxy button (bottom-right, 20px padding)

#### Colonies Tab
```
| Column      | Width | Content                                    |
|------------|-------|-------------------------------------------|
| Orbit      | 80px  | Orbital position number                    |
| Type       | 100px | "planet" or "asteroid-belt"               |
| Minerals   | 120px | Production rate (Storage capacity)         |
| Organic    | 120px | Production rate (Storage capacity)         |
| Radioactive| 120px | Production rate (Storage capacity)         |
| Exotic     | 120px | Production rate (Storage capacity)         |
```

Table Properties:
- Cell Height: 40px
- Header Height: 48px
- Background Color: 0x111111
- Header Background: 0x222222
- Text Color: #FFFFFF
- Header Text Color: #00FF00

#### Resources Tab
```
| Column   | Width | Content                |
|----------|-------|------------------------|
| Resource | 150px | Resource type name     |
| Storage  | 200px | Current storage amount |
| Capacity | 200px | Maximum capacity       |
```

Visual Elements:
- Progress bars between Storage and Capacity columns
  - Width: 200px
  - Height: 20px
  - Background: 0x333333
  - Fill Color: 0x00FF00
  - Shows percentage of capacity used

Table Properties:
- Same styling as Colonies table
- Centered in view
- Starts at y=150

## Layout Guidelines

### Spacing
- Standard padding: 20px
- Button spacing: 10px
- Table cell padding: 10px horizontal

### Positioning
- Content centered horizontally in view
- Navigation elements aligned to edges
- Tables start 150px from top of content area

### Responsiveness
- Tables scale with content
- Buttons maintain fixed size
- Content container adjusts to scene dimensions 