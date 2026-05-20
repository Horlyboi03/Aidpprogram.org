/**
 * AIDP Real-Time Chat — Socket.IO Client
 * Handles: connect, send, receive, online status, delivery & read receipts, image uploads
 */

let socket = null;
let currentUserId = null;
let recipientId = null;
let selectedImage = null;

/**
 * Initialize the chat socket connection.
 * @param {number} userId      - The currently logged-in user's ID
 * @param {number} targetId    - The recipient user's ID
 */
function initChat(userId, targetId) {
  currentUserId = userId;
  recipientId   = targetId;

  console.log('[AIDP Chat] Initializing chat...', { currentUserId, recipientId });

  // Check if Socket.IO library is loaded
  if (typeof io === 'undefined') {
    console.error('[AIDP Chat] Socket.IO library not loaded! Retrying...');
    let retryCount = 0;
    const maxRetries = 5;
    const retryInterval = setInterval(() => {
      retryCount++;
      if (typeof io !== 'undefined') {
        console.log('[AIDP Chat] Socket.IO loaded after retry, initializing...');
        clearInterval(retryInterval);
        initChat(userId, targetId);
      } else if (retryCount >= maxRetries) {
        clearInterval(retryInterval);
        console.error('[AIDP Chat] Socket.IO library failed to load after multiple retries.');
        alert('Chat system failed to load. Please refresh the page.');
      }
    }, 500);
    return;
  }

  // Always initialize socket, even without recipient
  // Connect to SocketIO server (use polling first, then upgrade to websocket)
  socket = io({ 
    transports: ['polling', 'websocket'],
    upgrade: true,
    rememberUpgrade: true
  });

  socket.on('connect', () => {
    console.log('[AIDP Chat] Connected:', socket.id);
  });

  socket.on('connect_error', (error) => {
    console.error('[AIDP Chat] Connection error:', error);
  });

  socket.on('disconnect', () => {
    console.log('[AIDP Chat] Disconnected');
  });

  // Only set up message handlers if we have a recipient
  if (recipientId) {
    // Receive incoming messages
    socket.on('receive_message', (data) => {
      console.log('[AIDP Chat] Message received:', data);
      // Only render if this message belongs to the current conversation
      if (
        (data.sender_id === currentUserId && data.recipient_id === recipientId) ||
        (data.sender_id === recipientId   && data.recipient_id === currentUserId)
      ) {
        appendMessage(data);
        scrollToBottom();
        
        // If we're the recipient, mark as delivered and read
        if (data.recipient_id === currentUserId) {
          socket.emit('message_delivered', { message_id: data.id });
          socket.emit('message_read', { message_id: data.id });
        }
      }
    });

    // Handle message status updates (delivery & read receipts)
    socket.on('message_status_update', (data) => {
      console.log('[AIDP Chat] Status update:', data);
      updateMessageStatus(data.message_id, data.is_delivered, data.is_read);
    });

    // Online/offline status updates
    socket.on('status', (data) => {
      console.log('[AIDP Chat] Status change:', data);
      if (data.user_id === recipientId) {
        updateOnlineStatus(data.online);
      }
    });

    // Mark all messages from recipient as read when chat opens
    socket.emit('mark_conversation_read', { sender_id: recipientId });

    // Scroll chat to top on load (shows oldest messages first)
    scrollToTop();
  }
}

/**
 * Handle image selection from file input.
 * @param {Event} event - File input change event
 */
function handleImageSelect(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('Please select an image file.');
    return;
  }

  // Validate file size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    alert('Image size must be less than 5MB.');
    return;
  }

  selectedImage = file;
  
  // Send image immediately
  sendImageMessage();
}

/**
 * Send an image message via SocketIO.
 */
