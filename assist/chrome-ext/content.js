// Content script for Messenger Web
console.log('Messenger AI Assistant content script loaded');

// Detect Messenger Web page
if (window.location.hostname === 'www.messenger.com') {
  console.log('Messenger Web detected');
  
  // Notify background script that we're on Messenger
  chrome.runtime.sendMessage({
    type: 'MESSENGER_DETECTED',
    url: window.location.href
  });
  
  // Add visual indicator that extension is active
  const indicator = document.createElement('div');
  indicator.id = 'messenger-ai-indicator';
  indicator.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: #4CAF50;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    z-index: 10000;
    display: none;
  `;
  indicator.textContent = 'AI Assistant Active';
  document.body.appendChild(indicator);
  
  // Show indicator when extension is active
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'SHOW_INDICATOR') {
      indicator.style.display = 'block';
      setTimeout(() => {
        indicator.style.display = 'none';
      }, 3000);
    }
  });
}
