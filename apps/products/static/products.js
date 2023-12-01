async function updateButton(product_id, btn, csrf_token) {
  const response = await fetch('/cart/has_product/' + product_id)
  const data = await response.json()
  if (data.has_product) {
    btn.innerHTML = 'Añadido al carrito'
    btn.classList.add('disabled-btn')
    btn.removeEventListener('click', () => {
      spawnBuyModal(product_id, csrf_token)
    })
  } else {
    btn.innerHTML = 'Reservar'
    btn.classList.remove('disabled-btn')
    btn.addEventListener('click', () => {
      spawnBuyModal(product_id, csrf_token)
    })
  }
}

function validateDate(date, disabled_dates) {
  const to_date_input = document.querySelector('#to-date')
  const error_msg = document.querySelector('#error-msg')

  if (disabled_dates.includes(date)) {
    error_msg.innerHTML = 'La fecha seleccionada no está disponible'
    to_date_input.disabled = true
    return false
  } else {
    error_msg.innerHTML = ''
  }

  const from_date = new Date(date)
  const minDate = new Date(from_date)
  minDate.setDate(minDate.getDate() + 1)
  to_date_input.min = minDate.toISOString().slice(0, 10)

  /* get closest date to from_date that is bigger than from_date */
  const tmp_disabled_dates = disabled_dates.filter(
    (d) => new Date(d) > from_date,
  )
  tmp_disabled_dates.sort((a, b) => new Date(a) - new Date(b))

  let to_date
  if (tmp_disabled_dates.length !== 0) {
    to_date = new Date(tmp_disabled_dates[0])
    to_date.setDate(to_date.getDate() - 1)
  } else {
    const today = new Date()
    const maxDate = new Date(
      today.getFullYear() + 1,
      today.getMonth(),
      today.getDate(),
    )
      .toISOString()
      .slice(0, 10)
    to_date = new Date(maxDate)
  }

  to_date_input.disabled = false
  to_date_input.max = to_date.toISOString().slice(0, 10)

  to_date_input.value = ''

  return true
}

async function getDisabledDates(product_id) {
  const response = await fetch('/products/disabled_dates/' + product_id)
  const data = await response.json()
  const disabled_dates = []
  const dates = data.disabled_dates
  dates.forEach((date) => {
    const start_date = new Date(date.start)
    const end_date = new Date(date.end)
    const tmp_date = new Date(start_date)
    while (tmp_date <= end_date) {
      disabled_dates.push(tmp_date.toISOString().slice(0, 10))
      tmp_date.setDate(tmp_date.getDate() + 1)
    }
  })
  return disabled_dates
}

async function addProductToCart(from_date, to_date, product_id, csrf_token) {
  const response = await fetch('/cart/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({
      product_id: product_id,
      from_date: from_date,
      to_date: to_date,
    }),
  })
  const data = await response.json()
  const error_msg = document.querySelector('#error-msg')
  if (data.error) {
    error_msg.innerHTML = data.error
  } else {
    error_msg.innerHTML = ''
    getCartCount()
    updateButton()
    showNotification('Producto añadido al carrito', 'success')
    closeModal()
  }
}

function closeModal() {
  const modal = document.querySelector('.modal')
  modal.style.display = 'none'
}

async function spawnBuyModal(product_id, csrf_token) {
  const response = await getDisabledDates(product_id)
  const disabled_dates = await response
  const modal = document.querySelector('.modal')

  /* minDate is today */
  const today = new Date()
  const minDate = today.toISOString().slice(0, 10)
  const maxDate = new Date(
    today.getFullYear() + 1,
    today.getMonth(),
    today.getDate(),
  )
    .toISOString()
    .slice(0, 10)

  const from_date_input = document.querySelector('#from-date')
  from_date_input.min = minDate
  from_date_input.max = maxDate

  modal.style.display = 'flex'
  const close = modal.querySelector('.close')
  close.addEventListener('click', () => {
    modal.style.display = 'none'
  })

  document.querySelector('#from-date').onchange = (evt) => {
    if (!validateDate(evt.target.value, disabled_dates)) {
      evt.target.value = ''
    }
  }

  /* remove all confirmn-btn event listeners */
  const confirm_btn = document.querySelector('#confirm-btn')
  const new_confirm_btn = confirm_btn.cloneNode(true)
  confirm_btn.parentNode.replaceChild(new_confirm_btn, confirm_btn)

  document.querySelector('#confirm-btn').addEventListener('click', () => {
    const from_date = document.querySelector('#from-date').value
    const to_date = document.querySelector('#to-date').value
    if (from_date && to_date) {
      addProductToCart(from_date, to_date, product_id, csrf_token)
    }
  })
}
