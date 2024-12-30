import requests
import json
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_urls = [
    "https://data.admhmao.ru/api/data/index.php?id=3486739",
    "https://data.admhmao.ru/api/data/index.php?id=2567434",
    "https://data.admhmao.ru/api/data/index.php?id=3069450",
    "https://data.admhmao.ru/api/data/index.php?id=1933014",
    "https://data.admhmao.ru/api/data/index.php?id=1933180",
]

LIMIT = 100

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def fetch_all_data(base_url):
    all_data = []
    offset = 0

    while True:
        url = f"{base_url}&offset={offset}&limit={LIMIT}"
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            response = session.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()

            # Парсинг ответа
            data = response.json()
            rows = data.get("rows", [])
            if rows:
                # Извлечение данных из cols
                for row in rows:
                    cols = row.get("cols", {})
                    all_data.append(cols)
                offset += LIMIT
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            break

    return all_data

all_data = []
for base_url in base_urls:
    print(f"Обработка API: {base_url}")
    api_data = fetch_all_data(base_url)
    all_data.extend(api_data)

# Отладка перед сохранением
print(f"Всего объектов: {len(all_data)}")
print("Пример данных:", all_data[:1])

# Сохранение
output_file = "attractions.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f"Данные успешно сохранены в файл {output_file}!")
