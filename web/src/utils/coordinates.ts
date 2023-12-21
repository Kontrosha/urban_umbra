import {Coordinates} from "../types/coordinates";

export const getBoundingRect = (coordinatesList: Coordinates[]): [Coordinates, Coordinates] => {
    const xCoords = coordinatesList.map(coordinates => coordinates[0])
    const yCoords = coordinatesList.map(coordinates => coordinates[1])

    const minX = Math.min(...xCoords)
    const maxX = Math.max(...xCoords)
    const minY = Math.min(...yCoords)
    const maxY = Math.max(...yCoords)

    return [[minX, minY], [maxX, maxY]]
}