import { create } from 'zustand';

export interface StarSystem {
    id: string;
    name: string;
    x: number;
    y: number;
    size: number;
    color: number;
    explored: boolean;
    planets: number;
    discoveryLevel: number;
}

export interface Planet {
    id: string;
    name: string;
    type: string;
    size: number;
    resources: {
        minerals: number;
        energy: number;
        organics: number;
    };
    colonized: boolean;
}

interface GameState {
    gameId: string | null;
    playerName: string | null;
    playerEmpire: string | null;
    turn: number;
    galaxySize: string;
    systems: StarSystem[];
    planets: Planet[];
    selectedSystem: StarSystem | null;
    selectedPlanet: Planet | null;
    resources: {
        minerals: number;
        energy: number;
        organics: number;
    };
    // Actions
    setGameId: (id: string) => void;
    setPlayerName: (name: string) => void;
    setPlayerEmpire: (empire: string) => void;
    setSystems: (systems: StarSystem[]) => void;
    setPlanets: (planets: Planet[]) => void;
    selectSystem: (system: StarSystem | null) => void;
    selectPlanet: (planet: Planet | null) => void;
    updateResources: (resources: { minerals: number; energy: number; organics: number }) => void;
    incrementTurn: () => void;
}

export const useGameState = create<GameState>((set) => ({
    gameId: null,
    playerName: null,
    playerEmpire: null,
    turn: 1,
    galaxySize: 'medium',
    systems: [],
    planets: [],
    selectedSystem: null,
    selectedPlanet: null,
    resources: {
        minerals: 0,
        energy: 0,
        organics: 0
    },

    setGameId: (id) => set({ gameId: id }),
    setPlayerName: (name) => set({ playerName: name }),
    setPlayerEmpire: (empire) => set({ playerEmpire: empire }),
    setSystems: (systems) => set({ systems }),
    setPlanets: (planets) => set({ planets }),
    selectSystem: (system) => set({ selectedSystem: system }),
    selectPlanet: (planet) => set({ selectedPlanet: planet }),
    updateResources: (resources) => set({ resources }),
    incrementTurn: () => set((state) => ({ turn: state.turn + 1 }))
})); 