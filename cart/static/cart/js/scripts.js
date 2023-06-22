


// Delete Cart Item
    function deleteCartItem(cartItemId) {
      const url = `/user/cart/delete/${cartItemId}/`;
      const csrfToken = getCookie('csrftoken');
    
      // Send AJAX request to delete cart item
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle response
          if (data.success) {
            // Remove the deleted cart item from the DOM
            const cartItemElement = document.querySelector(`[data-cart-item-id="${cartItemId}"]`).closest('.item');
            if (cartItemElement) {
              cartItemElement.remove();
            }
          } else {
            console.error(data.message);
          }
        })
        .catch((error) => {
          // Handle error if needed
          console.error(error);
        });
    }
