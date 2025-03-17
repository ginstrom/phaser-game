import 'phaser';
import { GameConfig } from './config/GameConfig';

window.addEventListener('load', () => {
    new Phaser.Game(GameConfig);
}); 