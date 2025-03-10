import React from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

interface PlanetsTabProps {
    empireData: any;  // TODO: Add proper type
}

export default function PlanetsTab({ empireData }: PlanetsTabProps) {
    // TODO: Fetch planets data from API
    const planets = empireData?.controlled_planets || [];

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                Controlled Planets
            </Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell>Size</TableCell>
                            <TableCell>System</TableCell>
                            <TableCell>Resources</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {planets.map((planet: any) => (
                            <TableRow key={planet.id}>
                                <TableCell>{planet.name}</TableCell>
                                <TableCell>{planet.type}</TableCell>
                                <TableCell>{planet.size}</TableCell>
                                <TableCell>{planet.system?.name || '--'}</TableCell>
                                <TableCell>
                                    <Box>
                                        {planet.resources?.organic && <span>🌱 {planet.resources.organic}</span>}
                                        {planet.resources?.mineral && <span>⛰️ {planet.resources.mineral}</span>}
                                        {planet.resources?.energy && <span>⚡ {planet.resources.energy}</span>}
                                        {planet.resources?.exotics && <span>💎 {planet.resources.exotics}</span>}
                                    </Box>
                                </TableCell>
                            </TableRow>
                        ))}
                        {planets.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={5} align="center">
                                    No planets under control
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
} 