// Types for enums
export interface GameEnums {
    PlanetType: string[];
    GalaxySize: string[];
    Difficulty: string[];
    ResearchArea: string[];
    PerkAttribute: string[];
}

// Types for game configuration
export interface GalaxyConfig {
    width: number;
    height: number;
    min_systems: number;
    max_systems: number;
}

export interface GameSettings {
    min_computer_empires: number;
    max_computer_empires: number;
    default_computer_empires: number;
    galaxy_sizes: Record<string, GalaxyConfig>;
}

export interface EmpirePerks {
    research_efficiency: number;
    combat_efficiency: number;
    economic_efficiency: number;
    diplomatic_influence: number;
}

export interface StartingResources {
    credits: number;
    research_points: number;
}

export interface ResearchLevels {
    weapons: number;
    shields: number;
    propulsion: number;
    economics: number;
}

export interface GameDefaults {
    perks: EmpirePerks;
    starting_resources: Record<string, StartingResources>;
    research_levels: ResearchLevels;
}

export interface EmpireArchetype {
    name: string;
    perks: EmpirePerks;
    color_range: string[];
}

export interface PerkPointAllocation {
    total_points: number;
    min_per_attribute: number;
    max_per_attribute: number;
}

export interface GameConfig {
    defaults: GameDefaults;
    empire_archetypes: EmpireArchetype[];
    perk_point_allocation: PerkPointAllocation;
    game_settings: GameSettings;
}

class ConfigLoader {
    private static instance: ConfigLoader;
    private _enums?: GameEnums;
    private _gameConfig?: GameConfig;

    private constructor() {
        // Private constructor for singleton
    }

    public static getInstance(): ConfigLoader {
        if (!ConfigLoader.instance) {
            ConfigLoader.instance = new ConfigLoader();
        }
        return ConfigLoader.instance;
    }

    public async loadConfigs(): Promise<void> {
        try {
            // Load enums
            const enumsResponse = await fetch('/config/enums.json');
            this._enums = await enumsResponse.json();

            // Load game config
            const configResponse = await fetch('/config/game_config.json');
            this._gameConfig = await configResponse.json();
        } catch (error) {
            console.error('Failed to load game configurations:', error);
            throw error;
        }
    }

    public get enums(): GameEnums {
        if (!this._enums) {
            throw new Error('Enums not loaded. Call loadConfigs() first.');
        }
        return this._enums;
    }

    public get gameConfig(): GameConfig {
        if (!this._gameConfig) {
            throw new Error('Game config not loaded. Call loadConfigs() first.');
        }
        return this._gameConfig;
    }

    public getEnum(enumName: keyof GameEnums): string[] {
        return this.enums[enumName];
    }

    public getConfigValue<T>(path: string[]): T {
        let value: any = this.gameConfig;
        for (const key of path) {
            value = value[key];
            if (value === undefined) {
                throw new Error(`Configuration path not found: ${path.join('.')}`);
            }
        }
        return value as T;
    }
}

// Create singleton instance
export const config = ConfigLoader.getInstance();

// Example usage:
// import { config } from './utils/config';
//
// async function initGame() {
//     await config.loadConfigs();
//
//     // Get enums
//     const planetTypes = config.getEnum('PlanetType');
//     const difficulties = config.getEnum('Difficulty');
//
//     // Get configuration
//     const defaultPerks = config.getConfigValue<EmpirePerks>(['defaults', 'perks']);
//     const startingResources = config.getConfigValue<Record<string, StartingResources>>(['defaults', 'starting_resources']);
//     const militantArchetype = config.getConfigValue<EmpireArchetype[]>(['empire_archetypes'])[0];
// } 