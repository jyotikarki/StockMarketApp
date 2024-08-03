// services/types.ts

export interface Stock {
    id: number;
    symbol: string;
    name: string;
    latestPrice: number; // Add this if you don't already have a similar field
}


export interface DailyPrice {
    id: number;
    stock: Stock;
    date: string;
    open_price: string;
    close_price: string;
    volume: number;
}

export interface PriceChange {
    id: number;
    stock: Stock;
    period: string;
    percentage_change: string;
}

export interface TopGainer {
    id: number;
    date: string;
    stock: Stock;
    percentage_gain: string;
}

export interface TopLoser {
    id: number;
    date: string;
    stock: Stock;
    percentage_loss: string;
}

