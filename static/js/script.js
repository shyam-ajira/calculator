document.addEventListener('DOMContentLoaded', function () {
    const addFloorButton = document.querySelector('.add-floor');
    const staircaseCheckbox = document.querySelector('.staircase-checkbox');
    const roomList = document.querySelector('.room-list');
    const quantityControls = document.querySelectorAll('.quantity-control');
    
    // Add floor functionality
    addFloorButton.addEventListener('click', function() {
        const floorNumber = document.querySelectorAll('.floor-selector label').length + 1;
        const newFloor = document.createElement('div');
        newFloor.classList.add('floor-selector');
        newFloor.innerHTML = `
            <label for="floor-number">Floor ${floorNumber}</label>
            <button class="add-floor">+</button>
        `;
        document.querySelector('.floor-selector').after(newFloor);
    });

    // Staircase checkbox functionality
    staircaseCheckbox.addEventListener('change', function() {
        if (this.checked) {
            roomList.style.display = 'none'; // Hide the room list
        } else {
            roomList.style.display = 'block'; // Show the room list
        }
    });


    // Quantity control buttons
    quantityControls.forEach(function(control) {
        const minusButton = control.querySelector('.minus');
        const plusButton = control.querySelector('.plus');
        const quantityDisplay = control.querySelector('.quantity');

        minusButton.addEventListener('click', function() {
            let quantity = parseInt(quantityDisplay.textContent);
            if (quantity > 0) {
                quantity--;
                quantityDisplay.textContent = quantity;
            }
        });

        plusButton.addEventListener('click', function() {
            let quantity = parseInt(quantityDisplay.textContent);
            quantity++;
            quantityDisplay.textContent = quantity;
        });
    });
});
