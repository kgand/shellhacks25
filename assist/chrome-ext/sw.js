// Service Worker for Messenger AI Assistant
chrome.action.onClicked.addListener(async (tab) => {
  // Open side panel when extension icon is clicked
  await chrome.sidePanel.open({ tabId: tab.id });
  await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});

// Handle messages from side panel
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'CREATE_OFFSCREEN') {
    createOffscreenDocument();
    sendResponse({ success: true });
  } else if (message.type === 'START_CAPTURE') {
    // Forward to offscreen document
    chrome.runtime.sendMessage(message);
    sendResponse({ success: true });
  } else if (message.type === 'STOP_CAPTURE') {
    // Forward to offscreen document
    chrome.runtime.sendMessage(message);
    sendResponse({ success: true });
  }
});

// Create offscreen document for MediaRecorder
async function createOffscreenDocument() {
  try {
    // Check if offscreen document already exists
    const existingContexts = await chrome.runtime.getContexts({
      contextTypes: ['OFFSCREEN_DOCUMENT']
    });
    
    if (existingContexts.length === 0) {
      await chrome.offscreen.createDocument({
        reasons: ['USER_MEDIA'],
        justification: 'A/V capture & encoding for Messenger conversations',
        url: 'offscreen.html'
      });
    }
  } catch (error) {
    console.error('Failed to create offscreen document:', error);
  }
}

// Handle tab updates to ensure we're on Messenger
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url?.includes('messenger.com')) {
    // Enable side panel for Messenger tabs
    chrome.sidePanel.setOptions({
      tabId: tabId,
      path: 'ui/sidepanel.html',
      enabled: true
    });
  }
});
