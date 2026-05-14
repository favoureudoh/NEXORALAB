// ── RUNS WHEN THE PAGE IS FULLY LOADED ──
document.addEventListener('DOMContentLoaded', function () {

  // Handle loading state on all forms
  handleFormSubmit()

  // Auto hide banners after 4 seconds
  autoDismissBanners()

})


// ── FORM SUBMIT LOADING STATE ──
// When a form is submitted, the button shows "Please wait..."
// This stops users from clicking the button multiple times

function handleFormSubmit() {
  const forms = document.querySelectorAll('form')

  forms.forEach(function (form) {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('button[type="submit"]')

      if (btn) {
        // Disable the button so it cannot be clicked again
        btn.disabled = true

        // Change the text so the user knows something is happening
        btn.textContent = 'Please wait...'

        // Add a visual dimmed style
        btn.style.opacity = '0.7'
        btn.style.cursor  = 'not-allowed'
      }
    })
  })
}


// ── AUTO DISMISS BANNERS ──
// Error and success banners fade out after 4 seconds

function autoDismissBanners() {
  const banners = document.querySelectorAll('.error-banner, .success-banner')

  banners.forEach(function (banner) {
    setTimeout(function () {
      // Smoothly fade the banner out
      banner.style.transition = 'opacity 0.6s ease'
      banner.style.opacity    = '0'

      // Remove it from the page after the fade completes
      setTimeout(function () {
        banner.remove()
      }, 600)

    }, 4000) // 4 seconds before it starts fading
  })
}