function sendImageMessage() {
  if (!selectedImage) return;

  console.log('[AIDP Chat] Sending image:', selectedImage.name);
  console.log('[AIDP Chat] Socket state:', socket ? 'exists' : 'null', socket ? (socket.connected ? 'connected' : 'disconnected') : 'N/A');
  console.log('[AIDP Chat] Recipient ID:', recipientId);

  // Check socket connection first
  if (!socket) {
    console.error('[AIDP Chat] Socket not initialized!');
    alert('Chat connection not initialized. Please refresh the page.');
    selectedImage = null;
    document.getElementById('imageInput').value = '';
    return;
  }

  if (!socket.connected) {
    console.error('[AIDP Chat] Socket not connected! Waiting for connection...');
    // Wait a bit for connection
    setTimeout(() => {
      if (socket && socket.connected) {
        console.log('[AIDP Chat] Socket connected after wait, retrying...');
        sendImageMessage(); // Retry
      } else {
        alert('Connection lost. Please refresh the page and try again.');
        selectedImage = null;
        document.getElementById('imageInput').value = '';
      }
    }, 1000);
    return;
  }

  if (!recipientId || recipientId === 'null' || recipientId === null) {
    console.error('[AIDP Chat] No recipient ID!');
    alert('Error: No recipient selected. Please select a user first.');
    selectedImage = null;
    document.getElementById('imageInput').value = '';
    return;
  }

  const reader = new FileReader();
  reader.onload = function(e) {
    const imageData = e.target.result;
    
    console.log('[AIDP Chat] Emitting send_image event...');
    
    socket.emit('send_image', {
      recipient_id: recipientId,
      image_data: imageData,
      image_name: selectedImage.name,
      image_type: selectedImage.type
    }, (response) => {
      console.log('[AIDP Chat] Server acknowledged image:', response);
    });

    console.log('[AIDP Chat] Image sent successfully');
    
    // Clear selected image
    selectedImage = null;
    document.getElementById('imageInput').value = '';
  };

  reader.onerror = function(error) {
    console.error('[AIDP Chat] Error reading file:', error);
    alert('Error reading image file. Please try again.');
    selectedImage = null;
    document.getElementById('imageInput').value = '';
  };

  reader.readAsDataURL(selectedImage);
}

/**
 * Send a message via SocketIO.
 * @param {Event} event - Form submit event
 */
function sendMessage(event) {
  event.preventDefault();

  const input = document.getElementById('msgInput');
  const body  = input.value.trim();

  console.log('[AIDP Chat] Attempting to send message:', { body, recipientId, socketConnected: socket && socket.connected });

  if (!body) {
    console.warn('[AIDP Chat] Cannot send empty message');
    return;
  }

  if (!recipientId) {
    console.error('[AIDP Chat] No recipient ID!');
    alert('Error: No recipient selected. Please refresh the page.');
    return;
  }

  if (!socket) {
    console.error('[AIDP Chat] Socket not initialized!');
    alert('Chat connection not initialized. Please refresh the page.');
    return;
  }

  if (!socket.connected) {
    console.error('[AIDP Chat] Socket not connected!');
    alert('Connection lost. Please refresh the page and try again.');
    return;
  }

  console.log('[AIDP Chat] Sending message via socket...');
  
  socket.emit('send_message', {
    recipient_id: recipientId,
    body: body,
  }, (response) => {
    console.log('[AIDP Chat] Server acknowledged message:', response);
  });

  console.log('[AIDP Chat] Message emitted successfully');

  input.value = '';
  input.focus();
}

/**
 * Append a message bubble to the chat window.
 * @param {Object} msg - Message data object from server
 */
