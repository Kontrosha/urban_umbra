declare namespace ymaps {
    type Coordinates = [number, number]

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
            coordinates: Coordinates,
            state: PlacemarkState,
            options: PlacemarkOptions
        );

        events: {
            add: (type: 'click', cb: () => void) => void
        }
    }

    interface MapState {
        center: Coordinates;
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

        setBounds: ([Coordinates, Coordinates]) => void
    }
}