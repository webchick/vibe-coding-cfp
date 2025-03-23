import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Checkbox,
  FormControlLabel,
  Box,
  Chip,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import axios from 'axios';

interface CFP {
  id: number;
  title: string;
  description: string;
  event_name: string;
  event_date: string;
  closing_date: string;
  location: string;
  target_audience: string;
  event_type: string;
  event_url: string;
  cfp_url: string;
  source: string;
}

const CFPList: React.FC = () => {
  const [selectedCFPs, setSelectedCFPs] = useState<number[]>([]);
  const [filters, setFilters] = useState({
    location: '',
    target_audience: '',
    event_type: '',
    closing_date: null as Date | null,
  });

  const { data: cfps, isLoading } = useQuery({
    queryKey: ['cfps', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.location) params.append('location', filters.location);
      if (filters.target_audience) params.append('target_audience', filters.target_audience);
      if (filters.event_type) params.append('event_type', filters.event_type);
      if (filters.closing_date) {
        params.append('closing_date', filters.closing_date.toISOString());
      }

      const response = await axios.get(`/api/cfps?${params.toString()}`);
      return response.data;
    },
  });

  const handleCFPSelect = (cfpId: number) => {
    setSelectedCFPs(prev =>
      prev.includes(cfpId)
        ? prev.filter(id => id !== cfpId)
        : [...prev, cfpId]
    );
  };

  const handleSendNotification = async () => {
    try {
      await axios.post('/api/notify', {
        cfp_ids: selectedCFPs,
      });
      setSelectedCFPs([]);
    } catch (error) {
      console.error('Error sending notification:', error);
    }
  };

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Filter CFPs
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Location"
              value={filters.location}
              onChange={(e) => setFilters(prev => ({ ...prev, location: e.target.value }))}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Target Audience"
              value={filters.target_audience}
              onChange={(e) => setFilters(prev => ({ ...prev, target_audience: e.target.value }))}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Event Type"
              value={filters.event_type}
              onChange={(e) => setFilters(prev => ({ ...prev, event_type: e.target.value }))}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <DatePicker
              label="Closing Date"
              value={filters.closing_date}
              onChange={(date) => setFilters(prev => ({ ...prev, closing_date: date }))}
              slotProps={{ textField: { fullWidth: true } }}
            />
          </Grid>
        </Grid>
      </Paper>

      <Grid container spacing={3}>
        {cfps?.map((cfp: CFP) => (
          <Grid item xs={12} key={cfp.id}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Typography variant="h6">{cfp.title}</Typography>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={selectedCFPs.includes(cfp.id)}
                        onChange={() => handleCFPSelect(cfp.id)}
                      />
                    }
                    label="Select"
                  />
                </Box>
                <Typography color="textSecondary" gutterBottom>
                  {cfp.event_name}
                </Typography>
                <Typography variant="body2" paragraph>
                  {cfp.description}
                </Typography>
                <Box display="flex" gap={1} flexWrap="wrap" mb={2}>
                  <Chip label={`Event: ${format(new Date(cfp.event_date), 'PPP')}`} />
                  <Chip label={`Closing: ${format(new Date(cfp.closing_date), 'PPP')}`} />
                  <Chip label={cfp.location} />
                  <Chip label={cfp.target_audience} />
                  <Chip label={cfp.event_type} />
                </Box>
                <Box display="flex" gap={2}>
                  <Button
                    variant="outlined"
                    href={cfp.event_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Event Details
                  </Button>
                  <Button
                    variant="outlined"
                    href={cfp.cfp_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Submit Proposal
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {selectedCFPs.length > 0 && (
        <Box sx={{ position: 'fixed', bottom: 16, right: 16 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSendNotification}
            startIcon={<span>📢</span>}
          >
            Send Notification ({selectedCFPs.length})
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default CFPList; 