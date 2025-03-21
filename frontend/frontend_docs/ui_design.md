# Space Conquest UI Design System

## Design Philosophy
Our UI design follows a dark sci-fi theme that emphasizes:
- Minimalism and clarity
- Futuristic aesthetics
- High contrast for readability
- Consistent visual hierarchy
- Responsive feedback

# Best Practices for UI in Phaser Games

 - Component-Based Approach: Create reusable UI components like we did with buttons and tables.
 - Clean Separation: Keep UI code separate from game logic. This makes it easier to update the UI without affecting gameplay.
 - Consistent Styling: Create a style system that defines colors, fonts, and sizes. I see you already have this in your UI design documentation.
 - Responsive Design: Make UI components that can adapt to different screen sizes:
 - Responsive UI 

## For Button Components:

- Use the SciFiButton component for all interactive buttons in the game
- Follow these button style guidelines:
  - ButtonStyle.PRIMARY: Main actions (Start Game, End Turn)
  - ButtonStyle.SECONDARY: Navigation actions (Empire, Galaxy view)
  - ButtonStyle.DANGER: Destructive actions (Exit, Cancel)
- Position guidelines:
  - Main menu buttons: Centered vertically and horizontally
  - Navigation buttons: Bottom of screen
  - Action buttons: Bottom right corner
  - Cancel/Exit buttons: Bottom left corner

## For Tables:

- Use HTML tables for complex data when you need rich formatting, scrolling, and extensive data display.
- Use pure Phaser tables for simpler displays or when performance is critical.
- Consider the hybrid approach for the most flexibility, allowing you to mix HTML and Phaser elements.

## General UI Structure:

- Create a dedicated UI directory as I outlined to keep your components organized.
- Implement the ResponsiveUI helper for better adapting to different screen sizes.
- Follow the performance tips to ensure your UI remains smooth even with many elements.


## UI Directory Structure

frontend/
├── src/
│   ├── ui/               # UI component directory
│   │   ├── buttons/      # Button components
│   │   │   ├── SciFiButton.ts
│   │   │   └── IconButton.ts
│   │   ├── tables/       # Table components
│   │   │   ├── HtmlTable.ts
│   │   │   └── PhaserTable.ts
│   │   ├── panels/       # Panel components
│   │   │   ├── InfoPanel.ts
│   │   │   └── DialogPanel.ts
│   │   ├── forms/        # Form components
│   │   │   ├── TextInput.ts
│   │   │   └── RadioButton.ts
│   │   └── common/       # Common UI utilities
│   │       ├── Colors.ts
│   │       ├── Styles.ts
│   │       └── Animations.ts
│   ├── scenes/           # Game scenes
│   ├── entities/         # Game objects
│   ├── config/           # Game configuration
│   └── utils/            # Utility functions
└── tests/                # Test files

## Color Palette

### Primary Colors
```
Background: #000000 (Deep Space Black)
Text: #FFFFFF (Pure White)
Accent: #00FF00 (Terminal Green)
```

### Secondary Colors
```
Highlight: #4444FF (Deep Blue)
Hover: #8888FF (Light Blue)
Warning: #FF4444 (Alert Red)
Success: #44FF44 (Success Green)
```

### UI Element Colors
```
Border: #333333 (Dark Gray)
Panel Background: #111111 (Near Black)
Disabled: #666666 (Medium Gray)
```

## Typography

### Font Families
1. **Primary Font**: Monospace
   - Used for: All text elements
   - Rationale: Maintains sci-fi terminal aesthetic

### Font Sizes
```
Title: 48px
Subtitle: 32px
Menu Items: 24px
Body Text: 16px
Small Text: 14px
```

### Text Styles
1. **Title Text**
   ```typescript
   {
       fontFamily: 'monospace',
       fontSize: '48px',
       color: '#00ff00',
       align: 'center',
       stroke: '#003300',
       strokeThickness: 6
   }
   ```

2. **Menu Items**
   ```typescript
   {
       fontFamily: 'monospace',
       fontSize: '32px',
       color: '#4444ff',
       align: 'center',
       backgroundColor: '#000000',
       padding: { x: 20, y: 10 }
   }
   ```

