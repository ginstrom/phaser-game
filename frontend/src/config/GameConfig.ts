import Phaser from 'phaser';
import { StartupScene } from '../scenes/StartupScene';

export const GameConfig: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    width: 1024,
    height: 768,
    backgroundColor: '#000000',
    parent: 'game',
    scene: [StartupScene],
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { x: 0, y: 0 },
            debug: false
        }
    }
}; 