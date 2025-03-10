import React from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

interface SystemsTabProps {
    empireData: any;  // TODO: Add proper type
}

export default function SystemsTab({ empireData }: SystemsTabProps) {
    // TODO: Fetch systems data from API
    const systems = empireData?.controlled_systems || [];

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                Controlled Systems
            </Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Position</TableCell>
                            <TableCell>Planets</TableCell>
                            <TableCell>Resources</TableCell>
                            <TableCell>Status</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {systems.map((system: any) => (
                            <TableRow key={system.id}>
                                <TableCell>{system.name}</TableCell>
                                <TableCell>
                                    ({system.position?.x.toFixed(1)}, {system.position?.y.toFixed(1)})
                                </TableCell>
                                <TableCell>{system.planets?.length || 0}</TableCell>
                                <TableCell>
                                    {/* TODO: Add resource summary */}
                                    --
                                </TableCell>
                                <TableCell>
                                    {system.explored ? 'Explored' : 'Unexplored'}
                                </TableCell>
                            </TableRow>
                        ))}
                        {systems.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={5} align="center">
                                    No systems under control
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
} 