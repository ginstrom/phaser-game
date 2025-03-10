import React, { useEffect, useRef } from 'react';
import { Box } from '@mui/material';
import Phaser from 'phaser';
import GalaxyScene from '../scenes/GalaxyScene';
import SystemScene from '../scenes/SystemScene';
import PlanetScene from '../scenes/PlanetScene';
import StartupScene from '../scenes/StartupScene';

const config: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    width: window.innerWidth,
    height: window.innerHeight,
    backgroundColor: '#000000',
    parent: 'game-container',
    scene: [StartupScene, GalaxyScene, SystemScene, PlanetScene],
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { x: 0, y: 0 },
            debug: false
        }
    }
};

export default function GameContainer() {
    const gameRef = useRef<Phaser.Game | null>(null);

    useEffect(() => {
        // Initialize Phaser game
        if (!gameRef.current) {
            gameRef.current = new Phaser.Game(config);
        }

        // Cleanup on unmount
        return () => {
            if (gameRef.current) {
                gameRef.current.destroy(true);
                gameRef.current = null;
            }
        };
    }, []);

    return (
        <Box
            id="game-container"
            sx={{
                width: '100vw',
                height: '100vh',
                backgroundColor: '#000',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
            }}
        />
    );
} 