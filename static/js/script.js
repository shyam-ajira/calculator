// document.addEventListener('DOMContentLoaded', () => {
//     const roomItems = document.querySelectorAll('.room-item');
//     const addFloorButton = document.querySelector('.add-floor');
//     const hideSpacesButton = document.querySelector('.add-space');
//     const otherSpacesDiv = document.querySelector('.other-spaces');
//     const roomList = document.querySelector('.room-list');

//     // Room Quantity Control
//     roomItems.forEach(roomItem => {
//         const minusButton = roomItem.querySelector('.minus');
//         const plusButton = roomItem.querySelector('.plus');
//         const quantitySpan = roomItem.querySelector('.quantity');
//         let quantity = 0;

//         minusButton.addEventListener('click', () => {
//             if (quantity > 0) {
//                 quantity--;
//                 quantitySpan.textContent = quantity;
//             }
//         });

//         plusButton.addEventListener('click', () => {
//             quantity++;
//             quantitySpan.textContent = quantity;
//         });
//     });

//     // Add Floor Functionality
//     let floorNumber = 1;
//     addFloorButton.addEventListener('click', () => {
//         floorNumber++;
//         const newFloorDiv = document.createElement('div');
//         newFloorDiv.classList.add('floor-selector');
//         newFloorDiv.innerHTML = `<label for="floor-number">Floor ${floorNumber}</label>
//                                  <button class="add-floor">+</button>`;

//         const newFloorRoomList = document.createElement('div');
//         newFloorRoomList.classList.add('room-list');

//         roomItems.forEach(room => {
//             const clonedRoom = room.cloneNode(true);
//             newFloorRoomList.appendChild(clonedRoom);

//             const clonedMinusButton = clonedRoom.querySelector('.minus');
//             const clonedPlusButton = clonedRoom.querySelector('.plus');
//             const clonedQuantitySpan = clonedRoom.querySelector('.quantity');
//             let clonedQuantity = 0;

//             clonedMinusButton.addEventListener('click', () => {
//                 if (clonedQuantity > 0) {
//                     clonedQuantity--;
//                     clonedQuantitySpan.textContent = clonedQuantity;
//                 }
//             });

//             clonedPlusButton.addEventListener('click', () => {
//                 clonedQuantity++;
//                 clonedQuantitySpan.textContent = clonedQuantity;
//             });
//         });
//         newFloorDiv.appendChild(newFloorRoomList);
//         roomList.parentNode.insertBefore(newFloorDiv, roomList.nextSibling);

//         const newAddFloorButton = newFloorDiv.querySelector('.add-floor');
//         newAddFloorButton.addEventListener('click', () => {
//             addFloor(newFloorDiv);
//         });
//     });

//     // Hide Additional Spaces Functionality
//     let spacesHidden = false;
//     hideSpacesButton.addEventListener('click', () => {
//         const otherSpaceRoomItems = document.querySelectorAll('.room-item:nth-child(n+9)');
//         if (!spacesHidden) {
//             otherSpaceRoomItems.forEach(item => {
//                 item.style.display = 'none';
//             });
//             hideSpacesButton.textContent = 'Show additional spaces';
//             spacesHidden = true;
//         } else {
//             otherSpaceRoomItems.forEach(item => {
//                 item.style.display = 'flex';
//             });
//             hideSpacesButton.textContent = 'Hide additional spaces';
//             spacesHidden = false;
//         }
//     });
// });