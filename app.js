// Function to fetch all products from the server asynchronously
async function fetchAllProducts() {
  try {
    // Make a request to the "data.json" file and parse the JSON response
    const response = await fetch("data.json");
    const data = await response.json();
    return data || []; // Return the parsed data or an empty array if no data is available
  } catch (error) {
    console.error("Error fetching products:", error); // Log an error if fetching fails
    return []; // Return an empty array in case of an error
  }
}

// Function to navigate to the product details page based on the provided product ID
function viewProduct(id) {
  window.location.href = `product.html?id=${id}`;
}

// Function to display products in the HTML based on an optional filter
async function displayAllProducts(filter = "") {
  // Fetch all products from the server
  const products = await fetchAllProducts();
  const productContainer = document.getElementById("product-container");
  let counter = 0;

  // Clear existing products in the container
  productContainer.innerHTML = "";

  // Iterate through each product and display it if it matches the search filter
  products.forEach((product) => {
    if (
      product.name.toLowerCase().includes(filter.toLowerCase()) ||
      product.category.toLowerCase().includes(filter.toLowerCase())
    ) {
      counter += 1;

      // Create HTML elements for each product and append them to the container
      const productElement = document.createElement("div");
      productElement.classList.add("col-sm-3", "col-md-4");
      productElement.innerHTML = `
        <div class="product">
          <img src="${product.thumbnail}" class="thumbnail" alt="${product.name}' Image">
          <div class="card-body">
            <h4 class="product-name">${product.name}</h4>
            <a onclick="viewProduct(${product.id})" class="view-product">View</a>
          </div>
        </div>
      `;
      productContainer.appendChild(productElement);
    }
  });

  // Update the heading to display the number of products
  const tableHeading = document.getElementById("tableHeading");
  tableHeading.innerHTML = `We've got over ${counter} products`;
}

// Event listener for the "DOMContentLoaded" event, executed when the page is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  const header = document.getElementById("header");

  // Display all products on page load
  displayAllProducts();

  // Add event listener for the search bar input
  const searchInput = document.getElementById("search");
  searchInput.addEventListener("input", () => {
    const searchTerm = searchInput.value;
    const isSearchEmpty = searchTerm.trim() === "";

    // Toggle the "hide" class based on whether the search term is empty
    header.classList.toggle("hide", !isSearchEmpty);

    // Display all products or filtered products based on the search term
    displayAllProducts(searchTerm);
  });
});
