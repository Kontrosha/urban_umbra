import {renderMap, renderPlacemarks} from "./ymaps";
import example from '../../back/src/example.json';
import {Place} from "./types/place";
import {Observable} from "./utils/observable";
import { v4 as uuid } from 'uuid';

const places = example.map(place => ({id: uuid(), ...place})) as Place[]

const selectedPlaceId = new Observable<string | null>(null)
selectedPlaceId.addListener(id => {
    const place = places.find(p => p.id === id)

    if (!id || !place) {
        return
    }
    document.querySelector('#title')!.textContent = place.name
    document.querySelector('#description')!.textContent = place.description
})

const main = async () => {
    await renderMap('map')

    await renderPlacemarks(places.map(place => ({
        coordinates: place.coordinates,
        onClick: () => {
            selectedPlaceId.value = place.id
        }
    })))
}

void main()
