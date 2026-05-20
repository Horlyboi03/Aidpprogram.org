/**
 * Chat Polling Fallback
 * Fetches new messages every 3 seconds if Socket.IO fails
 */

let lastMessageId = 0;
let pollingInterval = null;

function startPolling() {
  // Get the last message ID currently displayed
  const messages = document.querySelectorAll('[data-message-id]');
  if (messages.length > 0) {
    const lastMsg = messages[messages.length - 1];
    lastMessageId = parseInt(lastMsg.getAttribute('data-message-id')) || 0;
  }
  
  console.log('[AIDP Chat] Starting polling fallback, last message ID:', lastMessageId);
  
  // Poll every 3 seconds
  pollingInterval = setInterval(fetchNewMessages, 3000);
}

function stopPolling() {
  if (pollingInterval) {
    clearInterval(pollingInterval);
    pollingInterval = null;
    console.log('[AIDP Chat] Stopped polling');
  }
}

async function fetchNewMessages() {
  if (!recipientId) return;
  
  try {
    const response = await fetch(`/chat/history/${recipientId}?after=${lastMessageId}`);
    if (!response.ok) return;
    
    const data = await response.json();
    
    if (data.messages && data.messages.length > 0) {
      console.log('[AIDP Chat] Fetched', data.messages.length, 'new messages');
      
      data.messages.forEach(msg => {
        // Check if message already exists
        if (!document.querySelector(`[data-message-id="${msg.id}"]`)) {
          appendMessage(msg);
          lastMessageId = Math.max(lastMessageId, msg.id);
        }
      });
      
      scrollToBottom();
    }
  } catch (error) {
    console.error('[AIDP Chat] Polling error:', error);
  }
}

// Start polling if Socket.IO fails to connect within 5 seconds
setTimeout(() => {
  if (!socket || !socket.connected) {
    console.warn('[AIDP Chat] Socket.IO not connected, using polling fallback');
    startPolling();
  }
}, 5000);

// Also start polling if socket disconnects
if (socket) {
  socket.on('disconnect', () => {
    console.warn('[AIDP Chat] Socket disconnected, switching to polling');
    startPolling();
  });
  
  socket.on('connect', () => {
    console.log('[AIDP Chat] Socket reconnected, stopping polling');
    stopPolling();
  });
}
