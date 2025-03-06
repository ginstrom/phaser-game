import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';

interface StarSystem {
    id: number;
    name: string;
    x: number;
    y: number;
    size: number;
    color: number;
}

export default class GalaxyScene extends Phaser.Scene {
    private systems: StarSystem[] = [];
    private selectedSystem: StarSystem | null = null;
    private infoPanel: Panel | null = null;

    constructor() {
        super('GalaxyScene');
    }

    preload() {
        // Preload assets here
    }

    create() {
        const { width, height } = this.cameras.main;

        // Title
        this.add.text(
            width / 2,
            30,
            'Galaxy View',
            TextStyles.subtitle
        ).setOrigin(0.5);

        // Generate some random star systems
        this.generateStarSystems(15);

        // Create star systems
        this.systems.forEach(system => {
            const star = this.add.circle(system.x, system.y, system.size, system.color);
            star.setInteractive({ useHandCursor: true })
                .on('pointerover', () => this.onSystemHover(system))
                .on('pointerout', () => this.onSystemOut())
                .on('pointerdown', () => this.onSystemClick(system));
            
            // Add name label
            this.add.text(
                system.x,
                system.y + system.size + 10,
                system.name,
                TextStyles.small
            ).setOrigin(0.5);
        });

        // Back button
        new Button({
            scene: this,
            x: 100,
            y: height - 50,
            text: 'Back to Menu',
            textStyle: TextStyles.button,
            callback: () => this.backToMenu()
        });

        // Turn indicator
        this.add.text(
            width - 20,
            20,
            'Turn: 1',
            TextStyles.normal
        ).setOrigin(1, 0);
    }

    private generateStarSystems(count: number): void {
        const { width, height } = this.cameras.main;
        const padding = 100; // Padding from edges
        
        // Star colors
        const colors = [0xffff00, 0xff8800, 0xff0000, 0x8888ff, 0xffffff];
        
        // Generate systems
        for (let i = 0; i < count; i++) {
            const system: StarSystem = {
                id: i,
                name: `System ${i + 1}`,
                x: Phaser.Math.Between(padding, width - padding),
                y: Phaser.Math.Between(padding, height - padding),
                size: Phaser.Math.Between(3, 8),
                color: colors[Phaser.Math.Between(0, colors.length - 1)]
            };
            
            this.systems.push(system);
        }
    }

    private onSystemHover(system: StarSystem): void {
        // Show system name in a tooltip
        const tooltip = this.add.text(
            system.x,
            system.y - system.size - 20,
            system.name,
            TextStyles.normal
        ).setOrigin(0.5);
        
        // Store reference to remove on pointer out
        (this as any).tooltip = tooltip;
    }

    private onSystemOut(): void {
        // Remove tooltip
        if ((this as any).tooltip) {
            (this as any).tooltip.destroy();
            (this as any).tooltip = null;
        }
    }

    private onSystemClick(system: StarSystem): void {
        this.selectedSystem = system;
        
        // Remove existing info panel if any
        if (this.infoPanel) {
            this.infoPanel.destroy();
            this.infoPanel = null;
        }
        
        // Create info panel
        const { width, height } = this.cameras.main;
        this.infoPanel = new Panel({
            scene: this,
            x: width - 150,
            y: height / 2,
            width: 250,
            height: 300,
            title: system.name,
            draggable: true
        });
        
        // Add content to panel
        const viewButton = new Button({
            scene: this,
            x: 0,
            y: 50,
            text: 'View System',
            textStyle: TextStyles.button,
            callback: () => this.viewSystem(system)
        });
        
        this.infoPanel.addContent(viewButton);
        
        // Add some dummy system info
        const info = this.add.text(
            0,
            -50,
            'Status: Explored\nPlanets: 3\nResources: Medium\nThreat Level: Low',
            TextStyles.normal
        ).setOrigin(0.5, 0);
        
        this.infoPanel.addContent(info);
    }

    private viewSystem(system: StarSystem): void {
        console.log(`Viewing system ${system.name}`);
        this.scene.start('SystemScene', { systemId: system.id });
    }

    private backToMenu(): void {
        this.scene.start('StartupScene');
    }
}
