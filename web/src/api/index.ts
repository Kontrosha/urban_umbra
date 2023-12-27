import {Place} from "../types/place";
import { v4 as uuid } from 'uuid';

type RawPlace = {
    coordinates: [string, string],
    name: string
    description: string,
    review: string
}

export const getRecommendation = async (hotelName: string, mock?: boolean): Promise<Place[]> => {
    let data: RawPlace[]

    if (mock) {
        data = [
            {
                "coordinates": [
                    "47.3634",
                    "11.72411"
                ],
                "description": "Der Traubenwirt - это прекрасный отель в Тироле, Австрия, известный своей аутентичной альпийской атмосферой и гостеприимным сервисом. Отель расположен в живописном окружении горных пейзажей и предлагает своим гостям комфортное проживание и изысканную кухню. Это идеальное место для любителей активного отдыха, так как рядом находятся горные тропы и лыжные курорты.",
                "name": "Der Traubenwirt",
                "review": "No reviews"
            },
            {
                "coordinates": [
                    "47.252858",
                    "11.162618"
                ],
                "description": "Конечно! Elephant, расположенный в Тироле, Австрия, - это уютный ресторан с замечательной атмосферой и изысканным меню. Здесь вы можете насладиться блюдами европейской кухни, где основное внимание уделяется свежим местным ингредиентам. Владельцы заведения действительно заботятся о качестве и сервисе, делая Elephant идеальным местом для романтического ужина или специального мероприятия.",
                "name": "Elephant",
                "review": "No reviews"
            },
            {
                "coordinates": [
                    "47.252858",
                    "11.162618"
                ],
                "description": "Grissino — это уютная деревня в регионе Тироль, в Австрии. Она известна своей очаровательной архитектурой, традиционными домами и красивыми пейзажами. В этом месте можно насладиться живописными горными видами, попробовать местную кухню и насладиться активным отдыхом на свежем воздухе. Grissino — отличный выбор для тех, кто ищет спокойствие и природу во время своей поездки в Австрию.",
                "name": "Grissino",
                "review": "No reviews"
            }
        ]
    } else {
        const response = await fetch("http://kontrosha.pythonanywhere.com/get_closest_coordinates", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hotel: hotelName
            })})

        data = await response.json()
    }

    return data.map(({coordinates: [a, b], ...p}) => ({id: uuid(), ...p, coordinates: [Number(a), Number(b)]}))
}
