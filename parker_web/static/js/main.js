document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chatContainer");
  const userInput = document.getElementById("userInput");
  const micButton = document.getElementById("micButton");
  const sendButton = document.getElementById("sendButton");

  // Test speech synthesis
  const testSpeech = new SpeechSynthesisUtterance("Test");
  window.speechSynthesis.speak(testSpeech);

  let isListening = false;
  let recognition;
  let conversationActive = false;

  if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      userInput.value = text;
      sendMessage();
    };

    recognition.onend = () => {
      micButton.style.backgroundColor = "";
      isListening = false;
      updateVoiceWave(false);
    };
  }

  function addMessage(text, isUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${
      isUser ? "user-message" : "assistant-message"
    }`;
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    if (!conversationActive && !isUser) {
      conversationActive = true;
    }
  }

  async function sendMessage() {
    const text = userInput.value.trim();
    if (text) {
      addMessage(text, true);
      userInput.value = "";
      userInput.disabled = true;

      try {
        const response = await fetch("/process_command", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            command: text,
            contextRequired: true, // Always send context requirement
          }),
        });

        const data = await response.json();

        if (data.response) {
          addMessage(data.response);
        }

        // Handle actions based on response
        if (data.action) {
          switch (data.action) {
            case "music":
              console.log("Music playback initiated");
              break;
            case "search":
              console.log("Web search initiated");
              break;
            case "browser":
              console.log("Website opening initiated");
              break;
          }
        }

        if (data.status === "error") {
          console.error("Server reported an error:", data.response);
        }
      } catch (error) {
        console.error("Error:", error);
        addMessage("Sorry, I encountered an error processing your request.");
      } finally {
        userInput.disabled = false; // Re-enable input
        userInput.focus();
      }
    }
  }

  micButton.addEventListener("click", () => {
    if (recognition) {
      if (!isListening) {
        recognition.start();
        micButton.style.backgroundColor = "#ff4444";
        isListening = true;
        updateVoiceWave(true);
      } else {
        recognition.stop();
        micButton.style.backgroundColor = "";
        isListening = false;
        updateVoiceWave(false);
      }
    } else {
      alert("Speech recognition is not supported in your browser.");
    }
  });

  sendButton.addEventListener("click", sendMessage);

  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // Add feature buttons for random content
  document.querySelectorAll(".feature-item").forEach((item) => {
    item.addEventListener("click", () => {
      const command = item.dataset.command;
      switch (command) {
        case "search":
          userInput.value = "search ";
          break;
        case "music":
          userInput.value = "play ";
          break;
        case "weather":
          userInput.value = "weather in ";
          break;
        case "chat":
          userInput.value = "tell me a joke"; // Example of random content
          break;
      }
      userInput.focus();
    });
  });

  // Add clear history button
  const clearButton = document.createElement("button");
  clearButton.className = "clear-button";
  clearButton.innerHTML = '<span class="material-icons">delete</span>';
  clearButton.title = "Clear conversation history";
  document.querySelector(".input-container").appendChild(clearButton);

  clearButton.addEventListener("click", async () => {
    try {
      await fetch("/clear_history", { method: "POST" });
      chatContainer.innerHTML = `
        <div class="welcome-message assistant-message">
          <p>Hi! I am Parker, your AI assistant. How can I help you today?</p>
        </div>
      `;
      conversationActive = false;
    } catch (error) {
      console.error("Error clearing history:", error);
    }
  });

  // Theme toggle functionality
  const themeToggle = document.getElementById("themeToggle");
  const themeIcon = themeToggle.querySelector(".material-icons");

  // Check for saved theme preference or default to light
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  themeIcon.textContent = savedTheme === "dark" ? "light_mode" : "dark_mode";

  themeToggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    themeIcon.textContent = newTheme === "dark" ? "light_mode" : "dark_mode";
  });

  // Add voice settings functionality
  const settingsPanel = document.getElementById("settingsPanel");
  const settingsToggle = document.getElementById("settingsToggle");
  const closeSettings = document.getElementById("closeSettings");
  const voiceSelect = document.getElementById("voiceSelect");
  const voiceSpeed = document.getElementById("voiceSpeed");
  const voicePitch = document.getElementById("voicePitch");
  const voiceWave = document.getElementById("voiceWave");

  // Initialize voice settings
  function initVoiceSettings() {
    window.speechSynthesis.getVoices().forEach((voice) => {
      const option = document.createElement("option");
      option.value = voice.name;
      option.textContent = `${voice.name} (${voice.lang})`;
      voiceSelect.appendChild(option);
    });
  }

  // Voice settings event listeners
  settingsToggle.addEventListener("click", () => {
    settingsPanel.classList.toggle("active");
  });

  closeSettings.addEventListener("click", () => {
    settingsPanel.classList.remove("active");
  });

  // Update voice settings
  voiceSelect.addEventListener("change", updateVoiceSettings);
  voiceSpeed.addEventListener("input", updateVoiceSettings);
  voicePitch.addEventListener("input", updateVoiceSettings);

  function updateVoiceSettings() {
    const settings = {
      voice: voiceSelect.value,
      rate: voiceSpeed.value,
      pitch: voicePitch.value,
    };
    localStorage.setItem("voiceSettings", JSON.stringify(settings));
  }

  // Command suggestions
  const commonCommands = [
    "Tell me a joke",
    "What's the weather like",
    "Play some music",
    "Search the web",
    "Tell me about yourself",
  ];

  function showSuggestions() {
    const suggestionsDiv = document.getElementById("commandSuggestions");
    suggestionsDiv.innerHTML = "";

    commonCommands.forEach((cmd) => {
      const suggestion = document.createElement("button");
      suggestion.className = "suggestion-btn";
      suggestion.textContent = cmd;
      suggestion.onclick = () => {
        userInput.value = cmd;
        sendMessage();
      };
      suggestionsDiv.appendChild(suggestion);
    });
  }

  // Add keyboard shortcuts
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "V") {
      e.preventDefault();
      micButton.click();
    }

    if ((e.ctrlKey || e.metaKey) && e.key === "/") {
      e.preventDefault();
      userInput.focus();
    }
  });

  // Update voice wave animation
  function updateVoiceWave(active) {
    voiceWave.classList.toggle("active", active);
  }

  // Initialize voice settings when voices are available
  if (typeof speechSynthesis !== "undefined") {
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = initVoiceSettings;
    }
    initVoiceSettings();
  }

  // Show initial suggestions
  showSuggestions();
});
