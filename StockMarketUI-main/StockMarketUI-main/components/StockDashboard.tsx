import React from 'react'
import { useSymbolPerformance, useTopLosers, useTopGainers } from '../hooks/useAPI'

const StockDashboard = () => {
  const { symbolPerformance, isLoading: isLoadingSP, isError: isErrorSP } = useSymbolPerformance()
  const { topLosers, isLoading: isLoadingTL, isError: isErrorTL } = useTopLosers()
  const { topGainers, isLoading: isLoadingTG, isError: isErrorTG } = useTopGainers()

  if (isLoadingSP || isLoadingTL || isLoadingTG) return <div>Loading...</div>
  if (isErrorSP || isErrorTL || isErrorTG) return <div>Error loading data</div>

  return (
    <div>
      <h1>Stock Market Data</h1>
      <h2>Symbol Performance</h2>
      <ul>
        {symbolPerformance.map((item) => (
          <li key={item.symbol}>
            {item.symbol} - Daily Closing Price: {item.daily_closing_price} - 1 Day Change: {item.percentage_change_1day}%
          </li>
        ))}
      </ul>

      <h2>Top Losers</h2>
      <ul>
        {topLosers.map((item) => (
          <li key={item.symbol}>
            {item.symbol} - 1 Day Change: {item.percentage_change_1day}%
          </li>
        ))}
      </ul>

      <h2>Top Gainers</h2>
      <ul>
        {topGainers.map((item) => (
          <li key={item.symbol}>
            {item.symbol} - 1 Day Change: {item.percentage_change_1day}%
          </li>
        ))}
      </ul>
    </div>
  )
}

export default StockDashboard

