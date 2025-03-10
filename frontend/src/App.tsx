import React from 'react';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import GameContainer from './components/GameContainer';

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#90caf9'
        },
        secondary: {
            main: '#f48fb1'
        },
        background: {
            default: '#000000',
            paper: '#1a1a1a'
        }
    }
});

export default function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <GameContainer />
        </ThemeProvider>
    );
} 