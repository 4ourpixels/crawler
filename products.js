// Function to fetch data from products.json
async function fetchProducts() {
  try {
    const response = await fetch("products.json");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
}

// Function to display products in the product-container
async function displayProducts() {
  const products = await fetchProducts();
  const validProducts = products.filter((product) => product.data.length > 0);

  const productContainer = document.getElementById("product-container");

  validProducts.forEach((product) => {
    const productData = product.data[0];
    const imgLink = productData.href; // Assuming href contains the image URL

    const productElement = document.createElement("div");
    productElement.classList.add("col-md-4", "mb-4");
    productElement.innerHTML = `
      <div class="card">
        <img src="${imgLink}" loading="lazy" alt="${productData.title}' Image" class="img-fluid lazyload">
        <div class="card-body">
          <h5 class="card-title">
            <a href="${productData.href}" target="_blank">${productData.title}</a>
          </h5>
        </div>
      </div>
    `;
    productContainer.appendChild(productElement);
  });
}

// Execute the displayProducts function when the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  displayProducts();
});
