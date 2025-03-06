import Phaser from 'phaser';

// Text styles for different UI elements
export const TextStyles = {
    // Titles
    title: {
        color: '#ffffff',
        fontSize: '48px',
        fontFamily: 'Arial',
        fontStyle: 'bold',
        stroke: '#000000',
        strokeThickness: 4,
        shadow: { offsetX: 2, offsetY: 2, color: '#000000', blur: 4, stroke: true, fill: true }
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Subtitles
    subtitle: {
        color: '#ffffff',
        fontSize: '32px',
        fontFamily: 'Arial',
        fontStyle: 'bold',
        stroke: '#000000',
        strokeThickness: 2
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Button text
    button: {
        color: '#ffffff',
        fontSize: '24px',
        fontFamily: 'Arial'
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Panel titles
    panelTitle: {
        color: '#ffffff',
        fontSize: '24px',
        fontFamily: 'Arial',
        fontStyle: 'bold'
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Normal text
    normal: {
        color: '#ffffff',
        fontSize: '18px',
        fontFamily: 'Arial'
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Small text
    small: {
        color: '#cccccc',
        fontSize: '14px',
        fontFamily: 'Arial'
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Resource text (for displaying resources)
    resource: {
        color: '#ffdd00',
        fontSize: '18px',
        fontFamily: 'Arial',
        fontStyle: 'bold'
    } as Phaser.Types.GameObjects.Text.TextStyle,

    // Alert text (for warnings or important messages)
    alert: {
        color: '#ff0000',
        fontSize: '18px',
        fontFamily: 'Arial',
        fontStyle: 'bold'
    } as Phaser.Types.GameObjects.Text.TextStyle
};

// Function to create a custom text style based on an existing style
export function createCustomStyle(
    baseStyle: Phaser.Types.GameObjects.Text.TextStyle,
    overrides: Partial<Phaser.Types.GameObjects.Text.TextStyle>
): Phaser.Types.GameObjects.Text.TextStyle {
    return { ...baseStyle, ...overrides };
}
