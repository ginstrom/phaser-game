/**
 * API utility for making requests to the backend
 */

// Define the base URL for the API
const API_BASE_URL = 'http://localhost:8000';

// Define types for API requests and responses
export interface NewGameRequest {
    player_name: string;
    difficulty?: 'easy' | 'normal' | 'hard';
    galaxy_size?: 'small' | 'medium' | 'large';
}

export interface NewGameResponse {
    game_id: string;
    message: string;
    initial_state: {
        player: {
            name: string;
            empire: string;
            resources: {
                organic: number;
                mineral: number;
                energy: number;
                exotics: number;
                credits: number;
                research: number;
            }
        };
        galaxy: {
            size: string;
            systems: number;
            explored: number;
        };
        turn: number;
    };
}

export interface EmpireResponse {
    id: string;
    name: string;
    is_player: boolean;
    color: string;
    credits: number;
    research_points: number;
    research_levels: {
        weapons: number;
        shields: number;
        propulsion: number;
        economics: number;
    };
    controlled_systems_count: number;
    controlled_planets_count: number;
    controlled_systems?: any[];  // TODO: Add proper type
    controlled_planets?: any[];  // TODO: Add proper type
}

/**
 * Create a new game
 * @param params The parameters for creating a new game
 * @returns A promise that resolves to the new game response
 */
export async function createNewGame(params: NewGameRequest): Promise<NewGameResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/new-game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create new game');
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating new game:', error);
        throw error;
    }
}

/**
 * Game state singleton to store the current game state
 */
class GameState {
    private static instance: GameState;
    private _gameId: string | null = null;
    private _playerName: string | null = null;
    private _playerEmpire: string | null = null;
    private _resources: any = null;
    private _galaxySize: string | null = null;
    private _galaxySystems: number | null = null;
    private _galaxyExplored: number | null = null;
    private _turn: number | null = null;

    private constructor() {}

    public static getInstance(): GameState {
        if (!GameState.instance) {
            GameState.instance = new GameState();
        }
        return GameState.instance;
    }

    public setFromNewGameResponse(response: NewGameResponse): void {
        console.log('Setting game state from response:', response);
        
        try {
            // Validate response structure
            if (!response) {
                throw new Error('Response is null or undefined');
            }
            
            if (!response.game_id) {
                throw new Error('Response missing game_id');
            }
            
            if (!response.initial_state) {
                throw new Error('Response missing initial_state');
            }
            
            if (!response.initial_state.player) {
                throw new Error('Response missing player data');
            }
            
            if (!response.initial_state.galaxy) {
                throw new Error('Response missing galaxy data');
            }
            
            // Set game state properties with fallbacks
            this._gameId = response.game_id;
            this._playerName = response.initial_state.player.name || 'Player';
            this._playerEmpire = response.initial_state.player.empire || 'Human Empire';
            
            // Ensure resources object exists and has all required properties
            if (response.initial_state.player.resources) {
                this._resources = {
                    organic: response.initial_state.player.resources.organic || 0,
                    mineral: response.initial_state.player.resources.mineral || 0,
                    energy: response.initial_state.player.resources.energy || 0,
                    exotics: response.initial_state.player.resources.exotics || 0,
                    credits: response.initial_state.player.resources.credits || 0,
                    research: response.initial_state.player.resources.research || 0
                };
            } else {
                // Create default resources if missing
                console.warn('Resources missing in response, using defaults');
                this._resources = {
                    organic: 0,
                    mineral: 500,
                    energy: 200,
                    exotics: 0,
                    credits: 1000,
                    research: 0
                };
            }
            
            this._galaxySize = response.initial_state.galaxy.size || 'medium';
            this._galaxySystems = response.initial_state.galaxy.systems || 0;
            this._galaxyExplored = response.initial_state.galaxy.explored || 0;
            this._turn = response.initial_state.turn || 1;
            
            console.log('Game state after update:', {
                gameId: this._gameId,
                playerName: this._playerName,
                playerEmpire: this._playerEmpire,
                resources: this._resources,
                galaxySize: this._galaxySize,
                galaxySystems: this._galaxySystems,
                galaxyExplored: this._galaxyExplored,
                turn: this._turn
            });
        } catch (error) {
            console.error('Error setting game state from response:', error);
            // Reset game state to prevent partial initialization
            this.reset();
            throw error;
        }
    }

    public get gameId(): string | null {
        return this._gameId;
    }

    public get playerName(): string | null {
        return this._playerName;
    }

    public get playerEmpire(): string | null {
        return this._playerEmpire;
    }

    public get resources(): any {
        return this._resources;
    }

    public get galaxySize(): string | null {
        return this._galaxySize;
    }

    public get galaxySystems(): number | null {
        return this._galaxySystems;
    }

    public get galaxyExplored(): number | null {
        return this._galaxyExplored;
    }

    public get turn(): number | null {
        return this._turn;
    }

    public reset(): void {
        this._gameId = null;
        this._playerName = null;
        this._playerEmpire = null;
        this._resources = null;
        this._galaxySize = null;
        this._galaxySystems = null;
        this._galaxyExplored = null;
        this._turn = null;
    }
}

// Create a singleton instance
const gameState = GameState.getInstance();

export async function fetchEmpireDetails(gameId: string): Promise<EmpireResponse> {
    const response = await fetch(`/api/games/${gameId}/empires`);
    if (!response.ok) {
        throw new Error('Failed to fetch empire details');
    }
    const empires = await response.json();
    // Return the player's empire
    return empires.find((empire: EmpireResponse) => empire.is_player);
}

export async function updateEmpireResearch(
    gameId: string,
    empireId: string,
    researchArea: string,
    level: number
): Promise<EmpireResponse> {
    const response = await fetch(`/api/games/${gameId}/empires/${empireId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            research_levels: {
                [researchArea]: level
            }
        })
    });
    if (!response.ok) {
        throw new Error('Failed to update research level');
    }
    return response.json();
}

const api = {
    createNewGame,
    GameState: gameState,
    fetchEmpireDetails,
    updateEmpireResearch
};

export default api;
