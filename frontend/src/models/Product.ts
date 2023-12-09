export interface Product{
    id?: string
    name: string,
    price: number,
    specifications?: {
        
    },
    min_price: number,
    max_price: number,
    sales?: [number]
    scores?: [number]
    prices?: [number],
    recommended_price?: number| null,
    urls: {
        flipkartURL: string,
        amazonURL: string
    }
    type: string
}