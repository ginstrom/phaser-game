import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';

interface ResourcesTabProps {
    empireData: any;  // TODO: Add proper type
}

export default function ResourcesTab({ empireData }: ResourcesTabProps) {
    const resources = [
        { name: 'Credits', key: 'credits', icon: '💰' },
        { name: 'Research Points', key: 'research_points', icon: '🔬' },
        { name: 'Organic', key: 'organic', icon: '🌱' },
        { name: 'Mineral', key: 'mineral', icon: '⛰️' },
        { name: 'Energy', key: 'energy', icon: '⚡' },
        { name: 'Exotics', key: 'exotics', icon: '💎' }
    ];

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                Empire Resources
            </Typography>
            <Grid container spacing={3}>
                {resources.map(resource => (
                    <Grid item xs={12} sm={6} md={4} key={resource.key}>
                        <Paper sx={{ p: 2 }}>
                            <Box display="flex" alignItems="center" gap={1}>
                                <Typography variant="h4">{resource.icon}</Typography>
                                <Box>
                                    <Typography variant="subtitle1">
                                        {resource.name}
                                    </Typography>
                                    <Typography variant="h6">
                                        {empireData?.[resource.key] || 0}
                                    </Typography>
                                </Box>
                            </Box>
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
} 