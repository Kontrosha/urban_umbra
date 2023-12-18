declare namespace ymaps {
    type Coords = [number, number]

    function ready(cb: () => void);

    interface PlacemarkState {
        balloonContent?: string
    }

    interface PlacemarkOptions {
        preset: string,
        iconColor: string
    }

    class Placemark {
        constructor(
            coords: Coords,
            state: PlacemarkState,
            options: PlacemarkOptions
        );
    }

    interface MapState {
        center: Coords;
        zoom: number;
    }

    interface MapOptions {
        searchControlProvider: string
    }

    class Map {
        constructor(
            element: string | any,
            state: MapState,
            options: MapOptions
        );

        geoObjects: {
            add: (placemark: Placemark) => void
        }
    }
}