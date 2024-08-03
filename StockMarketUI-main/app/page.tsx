"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from '../utils/axiosInstance';
import styled from 'styled-components';

// Define styles for the dashboard container
const DashboardContainer = styled.div`
  font-family: Arial, sans-serif;
  padding: 20px;
  background-color: #f0f4f8; /* Light background color for the dashboard */
`;

// Define styles for the title with bold font
const Title = styled.h1`
  color: #2c3e50; /* Dark color for the title */
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold; /* Bold font weight */
`;

// Define styles for section titles with bold font
const SectionTitle = styled.h2`
  color: #34495e; /* Darker color for section titles */
  border-bottom: 2px solid #2c3e50; /* Border color to match the text */
  padding-bottom: 5px;
  margin-bottom: 15px;
  font-weight: bold; /* Bold font weight */
`;

// Define styles for the table
const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  background-color: #ffffff; /* White background color for the table */
`;

// Define styles for table headers with color
const Th = styled.th`
  border: 1px solid #ddd; /* Light border color for table headers */
  padding: 12px;
  text-align: center;
  background-color: #3498db; /* Blue background color for table headers */
  color: #ffffff; /* White text color for headers */
`;

// Define styles for table cells with black text color
const Td = styled.td<{ isNegative?: boolean }>`
  border: 1px solid #ddd; /* Light border color for table cells */
  padding: 12px;
  text-align: center;
  color: ${(props) => (props.isNegative ? '#e74c3c' : '#000000')}; /* Red for negative values, black otherwise */
`;

// Define styles for table rows with alternating colors
const Tr = styled.tr`
  &:nth-child(even) {
    background-color: #f2f2f2; /* Light gray color for even rows */
  }
  &:hover {
    background-color: #ddd; /* Light gray color for hover effect */
  }
`;

// Define bold styles for specific rows
const BoldText = styled.span`
  font-weight: bold;
`;

const Dashboard = () => {
  const router = useRouter();
  const [symbolPerformance, setSymbolPerformance] = useState([]);
  const [topLosers, setTopLosers] = useState([]);
  const [topGainers, setTopGainers] = useState([]);

  useEffect(() => {
    // Check if the user is authenticated
    const isAuthenticated = localStorage.getItem('authenticated') === 'true';

    if (!isAuthenticated) {
      router.push('/login'); // Redirect to login page if not authenticated
      return; // Stop further execution
    }

    // Fetch data if authenticated
    const fetchSymbolPerformance = async () => {
      try {
        const response = await axios.get('/api/symbol_performance/');
        setSymbolPerformance(response.data);
      } catch (error) {
        console.error('Error fetching symbol performance data:', error);
      }
    };

    const fetchTopLosers = async () => {
      try {
        const response = await axios.get('/api/top_losers/');
        setTopLosers(response.data.reverse()); // Reverse the order of top losers
      } catch (error) {
        console.error('Error fetching top losers data:', error);
      }
    };

    const fetchTopGainers = async () => {
      try {
        const response = await axios.get('/api/top_gainers/');
        setTopGainers(response.data);
      } catch (error) {
        console.error('Error fetching top gainers data:', error);
      }
    };

    fetchSymbolPerformance();
    fetchTopLosers();
    fetchTopGainers();
  }, [router]);

  // Helper function to format numbers to two decimal places
  const formatPercentage = (value: number) => value.toFixed(2);

  return (
    <DashboardContainer>
      <Title>Live Stock Market Data Dashboard</Title>

      <SectionTitle>Stocks Performance</SectionTitle>
      <Table>
        <thead>
          <tr>
            <Th>Company Code</Th>
            <Th>Daily Closing Price</Th>
            <Th>% Change (24 hr)</Th>
            <Th>% Change (30 Days)</Th>
            <Th>% Change (365 Days)</Th>
          </tr>
        </thead>
        <tbody>
          {symbolPerformance.map((item) => (
            <Tr key={item.symbol}>
              <Td>{item.symbol}</Td>
              <Td>{formatPercentage(item.daily_closing_price)}</Td>
              <Td isNegative={item.percentage_change_1day < 0}>
                {formatPercentage(item.percentage_change_1day)}
              </Td>
              <Td>{formatPercentage(item.percentage_change_30days)}</Td>
              <Td>{formatPercentage(item.percentage_change_365days)}</Td>
            </Tr>
          ))}
        </tbody>
      </Table>

      <SectionTitle><BoldText>Top Gainers</BoldText></SectionTitle>
      <Table>
        <thead>
          <tr>
            <Th>Company Code</Th>
            <Th>% Change (24 hr)</Th>
          </tr>
        </thead>
        <tbody>
          {topGainers.map((item) => (
            <Tr key={item.symbol}>
              <Td>{item.symbol}</Td>
              <Td isNegative={item.percentage_change_1day < 0}>
                {formatPercentage(item.percentage_change_1day)}
              </Td>
            </Tr>
          ))}
        </tbody>
      </Table>

      <SectionTitle><BoldText>Top Losers</BoldText></SectionTitle>
      <Table>
        <thead>
          <tr>
            <Th>Company Code</Th>
            <Th>% Change (24 hr)</Th>
          </tr>
        </thead>
        <tbody>
          {topLosers.map((item) => (
            <Tr key={item.symbol}>
              <Td>{item.symbol}</Td>
              <Td isNegative={item.percentage_change_1day < 0}>
                {formatPercentage(item.percentage_change_1day)}
              </Td>
            </Tr>
          ))}
        </tbody>
      </Table>
    </DashboardContainer>
  );
};

export default Dashboard;
