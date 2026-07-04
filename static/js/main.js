document.addEventListener('DOMContentLoaded', function(){
  // Theme toggle: persist in localStorage
  const themeToggle = document.getElementById('theme-toggle')
  const current = localStorage.getItem('theme')
  if(current === 'light') document.body.setAttribute('data-theme','light')
  if(themeToggle){
    themeToggle.addEventListener('click', ()=>{
      const isLight = document.body.getAttribute('data-theme') === 'light'
      if(isLight){
        document.body.removeAttribute('data-theme')
        localStorage.setItem('theme','dark')
      } else {
        document.body.setAttribute('data-theme','light')
        localStorage.setItem('theme','light')
      }
    })
  }

  // Helper: get CSRF token from cookies
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')
    return v ? v.pop() : ''
  }

  const csrftoken = getCookie('csrftoken')

  // Modal controls for confirmation
  const modal = document.getElementById('modal')
  const modalTitle = document.getElementById('modal-title')
  const modalBody = document.getElementById('modal-body')
  const modalConfirm = document.getElementById('modal-confirm')
  const modalCancel = document.getElementById('modal-cancel')
  let modalConfirmCallback = null

  function showModal(title, body, onConfirm){
    modal.setAttribute('aria-hidden','false')
    modalTitle.textContent = title
    modalBody.textContent = body
    modalConfirmCallback = onConfirm
  }
  function hideModal(){
    modal.setAttribute('aria-hidden','true')
    modalConfirmCallback = null
  }
  modalCancel.addEventListener('click', hideModal)
  modalConfirm.addEventListener('click', function(){ if(typeof modalConfirmCallback === 'function') modalConfirmCallback(); hideModal(); })

  // AJAX delete: intercept delete links with data-delete-url
  document.querySelectorAll('a.delete-ajax').forEach(function(a){
    a.addEventListener('click', function(e){
      e.preventDefault()
      const url = a.getAttribute('data-delete-url')
      showModal('Eliminar movimiento', '¿Eliminar este movimiento permanentemente?', ()=>{
        fetch(url, { method: 'POST', headers: { 'X-CSRFToken': csrftoken } })
          .then(resp => {
            if(resp.ok){
              const article = a.closest('article.movement-card')
              if(article) article.remove()
            } else {
              alert('No se pudo eliminar')
            }
          }).catch(()=> alert('Error de red'))
      })
    })
  })

  // Real-time monto preview and basic validation
  const montoInput = document.querySelector('input[name="monto"]')
  const tipoSelect = document.querySelector('select[name="tipo"]')
  const preview = document.querySelector('.monto-preview')
  if(montoInput && preview){
    function updatePreview(){
      let v = montoInput.value || '0'
      // ensure two decimals
      const num = parseFloat(v)
      if(isNaN(num)) v = '0.00'
      else v = num.toFixed(2)
      const tipo = (tipoSelect && tipoSelect.value) || 'gasto'
      preview.textContent = (tipo === 'gasto' ? '-' : '+') + v
      preview.className = 'monto-preview ' + tipo
    }
    montoInput.addEventListener('input', updatePreview)
    if(tipoSelect) tipoSelect.addEventListener('change', updatePreview)
    updatePreview()
  }
})