## Interactive Elements

### Buttons
1. **Standard Button**
   - Background: Transparent
   - Border: #333333
   - Text Color: #4444ff
   - Hover: Scale 1.1x, color #8888ff
   - Click: Scale 0.9x momentarily

2. **Primary Action Button**
   - Background: #4444ff
   - Text Color: #FFFFFF
   - Hover: Background #8888ff
   - Disabled: Background #666666

### Menu Items
- Default State: Blue text (#4444ff)
- Hover State: Lighter blue (#8888ff), scale up 1.1x
- Selected State: Green text (#00ff00)
- Transition: 100ms ease-in-out

## Animations

### Text Effects
1. **Title Glow**
   ```typescript
   this.tweens.add({
       targets: title,
       alpha: { from: 0.7, to: 1 },
       duration: 1500,
       ease: 'Sine.InOut',
       yoyo: true,
       repeat: -1
   });
   ```

2. **Button Hover**
   ```typescript
   this.tweens.add({
       targets: button,
       scaleX: 1.1,
       scaleY: 1.1,
       duration: 100
   });
   ```

### Transitions
- Scene Transitions: Fade black, 500ms
- Menu Transitions: Slide, 300ms
- Alert Popups: Scale up from center, 200ms

## Layout Guidelines

### Screen Composition
- Game canvas: 1024x768 pixels
- Centered horizontally and vertically
- Maintain 16:9 aspect ratio
- Black letterboxing when needed

### Menu Layout
- Vertical spacing: 32px between items
- Horizontal margins: 64px minimum
- Title position: 30% from top
- Menu items: Start at 60% from top

### HUD Elements
- Top left: Player status
- Top right: Resource counters
- Bottom left: Mini-map
- Bottom right: Action buttons

## Responsive Design

### Breakpoints
```typescript
const breakpoints = {
    small: 768,
    medium: 1024,
    large: 1440
};
```

### Scaling Rules
1. **Text**
   - Minimum size: 14px
   - Scale factor: 1.2 per breakpoint

2. **UI Elements**
   - Maintain relative positioning
   - Scale proportionally with screen size
   - Minimum touch target: 44x44 pixels

## Implementation Examples

### Creating a Standard Button
```typescript
export class SciFiButton extends Phaser.GameObjects.Container {
    constructor(scene: Phaser.Scene, x: number, y: number, text: string) {
        super(scene, x, y);

        const textObject = scene.add.text(0, 0, text, {
            fontFamily: 'monospace',
            fontSize: '32px',
            color: '#4444ff',
            align: 'center'
        });
        textObject.setOrigin(0.5);

        this.add(textObject);
        this.setSize(textObject.width + 40, textObject.height + 20);
        this.setInteractive({ useHandCursor: true });

        this.setupHoverEffects();
    }

    private setupHoverEffects() {
        this.on('pointerover', () => {
            this.scene.tweens.add({
                targets: this,
                scaleX: 1.1,
                scaleY: 1.1,
                duration: 100
            });
        });

        this.on('pointerout', () => {
            this.scene.tweens.add({
                targets: this,
                scaleX: 1,
                scaleY: 1,
                duration: 100
            });
        });
    }
}
```

## Accessibility Guidelines

### Color Contrast
- Minimum contrast ratio: 4.5:1
- Test all color combinations
- Provide alternative high-contrast theme

### Interactive Elements
- Clear focus states
- Minimum touch target size
- Keyboard navigation support

### Text Readability
- Minimum font size: 14px
- Clear font choice
- Adequate line spacing

## Asset Guidelines

### Icons
- Size: 32x32px base size
- Format: PNG with transparency
- Style: Monochrome with glow effects

### Backgrounds
- Resolution: 2048x1536px (2x base resolution)
- Format: JPEG for static, PNG for transparency
- Style: Dark, subtle patterns or starfields

## Quality Assurance

### Visual Testing
1. Check all breakpoints
2. Verify animations
3. Test color contrast
4. Validate layout consistency

### Performance Testing
1. Monitor frame rate during animations
2. Check memory usage
3. Verify asset loading times
4. Test input responsiveness 