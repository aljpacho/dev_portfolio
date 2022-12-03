let searchBtn = document.getElementById("search-btn");
let countryInput = document.getElementById("country-input");

searchBtn.addEventListener("click", () => {
  let countryName = countryInput.value;
  let finalURL = `https://restcountries.com/v3.1/name/${countryName}?fullText=true`;
  fetch(finalURL)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").innerHTML = `
      <img src="${data[0].flags.svg}" class="flag-img">
      <h2>${data[0].name.common}</h2>
      <div class="wrapper">
        <div class="data-wrapper">
          <h4>Capital: </h4>
          <span>${data[0].capital}</span>
        </div>
      <div>
      <div class="wrapper">
        <div class="data-wrapper">
          <h4>Continent: </h4>
          <span>${data[0].region}</span>
        </div>
      </div>
      <div class="wrapper">
        <div class="data-wrapper">
          <h4>Population: </h4>
          <span>${data[0].population}</span>
        </div>
      </div>
      <div class="wrapper">
        <div class="data-wrapper">
          <h4>Currency: </h4>
          <span>
            ${data[0].currencies[Object.keys(data[0].currencies)].name}
             (${Object.keys(data[0].currencies)})
          </span>
        </div>
      </div>
      <div class="wrapper">
        <div class="data-wrapper">
          <h4>Common Languages: </h4>
          <span>
            ${Object.values(data[0].languages).join(", ")}
          </span>
        </div>
      </div>
      `;
    }).catch(() => {
        if (countryName.length == 0) {
            document.getElementById("result").innerHTML = "<h3>Please enter a country"
        } else {
            document.getElementById("result").innerHTML = "<h3>Please enter a valid country</h3>"
        }
    })
});
