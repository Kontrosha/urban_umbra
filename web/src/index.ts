import {renderMap, renderPlacemarks} from "./ymaps";

const main = async () => {
    await renderMap({
        center: [9.5356700, 99.9356700],
        zoom: 10
    })

    await renderPlacemarks([{
        coords: [9.5356700, 99.9356700],
        htmlContent: '1 <strong>геолокация</strong>'
    }, {
        coords: [9.5456700, 99.9656700],
        htmlContent: '2 <strong>геолокация</strong>'
    }, {
        coords: [9.5456700, 99.9556700],
        htmlContent: '3 <strong>геолокация</strong>'
    }])
}

void main()
