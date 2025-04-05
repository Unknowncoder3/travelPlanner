document.getElementById("search-btn").addEventListener("click", function () {
    const searchType = document.querySelector('input[name="searchType"]:checked').value;
  
    let payload = { type: searchType };
  
    if (searchType === "state") {
      payload.state = document.getElementById("state").value;
      payload.rating = document.getElementById("rating").value;
    } else {
      payload.category = document.getElementById("category").value;
      payload.geo_type = document.getElementById("geo_type").value;
    }
  
    fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        const resultDiv = document.getElementById("results");
        resultDiv.innerHTML = "";
  
        if (!data.success || data.results.length === 0) {
          resultDiv.innerHTML = "<p>No results found.</p>";
          return;
        }
  
        data.results.forEach((item) => {
          const card = document.createElement("div");
          card.classList.add("card");
  
          card.innerHTML = `
            <h3>${item.Destination}</h3>
            <p>Rating: ${item.Rating}</p>
            <p>${item.Description}</p>
            <p><strong>Offbeat:</strong> ${item.Offbeat_place}</p>
            <p><strong>Local Food:</strong> ${item.Local_Food}</p>
            <img src="${item.picture_place}" alt="Place Image" />
            <img src="${item.picture_food}" alt="Food 1" />
            <img src="${item.picture_food1}" alt="Food 2" />
            <img src="${item.picture_offbit}" alt="Offbeat 1" />
            <img src="${item.picture_offbit1}" alt="Offbeat 2" />
          `;
  
          resultDiv.appendChild(card);
        });
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  });
  