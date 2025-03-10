import React from 'react';
import { Box, Typography, Paper, Grid, LinearProgress } from '@mui/material';

interface ResearchTabProps {
    empireData: any;  // TODO: Add proper type
}

export default function ResearchTab({ empireData }: ResearchTabProps) {
    const researchAreas = [
        { name: 'Weapons', key: 'weapons' },
        { name: 'Shields', key: 'shields' },
        { name: 'Propulsion', key: 'propulsion' },
        { name: 'Economics', key: 'economics' }
    ];

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                Research Progress
            </Typography>
            <Grid container spacing={3}>
                {researchAreas.map(area => (
                    <Grid item xs={12} md={6} key={area.key}>
                        <Paper sx={{ p: 2 }}>
                            <Typography variant="subtitle1" gutterBottom>
                                {area.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" gutterBottom>
                                Level {empireData?.research_levels?.[area.key] || 0}
                            </Typography>
                            <LinearProgress 
                                variant="determinate" 
                                value={(empireData?.research_levels?.[area.key] || 0) * 10}
                                sx={{ height: 10, borderRadius: 5 }}
                            />
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
} 