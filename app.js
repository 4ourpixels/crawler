// Load categories data from navlinks.json
fetch("navlinks.json")
  .then((response) => response.json())
  .then((categoriesData) => {
    // Function to populate the table with categories data
    function populateTable(pageNumber, pageSize) {
      var startIndex = (pageNumber - 1) * pageSize;
      var endIndex = startIndex + pageSize;

      var tableBody = document
        .getElementById("categoriesTable")
        .getElementsByTagName("tbody")[0];
      tableBody.innerHTML = ""; // Clear existing rows

      for (var i = startIndex; i < endIndex && i < categoriesData.length; i++) {
        var category = categoriesData[i];
        var row = `<tr>
                      <th scope="row">${i + 1}</th>
                      <td>${category.category}</td>
                      <td><a target="_blank" href="${
                        category.href
                      }" class="link">View</a></td>
                      <td>${category["data-id"]}</td>
                      </tr>`;
        tableBody.innerHTML += row;
      }
    }

    // Function to generate pagination links
    function generatePaginationLinks(totalPages) {
      var pagination = document.getElementById("pagination");
      pagination.innerHTML = ""; // Clear existing pagination links

      for (var i = 1; i <= totalPages; i++) {
        var li = document.createElement("li");
        li.className = "page-item";
        var a = document.createElement("a");
        a.className = "page-link";
        a.href = "#";
        a.innerText = i;
        a.addEventListener("click", function (event) {
          event.preventDefault();
          var pageNumber = parseInt(event.target.innerText);
          populateTable(pageNumber, 10); // Adjust the page size as needed
        });
        li.appendChild(a);
        pagination.appendChild(li);
      }
    }

    // Initial population of the table with the first page
    populateTable(1, 10); // Adjust the page size as needed

    // Assuming categoriesData is the array of objects obtained from navlinks.json
    var totalPages = Math.ceil(categoriesData.length / 10); // Adjust the page size as needed
    generatePaginationLinks(totalPages);
  })
  .catch((error) => console.error("Error loading navlinks.json:", error));
