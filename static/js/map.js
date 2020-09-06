const mapContainer = document.getElementById("map"); // 지도를 표시할 div 입니다

let mapOption = {
  center: new kakao.maps.LatLng(34.844207, 128.443506), // 지도의 중심좌표
  level: 8, // 지도의 확대 레벨
  mapTypeId: kakao.maps.MapTypeId.ROADMAP, // 지도종류
};
// Data_set::임시방편으로..x
const map = new kakao.maps.Map(mapContainer, mapOption);
const places = [
  {
    title: "지화자술마시는 노래방",
    latlng: new kakao.maps.LatLng(34.84458, 128.4311),
  },
  {
    title: "박대감",
    latlng: new kakao.maps.LatLng(34.87762, 128.4219),
  },
  {
    title: "엠비씨웰빙삼겹살",
    latlng: new kakao.maps.LatLng(34.95894, 128.4116),
  },
];

var bounds = new kakao.maps.LatLngBounds();
// 지도 위에 마커와 인포윈도우 표시
for (var i = 0; i < places.length; i++) {
  var marker = new kakao.maps.Marker({
    map: map,
    position: places[i].latlng,
  });
  bounds.extend(places[i].latlng);
  var infowindow = new kakao.maps.InfoWindow({
    content: places[i].title,
  });

  kakao.maps.event.addListener(
    marker,
    "mouseover",
    makeOverListener(map, marker, infowindow)
  );
  kakao.maps.event.addListener(marker, "mouseout", makeOutListener(infowindow));
}

function makeOverListener(map, marker, infowindow) {
  return function () {
    infowindow.open(map, marker);
  };
}
function makeOutListener(infowindow) {
  return function () {
    infowindow.close();
  };
}
