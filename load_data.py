import json
from app import db, Landmark, app

def clean_coordinate(coord):
    """
    Удаляет нежелательные символы, такие как '°', и возвращает координату как float.
    Если координата некорректная, возвращает None.
    """
    try:
        return float(coord.replace("°", "").strip())
    except (ValueError, AttributeError):
        return None

def load_landmarks():
    with open('data/landmarks.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            try:
                latitude = clean_coordinate(item.get("SHIROTA", "0"))
                longitude = clean_coordinate(item.get("DOLGOTA", "0"))

                # Проверяем, что координаты валидны
                if latitude is None or longitude is None:
                    raise ValueError("Неверные координаты")

                landmark = Landmark(
                    name=item.get("NAME", "Неизвестный объект"),
                    address=item.get("ADDRESS", "Адрес не указан"),
                    photo=item.get("PHOTO"),
                    type=item.get("TYPE"),
                    fio_rukovoditelya=item.get("FIO_RUKOVODITELYA"),
                    phone=item.get("PHONE"),
                    rezhim_raboty=item.get("REZHIM_RABOTY"),
                    sayt=item.get("SAYT"),
                    elektronnaya_pochta=item.get("ELEKTRONNAYA_POCHTA"),
                    sportivnye_sektsii=item.get("SPORTIVNYE_SEKTSII"),
                    naimenovanie_geoobekta=item.get("NAIMENOVANIE_GEOOBEKTA"),
                    latitude=latitude,
                    longitude=longitude
                )
                db.session.add(landmark)
            except ValueError as e:
                print(f"Ошибка обработки записи: {item}")
                print(e)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        load_landmarks()
        print("Данные успешно загружены.")
