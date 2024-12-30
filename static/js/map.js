// Инициализация карты
const map = L.map('map').setView([61.0034, 69.0279], 13);

// Подключение тайлов
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

// Массив для маркеров
const markers = [];

// Добавляем маркеры на карту
if (Array.isArray(landmarks)) {
    landmarks.forEach((item) => {
        const marker = L.marker([item.latitude, item.longitude]).addTo(map);

        // Содержимое всплывающего окна
        let popupContent = `<h3>${item.name}</h3><p>${item.address || 'Адрес не указан'}</p>`;
        marker.bindPopup(popupContent);

        // Добавляем маркер в массив
        markers.push(marker);
    });
} else {
    console.error("Landmarks is not an array or invalid.");
}
