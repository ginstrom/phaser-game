/**
 * Utility for loading and using enums from the enums.json file
 */

// Import the enums directly
import enumsData from './enums.json';

// Define the structure of the enums.json file
export interface EnumsConfig {
  PlanetType: string[];
  GalaxySize: string[];
  Difficulty: string[];
  [key: string]: string[]; // Allow for additional enum types
}

// Define the enum types
export type PlanetType = string;
export type GalaxySize = string;
export type Difficulty = string;

// Cast the imported data to the EnumsConfig type
const enums: EnumsConfig = enumsData as EnumsConfig;

/**
 * Load the enums from the enums.json file
 * @returns A promise that resolves to the enums object
 */
export async function loadEnums(): Promise<EnumsConfig> {
  return enums;
}

/**
 * Get the options for a select field from an enum type
 * @param enumType The enum type to get options for
 * @param enums The enums object
 * @returns An array of select options
 */
export function getSelectOptions(enumType: keyof EnumsConfig, enums: EnumsConfig) {
  return enums[enumType].map(value => ({
    value,
    label: value.charAt(0).toUpperCase() + value.slice(1).replace(/_/g, ' ')
  }));
}

/**
 * Get the default value for an enum type
 * @param enumType The enum type to get the default value for
 * @param enums The enums object
 * @returns The default value for the enum type
 */
export function getDefaultValue(enumType: keyof EnumsConfig, enums: EnumsConfig): string {
  // Default values for each enum type
  const defaults: Record<string, string> = {
    PlanetType: 'terrestrial',
    GalaxySize: 'medium',
    Difficulty: 'normal'
  };
  
  // Return the default value if it exists in the enum values
  const defaultValue = defaults[enumType];
  if (defaultValue && enums[enumType].includes(defaultValue)) {
    return defaultValue;
  }
  
  // Otherwise return the first value
  return enums[enumType][0];
}
