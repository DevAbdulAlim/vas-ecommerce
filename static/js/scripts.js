// Navbar

function myDropdown() {
    var dropdown = document.getElementById("myDropdown");
    dropdown.classList.toggle("show");
    document.getElementById("defaultOpen").click();
    setTimeout(function () {
      outsideListener();
    }, 0);
  }
  
  function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    document.getElementById(tabName).style.display = "flex";
    evt.currentTarget.className += " active";
  }
  
  // outside listener
  function outsideListener() {
    var content = document.getElementById("myDropdown");
    function handleClick(event) {
      if (content.classList.contains("show") && !content.contains(event.target)) {
        if (event.target !== document.getElementById("myDropdownBtn")) {
          content.classList.remove("show");
          document.removeEventListener("click", handleClick);
        }
      }
    }
    document.addEventListener("click", handleClick);
  }
  












  // Update Cart Item
  function updateCart(action, cartItemId) {
    const url = `/user/cart/update/${cartItemId}/`
    const csrfToken = getCookie('csrftoken')
  
    // Send AJAX request to update cart
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ action: action })
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle response
        if (data.success) {
          const quantityElement = document.querySelector(`[data-cart-item-id="${cartItemId}"] .quantity`)
          quantityElement.textContent = data.quantity

          console.log("success")
        } else {
          console.error(data.message)
        }
      })
      .catch((error) => {
        // Handle error if needed
        console.error(error)
      })
  }
  
  function getCookie(name) {
    const cookieValue = document.cookie.split(';').find((cookie) => cookie.trim().startsWith(name + '='))
    if (cookieValue) {
      return cookieValue.split('=')[1]
    }
    return null
  }
  
  // Event delegation for increase and decrease buttons
  document.addEventListener('click', function (event) {
    const target = event.target
    if (target.classList.contains('increase-btn')) {
      const cartItemId = target.closest('.quantity-controls').dataset.cartItemId
      updateCart('increase', cartItemId)
    } else if (target.classList.contains('decrease-btn')) {
      const cartItemId = target.closest('.quantity-controls').dataset.cartItemId
      updateCart('decrease', cartItemId)
    }
  })


  // payment 
  function toggleDiv(divId) {
    var hiddenDiv = document.getElementById(divId);

    if (hiddenDiv.style.display === 'none') {
      hiddenDiv.style.display = 'block';
    } else {
      hiddenDiv.style.display = 'none';
    }
  }