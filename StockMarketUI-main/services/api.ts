// services/api.ts

import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchStocks = async () => {
    const response = await axios.get(`${API_URL}/stocks/`);
    return response.data;
};

export const fetchDailyPrices = async () => {
    const response = await axios.get(`${API_URL}/daily-prices/`);
    return response.data;
};

export const fetchPriceChanges = async () => {
    const response = await axios.get(`${API_URL}/price-changes/`);
    return response.data;
};

export const fetchTopGainers = async () => {
    const response = await axios.get(`${API_URL}/top-gainers/`);
    return response.data;
};

export const fetchTopLosers = async () => {
    const response = await axios.get(`${API_URL}/top-losers/`);
    return response.data;
};

