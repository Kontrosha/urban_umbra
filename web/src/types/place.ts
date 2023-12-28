import {Coordinates} from "./coordinates";

export interface Place {
    id: string,
    coordinates: Coordinates,
    name: string
    description: string,
    review: string
}