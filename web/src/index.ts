import {renderMap, renderPlacemarks} from "./ymaps";
import {Observable} from "./utils/observable";
import {getRecommendation} from "./api";

const selectedPlaceId = new Observable<string | null>(null)


const main = async () => {
    await renderMap('map')

    const places = await getRecommendation('Miramonti Boutique Hotel')

    selectedPlaceId.addListener(id => {
        const place = places.find(p => p.id === id)

        if (!id || !place) {
            return
        }
        document.querySelector('#title')!.textContent = place.name
        document.querySelector('#description')!.textContent = place.description
        document.querySelector('#review')!.textContent = place.review
    })

    await renderPlacemarks(places.map(place => ({
        coordinates: place.coordinates,
        onClick: () => {
            selectedPlaceId.value = place.id
        }
    })))
}

void main()
