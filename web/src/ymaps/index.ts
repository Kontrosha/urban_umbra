import {getBoundingRect} from "../utils/coordinates";

let mapInstance: ymaps.Map;

export const renderMap = async (nodeId: string): Promise<void> => new Promise(res => {
    ymaps.ready(() => {
        mapInstance = new ymaps.Map(nodeId, {center: [0, 0], zoom: 1}, {
            searchControlProvider: 'yandex#search'
        });

        res()
    })
})

export const renderPlacemarks = async (placemarks: Placemark[]): Promise<void> => new Promise(res => {
    ymaps.ready(() => {
        const boundingRect = getBoundingRect(placemarks.map(placemark => placemark.coordinates))
        mapInstance.setBounds(boundingRect)

        placemarks.forEach(pm => {
            const placemark = new ymaps.Placemark(pm.coordinates, {
                balloonContent: pm.htmlContent
            }, {
                preset: 'islands#icon',
                iconColor: pm.color || '#0095b6'
            })

            pm.onClick && placemark.events.add('click', pm.onClick)

            mapInstance.geoObjects.add(
                placemark
            );
        })

        res()
    })
})