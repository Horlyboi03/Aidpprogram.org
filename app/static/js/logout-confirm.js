/**
 * Modern Logout Confirmation Modal
 */

// Create and inject modal HTML
function createLogoutModal() {
  const modalHTML = `
    <div id="logoutModal" class="logout-modal-overlay" style="display: none;">
      <div class="logout-modal">
        <div class="logout-modal-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </div>
        <h3 class="logout-modal-title">Confirm Logout</h3>
        <p class="logout-modal-text">Are you sure you want to logout? You'll need to sign in again to access your account.</p>
        <div class="logout-modal-actions">
          <button class="logout-modal-btn logout-modal-cancel" onclick="closeLogoutModal()">Cancel</button>
          <button class="logout-modal-btn logout-modal-confirm" onclick="confirmLogout()">Logout</button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
}

let logoutUrl = '';

function showLogoutModal(url) {
  logoutUrl = url;
  const modal = document.getElementById('logoutModal');
  if (modal) {
    modal.style.display = 'flex';
    // Animate in
    setTimeout(() => {
      modal.classList.add('active');
    }, 10);
  }
}

function closeLogoutModal() {
  const modal = document.getElementById('logoutModal');
  if (modal) {
    modal.classList.remove('active');
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  }
}

function confirmLogout() {
  if (logoutUrl) {
    window.location.href = logoutUrl;
  }
}

// Initialize modal on page load
document.addEventListener('DOMContentLoaded', () => {
  createLogoutModal();
  
  // Attach to all logout links
  const logoutLinks = document.querySelectorAll('a[href*="logout"]');
  if (logoutLinks.length > 0) {
    logoutLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        showLogoutModal(link.href);
      });
    });
  }
  
  // Close modal on overlay click
  const modal = document.getElementById('logoutModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target.id === 'logoutModal') {
        closeLogoutModal();
      }
    });
  }
  
  // Close modal on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeLogoutModal();
    }
  });
});
