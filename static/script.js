var currentResults = [];

$(document).ready(function () {
  // Similarity filter functionality
  $("#similarity-filter").on("input", function () {
    var threshold = parseFloat($(this).val());
    $("#similarity-threshold").text(threshold.toFixed(1));
    filterResults(threshold);
  });

  $("#upload-form").on("submit", function (e) {
    e.preventDefault();

    var formData = new FormData();
    var fileInput = $("#file-input")[0].files[0];
    var urlInput = $("#url-input").val();

    if (fileInput) {
      formData.append("file", fileInput);
    } else if (urlInput) {
      formData.append("url", urlInput);
    } else {
      alert("Please select a file or enter a URL.");
      return;
    }

    $("#loading").show();
    $("#results").hide();
    $("#uploaded-image-container").hide();
    $("#filter-container").hide();
    $("#similar-products").empty();

    $.ajax({
      url: "/api/search",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        $("#loading").hide();
        $("#results").show();

        if (fileInput) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#uploaded-image").attr("src", e.target.result);
            $("#uploaded-image-container").show();
          };
          reader.readAsDataURL(fileInput);
        } else if (urlInput) {
          $("#uploaded-image").attr("src", urlInput);
          $("#uploaded-image-container").show();
        }

        if (data.results && data.results.length > 0) {
          currentResults = data.results;
          $("#filter-container").show();
          displayResults(data.results);
        } else {
          $("#similar-products").html(
            '<div class="col-12"><p class="text-center">No similar products found.</p></div>'
          );
        }
      },
      error: function (xhr, status, error) {
        $("#loading").hide();
        alert("Error: " + xhr.responseText);
      },
    });
  });
});

function displayResults(results) {
  var similarProducts = $("#similar-products");
  similarProducts.empty();

  results.forEach(function (product) {
    var similarityClass =
      product.similarity > 0.7
        ? "success"
        : product.similarity > 0.4
        ? "warning"
        : "secondary";
    var productCard = `
            <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                <div class="card h-100">
                    <img src="${product.image_url}" class="card-img-top" alt="${
      product.name
    }" style="height: 200px; object-fit: cover;">
                    <div class="card-body d-flex flex-column">
                        <h6 class="card-title">${product.name}</h6>
                        <p class="card-text text-muted small">${
                          product.category
                        }</p>
                        <div class="mt-auto">
                            <span class="badge badge-${similarityClass}">Similarity: ${product.similarity.toFixed(
      2
    )}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    similarProducts.append(productCard);
  });
}

function filterResults(threshold) {
  var filteredResults = currentResults.filter(function (product) {
    return product.similarity >= threshold;
  });

  if (filteredResults.length === 0) {
    $("#similar-products").html(
      '<div class="col-12"><p class="text-center">No products meet the similarity threshold.</p></div>'
    );
  } else {
    displayResults(filteredResults);
  }
}
