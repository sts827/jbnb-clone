/* Location 정보 가져오기 */
const weather = document.querySelector(".js-weather");
const API_KEY = "feb793ec48123474580d7168b8e8a261";
const COORDS = "coords";

function getWeather(lat, lng) {
  fetch(
    `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${API_KEY}&units=metric`
  )
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      const temperature = json.main.temp;
      const location = json.name;
      weather.innerText = `온도:${temperature}`;
    });
}

function saveLocation(coordObj) {
  localStorage.setItem(COORDS, JSON.stringify(coordObj));
}

function handleSuccess(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  const coordObj = {
    latitude: latitude,
    longitude: longitude,
  };
  saveLocation(coordObj);
  getWeather(latitude, longitude);
}

function handleError() {
  console.log("Can't Access geoLocation");
}

function askForLocation() {
  navigator.geolocation.getCurrentPosition(handleSuccess, handleError);
}

function loadCoords() {
  const loadedCoords = localStorage.getItem(COORDS);
  if (loadedCoords === null) {
    askForLocation();
  } else {
    //getWeather
    const parsedCoords = JSON.parse(loadedCoords);
    getWeather(parsedCoords.latitude, parsedCoords.longitude);
  }
}

function init() {
  loadCoords();
}

init();
