// Professional Admin Dashboard - Sidebar Toggle
document.addEventListener('DOMContentLoaded', function() {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('adminSidebar');
  const content = document.querySelector('.admin-content-pro');
  
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      if (window.innerWidth <= 768) {
        sidebar.classList.toggle('sidebar-active');
      } else {
        sidebar.classList.toggle('sidebar-collapsed');
        if (content) {
          content.classList.toggle('content-expanded');
        }
      }
    });
    
    document.addEventListener('click', function(event) {
      if (window.innerWidth <= 768) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = sidebarToggle.contains(event.target);
        
        if (!isClickInsideSidebar && !isClickOnToggle && sidebar.classList.contains('sidebar-active')) {
          sidebar.classList.remove('sidebar-active');
        }
      }
    });
  }
});
