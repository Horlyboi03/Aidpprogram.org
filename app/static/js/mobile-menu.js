/**
 * Mobile Menu Toggle for Admin Sidebar
 * EXCLUDED FROM CHAT PAGES
 */

document.addEventListener('DOMContentLoaded', function() {
  // Don't create hamburger menu on chat pages
  const isChatPage = document.querySelector('.admin-chat-layout') || 
                     document.querySelector('.chat-layout') ||
                     window.location.pathname.includes('/chat');
  
  if (isChatPage) {
    console.log('[Mobile Menu] Chat page detected - skipping hamburger menu');
    return; // Exit early for chat pages
  }
  
  // Create mobile menu toggle button if it doesn't exist
  const adminSidebar = document.querySelector('.admin-sidebar');
  
  if (adminSidebar && window.innerWidth <= 1024) {
    // Check if toggle button already exists
    let toggleBtn = document.querySelector('.mobile-menu-toggle');
    
    if (!toggleBtn) {
      // Create toggle button
      toggleBtn = document.createElement('button');
      toggleBtn.className = 'mobile-menu-toggle';
      toggleBtn.setAttribute('aria-label', 'Toggle menu');
      toggleBtn.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      `;
      document.body.appendChild(toggleBtn);
    }
    
    // Toggle sidebar on button click
    toggleBtn.addEventListener('click', function() {
      adminSidebar.classList.toggle('active');
      
      // Update icon
      if (adminSidebar.classList.contains('active')) {
        toggleBtn.innerHTML = `
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        `;
      } else {
        toggleBtn.innerHTML = `
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        `;
      }
    });
    
    // Close sidebar when clicking outside
    document.addEventListener('click', function(e) {
      if (adminSidebar.classList.contains('active') && 
          !adminSidebar.contains(e.target) && 
          !toggleBtn.contains(e.target)) {
        adminSidebar.classList.remove('active');
        toggleBtn.innerHTML = `
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        `;
      }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
      if (window.innerWidth > 1024) {
        adminSidebar.classList.remove('active');
        if (toggleBtn) {
          toggleBtn.style.display = 'none';
        }
      } else {
        if (toggleBtn) {
          toggleBtn.style.display = 'flex';
        }
      }
    });
  }
});

/**
 * Mobile Navigation Toggle for User Pages
 */
document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.querySelector('.nav-menu');
  
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
      navToggle.classList.toggle('active');
      
      // Update aria-expanded
      const isExpanded = navMenu.classList.contains('active');
      navToggle.setAttribute('aria-expanded', isExpanded);
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    
    // Close menu when clicking a link
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
});
