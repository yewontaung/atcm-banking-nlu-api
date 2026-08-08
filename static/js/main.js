/**
 * ATCM Banking API Developer Platform - Main Application JS
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initMobileNav();
  initQuickFill();
  initCopyButtons();
  initErrorFilter();
});

function initErrorFilter() {
  // 1. Parse URL query parameters
  const urlParams = new URLSearchParams(window.location.search);
  const errorMessage = urlParams.get('error');

  // 2. If 'error' parameter exists in URL, show toast
  if (errorMessage) {
    showToast(errorMessage, "error");
  }
}

/* Theme Toggle (Dark/Light) */
function initThemeToggle() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeToggleIcon');

  // Load saved theme or default to dark
  const savedTheme = localStorage.getItem('atcm_theme') || 'dark';
  applyTheme(savedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
      localStorage.setItem('atcm_theme', newTheme);
    });
  }

  function applyTheme(theme) {
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
      if (toggleBtn) toggleBtn.title = 'Switch to Dark Mode';
      if (themeIcon) themeIcon.className = 'fas fa-moon';
    } else {
      document.documentElement.removeAttribute('data-theme');
      if (toggleBtn) toggleBtn.title = 'Switch to Light Mode';
      if (themeIcon) themeIcon.className = 'fas fa-sun';
    }
  }
}

/* Mobile Nav Toggle */
function initMobileNav() {
  const toggleBtn = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = navMenu.classList.toggle('open');
      const icon = toggleBtn.querySelector('i');
      if (icon) {
        icon.className = isOpen ? 'fas fa-times' : 'fas fa-bars';
      }
    });

    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
        if (navMenu.classList.contains('open')) {
          navMenu.classList.remove('open');
          const icon = toggleBtn.querySelector('i');
          if (icon) icon.className = 'fas fa-bars';
        }
      }
    });
  }
}

/* Quick Auto-Fill for Sign-In and Sign-Up */
function initQuickFill() {
  // Sign-In User auto-fill
  const fillUserSignInBtn = document.getElementById('fillUserSignIn');
  if (fillUserSignInBtn) {
    fillUserSignInBtn.addEventListener('click', () => {
      const emailInput = document.getElementById('email');
      const passInput = document.getElementById('password');
      if (emailInput) emailInput.value = 'dev@atcm-bank.com';
      if (passInput) passInput.value = 'developer123';
      showToast('Autofilled User credentials!');
    });
  }

  // Sign-In Admin auto-fill
  const fillAdminSignInBtn = document.getElementById('fillAdminSignIn');
  if (fillAdminSignInBtn) {
    fillAdminSignInBtn.addEventListener('click', () => {
      const emailInput = document.getElementById('email');
      const passInput = document.getElementById('password');
      if (emailInput) emailInput.value = 'admin@atcm-bank.com';
      if (passInput) passInput.value = 'admin123';
      showToast('Autofilled Admin credentials!');
    });
  }

  // Sign-Up auto-fill
  const fillSignUpBtn = document.getElementById('fillSignUp');
  if (fillSignUpBtn) {
    fillSignUpBtn.addEventListener('click', () => {
      const nameInput = document.getElementById('fullName');
      const emailInput = document.getElementById('email');
      const passInput = document.getElementById('password');
      const confirmInput = document.getElementById('confirmPassword');

      if (nameInput) nameInput.value = 'Alex Morgan';
      if (emailInput) emailInput.value = 'alex.morgan@fintech.io';
      if (passInput) passInput.value = 'SecurePass123!';
      if (confirmInput) confirmInput.value = 'SecurePass123!';
      showToast('Autofilled Sign-up form!');
    });
  }
}

/* Copy to Clipboard Helper */
function initCopyButtons() {
  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-copy') || '';
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showToast('Copied to clipboard!');
        }).catch(err => {
          console.error('Failed to copy text: ', err);
        });
      }
    });
  });
}

function copyApiKey(key) {
  if (!key) return;
  navigator.clipboard.writeText(key).then(() => {
    showToast('API Key copied to clipboard!');
  }).catch(() => {
    showToast('Failed to copy key.');
  });
}

function copyCodeSnippet(btn) {
  const cardEl = btn.closest('.card');
  const codeEl = cardEl ? cardEl.querySelector('pre') : null;
  if (codeEl) {
    const text = codeEl.innerText || codeEl.textContent;
    navigator.clipboard.writeText(text).then(() => {
      showToast('Code snippet copied!');
    }).catch(() => {
      showToast('Failed to copy code snippet.');
    });
  }
}

/* Toast Notifications */
function showToast(message, type = 'success') {
  let toastContainer = document.querySelector('.toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fas ${type === 'successs' ? 'fa-check-circle' : 'fa-circle-xmark'}" style="color: var(${type === 'success' ? '--primary' : '--danger'});"></i> <span>${message}</span>`;

  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
