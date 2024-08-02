import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function useSymbolPerformance() {
  const { data, error } = useSWR('/api/symbol_performance/', fetcher)
  return {
    symbolPerformance: data,
    isLoading: !error && !data,
    isError: error
  }
}

export function useTopLosers() {
  const { data, error } = useSWR('/api/top_losers/', fetcher)
  return {
    topLosers: data,
    isLoading: !error && !data,
    isError: error
  }
}

export function useTopGainers() {
  const { data, error } = useSWR('/api/top_gainers/', fetcher)
  return {
    topGainers: data,
    isLoading: !error && !data,
    isError: error
  }
}

