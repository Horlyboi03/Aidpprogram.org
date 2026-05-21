// Professional Admin Dashboard - Sidebar Toggle
document.addEventListener('DOMContentLoaded', function() {
  const sidebarToggle = document.getElementById('premiumSidebarToggle');
  const sidebar = document.getElementById('premiumSidebar');
  const content = document.querySelector('.admin-content-pro');
  
  // Create sidebar overlay element
  let sidebarOverlay = document.getElementById('sidebarOverlay');
  if (!sidebarOverlay) {
    sidebarOverlay = document.createElement('div');
    sidebarOverlay.id = 'sidebarOverlay';
    sidebarOverlay.className = 'sidebar-overlay';
    document.body.appendChild(sidebarOverlay);
  }
  
  if (sidebarToggle && sidebar) {
    // Toggle sidebar on hamburger click
    sidebarToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      if (window.innerWidth <= 768) {
        sidebar.classList.toggle('sidebar-open');
        sidebarOverlay.classList.toggle('show');
      } else {
        sidebar.classList.toggle('sidebar-collapsed');
        if (content) {
          content.classList.toggle('content-expanded');
        }
      }
    });
    
    // Close sidebar when clicking overlay
    sidebarOverlay.addEventListener('click', function() {
      if (window.innerWidth <= 768) {
        sidebar.classList.remove('sidebar-open');
        sidebarOverlay.classList.remove('show');
      }
    });
    
    // Close sidebar when clicking outside (fallback)
    document.addEventListener('click', function(event) {
      if (window.innerWidth <= 768) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = sidebarToggle.contains(event.target);
        
        if (!isClickInsideSidebar && !isClickOnToggle && sidebar.classList.contains('sidebar-open')) {
          sidebar.classList.remove('sidebar-open');
          sidebarOverlay.classList.remove('show');
        }
      }
    });
  }
});
