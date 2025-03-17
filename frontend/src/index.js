import 'phaser';

class MainScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MainScene' });
    }

    create() {
        this.add.text(400, 300, 'Hello Space Conquest!', {
            color: '#ffffff',
            fontSize: '32px'
        }).setOrigin(0.5);
    }
}

const config = {
    type: Phaser.AUTO,
    parent: 'game',
    width: 1024,
    height: 768,
    scene: MainScene,
    backgroundColor: '#000000'
};

// Initialize the game only if we're on the main route
if (window.location.pathname === '/' || window.location.pathname === '/game') {
    const game = new Phaser.Game(config);
} else {
    // For non-game routes, show a message or redirect
    document.getElementById('game').innerHTML = 'Page Not Found';
    window.location.href = '/';
} 