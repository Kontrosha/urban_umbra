import {renderMap, rerenderPlacemarks} from "./ymaps";
import {Observable} from "./utils/observable";
import {getRecommendation} from "./api";

const selectedPlaceId = new Observable<string | null>(null)


const main = async () => {
    await renderMap('map')

    document.getElementById('submit-button')?.addEventListener('click', async e => {
        e.preventDefault()

        const hotelName = (document.getElementById('hotels') as HTMLSelectElement).value
        const places = await getRecommendation(hotelName)

        selectedPlaceId.addListener(id => {
            const place = places.find(p => p.id === id)

            if (!id || !place) {
                return
            }
            document.querySelector('#title')!.textContent = place.name
            document.querySelector('#description')!.textContent = place.description
            document.querySelector('#review')!.textContent = place.review
        })

        await rerenderPlacemarks(places.map(place => ({
            coordinates: place.coordinates,
            onClick: () => {
                selectedPlaceId.value = place.id
            }
        })))
    })
}

void main()
