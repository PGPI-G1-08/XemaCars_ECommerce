async function updateButton(order_id, btn, csrf_token) {
  btn.addEventListener('click', () => {
    spawnBuyModal(order_id, csrf_token)
  })
}

async function changeStatus(order_id, status, csrf_token) {
  const response = await fetch('/orders/change-status', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({
      order_id: order_id,
      status: status,
    }),
  })
  const data = await response.json()
  const error_msg = document.querySelector('#error-msg')
  if (data.error) {
    error_msg.innerHTML = data.error
  } else {
    error_msg.innerHTML = ''
    window.location.reload()
  }
}

function closeModal() {
  const modal = document.querySelector('.modal')
  modal.style.display = 'none'
}

async function spawnBuyModal(order_id, csrf_token) {
  const modal = document.querySelector('.modal')
  const status = document
    .querySelector(`#order-${order_id}-status`)
    .innerHTML.split(': ')[1]
  const status_nopagado = document.querySelector('#status-nopagado')
  const status_pagado = document.querySelector('#status-pagado')
  if (status === 'No pagado') {
    status_nopagado.selected = true
  } else {
    status_pagado.selected = true
  }

  modal.style.display = 'flex'
  const close = modal.querySelector('.close')
  close.addEventListener('click', () => {
    modal.style.display = 'none'
  })

  /* remove all confirmn-btn event listeners */
  const confirm_btn = document.querySelector('#confirm-btn')
  const new_confirm_btn = confirm_btn.cloneNode(true)
  confirm_btn.parentNode.replaceChild(new_confirm_btn, confirm_btn)

  document.querySelector('#confirm-btn').addEventListener('click', () => {
    const status = document.querySelector('#status-select').value
    changeStatus(order_id, status, csrf_token)
  })
}