function appendMessage(msg) {
  console.log('[AIDP Chat] appendMessage called with:', msg);
  
  const container = document.getElementById('chatMessages');
  if (!container) {
    console.error('[AIDP Chat] chatMessages container not found!');
    return;
  }

  // Remove the "no messages yet" system message if present
  const sysMsg = container.querySelector('.chat-sys-msg');
  if (sysMsg) {
    console.log('[AIDP Chat] Removing system message');
    sysMsg.remove();
  }

  const isMine = msg.sender_id === currentUserId;
  console.log('[AIDP Chat] Message is mine:', isMine);
  
  const row = document.createElement('div');
  row.className = `msg-row ${isMine ? 'msg-mine' : 'msg-theirs'}`;
  row.setAttribute('data-message-id', msg.id);
  
  // Add sender name for received messages
  let senderNameHtml = '';
  if (!isMine && msg.sender_name) {
    senderNameHtml = `<p class="msg-sender-name">${escapeHtml(msg.sender_name)}</p>`;
  }
  
  // Handle image messages
  let contentHtml = '';
  if (msg.image_url) {
    contentHtml = `<img src="${escapeHtml(msg.image_url)}" alt="Shared image" class="msg-image" onclick="window.open('${escapeHtml(msg.image_url)}', '_blank')" />`;
  } else {
    contentHtml = `<p class="msg-text">${escapeHtml(msg.body)}</p>`;
  }
  
  // Status indicator for sent messages (one tick = delivered, two ticks = read)
  let statusHtml = '';
  if (isMine) {
    if (msg.is_read) {
      // Two ticks (read) - blue
      statusHtml = `
        <span class="msg-status-indicator read" title="Read">
          <svg class="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <svg class="status-icon status-icon-second" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </span>
      `;
    } else if (msg.is_delivered) {
      // One tick (delivered) - grey
      statusHtml = `
        <span class="msg-status-indicator delivered" title="Delivered">
          <svg class="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </span>
      `;
    } else {
      // Sending (clock icon)
      statusHtml = `
        <span class="msg-status-indicator sending" title="Sending">
          <svg class="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </span>
      `;
    }
  }

  row.innerHTML = `
    <div class="msg-bubble">
      ${senderNameHtml}
      ${contentHtml}
      <div class="msg-footer">
        <span class="msg-time">${msg.timestamp}</span>
        ${statusHtml}
      </div>
    </div>
  `;

  console.log('[AIDP Chat] Appending message to container');
  container.appendChild(row);

  // Animate in
  row.style.opacity = '0';
  row.style.transform = 'translateY(12px)';
  requestAnimationFrame(() => {
    row.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
    row.style.opacity = '1';
    row.style.transform = 'translateY(0)';
  });
  
  console.log('[AIDP Chat] Message appended successfully');
}

/**
 * Update message status indicator (delivery & read receipts).
 * @param {number} messageId
 * @param {boolean} isDelivered
 * @param {boolean} isRead
 */
function updateMessageStatus(messageId, isDelivered, isRead) {
  const msgRow = document.querySelector(`[data-message-id="${messageId}"]`);
  if (!msgRow) return;

  const statusIndicator = msgRow.querySelector('.msg-status-indicator');
  if (!statusIndicator) return;

  if (isRead) {
    // Two ticks (read) - blue color
    statusIndicator.className = 'msg-status-indicator read';
    statusIndicator.title = 'Read';
    statusIndicator.innerHTML = `
      <svg class="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
      <svg class="status-icon status-icon-second" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
    `;
  } else if (isDelivered) {
    // One tick (delivered) - grey color
    statusIndicator.className = 'msg-status-indicator delivered';
    statusIndicator.title = 'Delivered';
    statusIndicator.innerHTML = `
      <svg class="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
    `;
  }
}

/**
 * Scroll the chat messages container to the top.
 */
function scrollToTop() {
  const container = document.getElementById('chatMessages');
  if (container) {
    container.scrollTop = 0;
  }
}

/**
 * Scroll the chat messages container to the bottom.
 */
function scrollToBottom() {
  const container = document.getElementById('chatMessages');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

/**
 * Update the online status indicator in the UI.
 * @param {boolean} online
 */
function updateOnlineStatus(online) {
  // User-side chat
  const statusEl = document.getElementById('adminStatus');
  if (statusEl) {
    statusEl.className = online ? 'chat-admin-status online-status' : 'chat-admin-status offline-status';
    statusEl.innerHTML = `
      <span class="status-dot"></span>
      ${online ? 'Online' : 'Offline'}
    `;
  }

  // Admin-side chat
  const adminStatusEl = document.getElementById('userOnlineStatus');
  if (adminStatusEl) {
    adminStatusEl.textContent = online ? '● Online' : '○ Offline';
    adminStatusEl.style.color = online ? '#22c55e' : '#6b7280';
  }

  // Online dot indicator
  const dot = document.querySelector('.online-dot');
  if (dot) {
    dot.classList.toggle('online', online);
    dot.classList.toggle('offline', !online);
  }
}

/**
 * Escape HTML to prevent XSS in chat messages.
 * @param {string} str
 * @returns {string}
 */
function escapeHtml(str) {
  const map = { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#x27;' };
  return String(str).replace(/[&<>"']/g, c => map[c]);
}
