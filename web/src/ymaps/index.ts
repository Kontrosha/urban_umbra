let mapInstance: ymaps.Map;

export const renderMap = async (state: ymaps.MapState): Promise<void> => new Promise(res => {
    ymaps.ready(() => {
        mapInstance = new ymaps.Map("map", state, {
            searchControlProvider: 'yandex#search'
        });
        res()
    })
})

export const renderPlacemarks = async (placemarks: Placemark[]): Promise<void> => new Promise(res => {
    ymaps.ready(() => {
        placemarks.forEach(pm => {
            mapInstance.geoObjects.add(
                new ymaps.Placemark(pm.coords, {
                    balloonContent: pm.htmlContent
                }, {
                    preset: 'islands#icon',
                    iconColor: pm.color || '#0095b6'
                })
            );
        })
        res()
    })
})