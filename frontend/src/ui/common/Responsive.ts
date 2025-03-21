// src/ui/common/Responsive.ts
import Phaser from 'phaser';

interface PositionableGameObject extends Phaser.GameObjects.GameObject {
    x?: number;
    y?: number;
}

export class ResponsiveUI {
    private scene: Phaser.Scene;
    private baseWidth: number;
    private baseHeight: number;
    
    constructor(scene: Phaser.Scene, baseWidth = 1024, baseHeight = 768) {
        this.scene = scene;
        this.baseWidth = baseWidth;
        this.baseHeight = baseHeight;
        
        // Listen for resize events
        this.scene.scale.on('resize', this.onResize, this);
    }
    
    private onResize(): void {
        // Adjust UI elements on resize
        // This would be called when the window is resized
        this.scene.events.emit('ui-resize', {
            scaleX: this.getScaleX(),
            scaleY: this.getScaleY(),
            width: this.scene.cameras.main.width,
            height: this.scene.cameras.main.height
        });
    }
    
    public getScaleX(): number {
        return this.scene.cameras.main.width / this.baseWidth;
    }
    
    public getScaleY(): number {
        return this.scene.cameras.main.height / this.baseHeight;
    }
    
    public scalePosition(x: number, y: number): { x: number, y: number } {
        return {
            x: x * this.getScaleX(),
            y: y * this.getScaleY()
        };
    }
    
    public calculateFontSize(baseSize: number): string {
        // Calculate a responsive font size based on screen dimensions
        const scaleFactor = Math.min(this.getScaleX(), this.getScaleY());
        const fontSize = Math.round(baseSize * scaleFactor);
        return `${fontSize}px`;
    }
    
    public positionToBottom(element: PositionableGameObject, offsetY = 20): void {
        // Position element to bottom of screen with offset
        if ('y' in element) {
            element.y = this.scene.cameras.main.height - offsetY;
        }
    }
    
    public positionToRight(element: PositionableGameObject, offsetX = 20): void {
        // Position element to right of screen with offset
        if ('x' in element) {
            element.x = this.scene.cameras.main.width - offsetX;
        }
    }
    
    public centerHorizontally(element: PositionableGameObject): void {
        // Center element horizontally
        if ('x' in element) {
            element.x = this.scene.cameras.main.centerX;
        }
    }
    
    public centerVertically(element: PositionableGameObject): void {
        // Center element vertically
        if ('y' in element) {
            element.y = this.scene.cameras.main.centerY;
        }
    }
    
    public destroy(): void {
        this.scene.scale.off('resize', this.onResize, this);
    }
}