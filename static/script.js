var currentResults = [];

$(document).ready(function () {
  // File upload area click handler
  $("#file-upload-area").on("click", function () {
    $("#file-input").click();
  });

  // File input change handler
  $("#file-input").on("change", function () {
    var file = this.files[0];
    if (file) {
      updateFileUploadArea(file.name);
    }
  });

  // Drag and drop handlers
  $("#file-upload-area").on("dragover", function (e) {
    e.preventDefault();
    $(this).addClass("dragover");
  });

  $("#file-upload-area").on("dragleave", function (e) {
    e.preventDefault();
    $(this).removeClass("dragover");
  });

  $("#file-upload-area").on("drop", function (e) {
    e.preventDefault();
    $(this).removeClass("dragover");
    
    var files = e.originalEvent.dataTransfer.files;
    if (files.length > 0) {
      $("#file-input")[0].files = files;
      updateFileUploadArea(files[0].name);
    }
  });

  // Clear URL button
  $("#clear-url").on("click", function () {
    $("#url-input").val("");
  });

  // Similarity filter functionality
  $("#similarity-filter").on("input", function () {
    var threshold = parseFloat($(this).val());
    $("#similarity-threshold").text(threshold.toFixed(1));
    filterResults(threshold);
  });

  // Form submission
  $("#upload-form").on("submit", function (e) {
    e.preventDefault();

    var formData = new FormData();
    var fileInput = $("#file-input")[0].files[0];
    var urlInput = $("#url-input").val().trim();

    if (fileInput) {
      formData.append("file", fileInput);
    } else if (urlInput) {
      formData.append("url", urlInput);
    } else {
      showAlert("Please select a file or enter a URL.", "warning");
      return;
    }

    // Show loading state
    showLoading();
    hideResults();

    $.ajax({
      url: "/api/search",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        hideLoading();
        showResults();

        // Display uploaded image
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

        // Display results
        if (data.results && data.results.length > 0) {
          currentResults = data.results;
          $("#filter-container").show();
          displayResults(data.results);
        } else {
          showNoResults();
        }
      },
      error: function (xhr, status, error) {
        hideLoading();
        var errorMessage = "An error occurred while processing your request.";
        try {
          var response = JSON.parse(xhr.responseText);
          errorMessage = response.error || errorMessage;
        } catch (e) {
          errorMessage = xhr.responseText || errorMessage;
        }
        showAlert(errorMessage, "danger");
      },
    });
  });
});

function updateFileUploadArea(fileName) {
  var uploadArea = $("#file-upload-area");
  uploadArea.html(`
    <i class="fas fa-check-circle upload-icon" style="color: var(--success-color);"></i>
    <h4>File Selected</h4>
    <p>${fileName}</p>
    <small class="text-muted">Click to change file</small>
  `);
}

function showLoading() {
  $("#loading").show();
  $("#results").hide();
}

function hideLoading() {
  $("#loading").hide();
}

function showResults() {
  $("#results").show();
}

function hideResults() {
  $("#results").hide();
  $("#uploaded-image-container").hide();
  $("#filter-container").hide();
  $("#similar-products").empty();
}

function showNoResults() {
  $("#similar-products").html(`
    <div class="col-12">
      <div class="text-center py-5">
        <i class="fas fa-search" style="font-size: 3rem; color: var(--light-text); margin-bottom: 1rem;"></i>
        <h4 style="color: var(--light-text);">No similar products found</h4>
        <p style="color: var(--light-text);">Try uploading a different image or adjusting your search criteria.</p>
      </div>
    </div>
  `);
}

function displayResults(results) {
  var similarProducts = $("#similar-products");
  similarProducts.empty();

  results.forEach(function (product) {
    var similarityPercentage = Math.round(product.similarity * 100);
    var similarityClass = getSimilarityClass(product.similarity);
    
    var productCard = `
      <div class="product-card">
        <img src="${product.image_url}" class="product-image" alt="${product.name}" 
             onerror="this.src='data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"280\" height=\"200\" viewBox=\"0 0 280 200\"><rect width=\"280\" height=\"200\" fill=\"%23f8f9fa\"/><text x=\"50%\" y=\"50%\" text-anchor=\"middle\" dy=\".3em\" fill=\"%236c757d\" font-family=\"Arial, sans-serif\">Image not found</text></svg>'">
        <div class="product-info">
          <h5 class="product-name">${product.name}</h5>
          <span class="product-category">${product.category}</span>
          <div class="similarity-score">
            <span class="similarity-label">Similarity</span>
            <span class="similarity-badge ${similarityClass}">${similarityPercentage}%</span>
          </div>
        </div>
      </div>
    `;
    similarProducts.append(productCard);
  });
}

function getSimilarityClass(similarity) {
  if (similarity >= 0.7) return "high";
  if (similarity >= 0.4) return "medium";
  return "low";
}

function filterResults(threshold) {
  var filteredResults = currentResults.filter(function (product) {
    return product.similarity >= threshold;
  });

  if (filteredResults.length === 0) {
    $("#similar-products").html(`
      <div class="col-12">
        <div class="text-center py-5">
          <i class="fas fa-filter" style="font-size: 3rem; color: var(--light-text); margin-bottom: 1rem;"></i>
          <h4 style="color: var(--light-text);">No products meet the similarity threshold</h4>
          <p style="color: var(--light-text);">Try lowering the similarity threshold to see more results.</p>
        </div>
      </div>
    `);
  } else {
    displayResults(filteredResults);
  }
}

function showAlert(message, type) {
  // Create a simple alert notification
  var alertClass = type === "danger" ? "alert-danger" : "alert-warning";
  var alertHtml = `
    <div class="alert ${alertClass} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
      <i class="fas fa-exclamation-triangle"></i>
      ${message}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  `;
  
  $("body").append(alertHtml);
  
  // Auto-dismiss after 5 seconds
  setTimeout(function() {
    $(".alert").fadeOut();
  }, 5000);
}

// Add CSS for similarity badge classes
$(document).ready(function() {
  $("<style>")
    .prop("type", "text/css")
    .html(`
      .similarity-badge.high { background: var(--success-color); }
      .similarity-badge.medium { background: var(--warning-color); color: var(--dark-text); }
      .similarity-badge.low { background: var(--light-text); }
    `)
    .appendTo("head");
});