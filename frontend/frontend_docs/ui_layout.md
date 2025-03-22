# UI Layout Documentation

## Scene Structure

### Empire Scene
The Empire scene provides management of colonies and resources through a tabbed interface.

#### Layout
- **Top Navigation**: Tabs positioned at y=50
  - Colonies tab (x=125, width=150)
  - Resources tab (x=285, width=150)
- **Content Area**: Starts at y=100
- **Bottom Navigation**: 
  - Galaxy button (bottom-right, 20px padding)

#### Colonies Tab
Displays a table of all colonies (planets and asteroid belts) with the following columns:
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
Displays empire-wide resource management in a table format:
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

### Common UI Elements

#### SciFiButton
Standard button component used across scenes:
- Primary Style: Used for active tabs
- Secondary Style: Used for inactive tabs and navigation
- Text: Monospace font, centered
- Interactive hover effects

#### PhaserTable
Reusable table component with features:
- Sortable columns
- Customizable cell formatting
- Consistent styling across tables
- Header/content separation
- Scrollable content area

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