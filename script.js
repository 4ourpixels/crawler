// Function to fetch product details from the server based on the product ID
async function fetchProductDetails(productId) {
  try {
    // Fetch product details from a specific category JSON file (Example: "data.json")
    const response = await fetch(`data.json`);
    const data = await response.json();
    return data || {}; // Return the parsed data or an empty object if no data is available
  } catch (error) {
    console.error(`Error fetching product details for ID ${productId}:`, error); // Log an error if fetching fails
    return {}; // Return an empty object in case of an error
  }
}

// Function to display product details on the product details page
async function displayProductDetails() {
  // Get the product ID from the URL query parameters
  const productId = getProductIdFromUrl();
  const productDetailsContainer = document.getElementById(
    "product-details-container"
  );

  // Check if a valid product ID is present in the URL
  if (productId) {
    // Fetch product details for the specified product ID
    const productDetails = await fetchProductDetails(productId);
    const product = await productDetails[productId];

    // Check if product details are available for the specified product ID
    if (product) {
      // Create HTML elements for displaying product details
      const productElement = document.createElement("div");
      const productImages = document.createElement("div");
      productElement.classList.add("text-start");
      productImages.classList.add("product-images");
      productElement.innerHTML = `
        <h2>${product.name}</h2>
        <p>Brand: ${product.brand}</p>
        <p>Category: ${product.category}</p>
        <p>${product.description}</p>
        <img src="${product.thumbnail}" class="img-fluid" alt="${
        product.name
      } Image" class="img-fluid me-2 mb-2 ">
        <br/>
        <button class="view-product mt-3" onclick="goBack()">Go Back</button>
        <br/>
        <br/>
         ${
           product.product_images
             ? displayProductImages(product.product_images)
             : ""
         }
      `;
      productDetailsContainer.appendChild(productElement);
    } else {
      // Display a message if product details are not found
      productDetailsContainer.innerHTML = `<h1 class="fw-bold display-1">Not found.</h1>`;
    }
  } else {
    // Display a message for an invalid product ID
    productDetailsContainer.innerHTML = "<p>Invalid product ID.</p>";
  }
}

// Function to display additional product images in the product details
function displayProductImages(images) {
  return `
    <div class="product-images">
      <h3>Other Product Images</h3>
      <div class="image-container">
        ${images
          .map(
            (image) =>
              `<img src="${image}" alt="Product Image" class="img-fluid mb-3 me-3 ">`
          )
          .join("")}
      </div>
    </div>
  `;
}

// Function to extract the product ID from the URL query parameters
function getProductIdFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("id");
}

// Function to navigate back in the browser history
function goBack() {
  window.history.back();
}

// Event listener for the "DOMContentLoaded" event, executed when the page is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  displayProductDetails();
});
