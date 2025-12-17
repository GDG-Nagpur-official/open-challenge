onst STORAGE_KEYS = { USER: 'gdg_user', PREFS: 'gdg_prefs' };

function defaultUser() {
  return {
    name: 'Jane Doe',
    email: 'jane@example.com',
    bio: 'API developer',
    avatar: ''
  };
}

function defaultPrefs() {
  return { 
    darkMode: false, 
    emailNotif: true, 
    itemsPerPage: 10,
    rateLimitEnabled: true,
    requestsPerMinute: 120,
    maxConnections: 50,
    analyticsEnabled: true,
    performanceMetrics: true,
    userBehavior: false,
    dataRetention: 90
  };
}

function loadUser() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.USER);
    return raw ? JSON.parse(raw) : defaultUser();
  } catch {
    return defaultUser();
  }
}

function saveUser(u) {
  localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(u));
}

function loadPrefs() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.PREFS);
    return raw ? JSON.parse(raw) : defaultPrefs();
  } catch {
    return defaultPrefs();
  }
}

function savePrefs(p) {
  localStorage.setItem(STORAGE_KEYS.PREFS, JSON.stringify(p));
  applyTheme(p.darkMode);
}

function applyTheme(isDark) {
  document.body.classList.toggle('dark', !!isDark);
}

document.addEventListener('DOMContentLoaded', () => {
  applyTheme(loadPrefs().darkMode);

  const displayName = document.getElementById('displayName');
  if (displayName) {
    const user = loadUser();
    const displayEmail = document.getElementById('displayEmail');
    const displayBio = document.getElementById('displayBio');
    const avatar = document.getElementById('avatar');
    const editBtn = document.getElementById('editBtn');
    const editForm = document.getElementById('editForm');

    const nameInput = document.getElementById('nameInput');
    const emailInput = document.getElementById('emailInput');
    const bioInput = document.getElementById('bioInput');
    const avatarInput = document.getElementById('avatarInput');
    const saveProfile = document.getElementById('saveProfile');
    const cancelEdit = document.getElementById('cancelEdit');

    function renderProfile() {
      displayName.textContent = user.name;
      displayEmail.textContent = user.email;
      displayBio.textContent = user.bio;
      avatar.src = user.avatar || 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80"><rect width="100%" height="100%" fill="%23ddd"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="18" fill="%23777">Avatar</text></svg>';
    }

    editBtn.addEventListener('click', () => {
      editForm.classList.remove('hidden');
      nameInput.value = user.name;
      emailInput.value = user.email;
      bioInput.value = user.bio;
      avatarInput.value = user.avatar || '';
    });

    cancelEdit.addEventListener('click', () => {
      editForm.classList.add('hidden');
    });

    saveProfile.addEventListener('click', () => {
      user.name = nameInput.value || user.name;
      user.email = emailInput.value || user.email;
      user.bio = bioInput.value || '';
      user.avatar = avatarInput.value || '';
      saveUser(user);
      renderProfile();
      editForm.classList.add('hidden');
    });

    renderProfile();
  }

  const settingsForm = document.getElementById('settingsForm');
  if (settingsForm) {
    const prefs = loadPrefs();
    const darkMode = document.getElementById('darkMode');
    const emailNotif = document.getElementById('emailNotif');
    const itemsPerPage = document.getElementById('itemsPerPage');

    const rateLimitEnabled = document.getElementById('rateLimitEnabled');
    const requestsPerMinute = document.getElementById('requestsPerMinute');
    const maxConnections = document.getElementById('maxConnections');
  
    const analyticsEnabled = document.getElementById('analyticsEnabled');
    const performanceMetrics = document.getElementById('performanceMetrics');
    const userBehavior = document.getElementById('userBehavior');
    const dataRetention = document.getElementById('dataRetention');
    
    const saveSettings = document.getElementById('saveSettings');
    const settingsMsg = document.getElementById('settingsMsg');

    darkMode.checked = !!prefs.darkMode;
    emailNotif.checked = !!prefs.emailNotif;
    itemsPerPage.value = prefs.itemsPerPage || 10;
    rateLimitEnabled.checked = !!prefs.rateLimitEnabled;
    requestsPerMinute.value = prefs.requestsPerMinute || 120;
    maxConnections.value = prefs.maxConnections || 50;
    analyticsEnabled.checked = !!prefs.analyticsEnabled;
    performanceMetrics.checked = !!prefs.performanceMetrics;
    userBehavior.checked = !!prefs.userBehavior;
    dataRetention.value = prefs.dataRetention || 90;


    function updateAnalyticsUI() {
      const enabled = analyticsEnabled.checked;
      performanceMetrics.disabled = !enabled;
      userBehavior.disabled = !enabled;
      dataRetention.disabled = !enabled;
    }

  
    function updateRateLimitUI() {
      const enabled = rateLimitEnabled.checked;
      requestsPerMinute.disabled = !enabled;
    }

    updateAnalyticsUI();
    updateRateLimitUI();

    analyticsEnabled.addEventListener('change', updateAnalyticsUI);
    rateLimitEnabled.addEventListener('change', updateRateLimitUI);

    saveSettings.addEventListener('click', () => {
      const newPrefs = {
        darkMode: !!darkMode.checked,
        emailNotif: !!emailNotif.checked,
        itemsPerPage: Number(itemsPerPage.value) || 10,
        rateLimitEnabled: !!rateLimitEnabled.checked,
        requestsPerMinute: Number(requestsPerMinute.value) || 120,
        maxConnections: Number(maxConnections.value) || 50,
        analyticsEnabled: !!analyticsEnabled.checked,
        performanceMetrics: !!performanceMetrics.checked,
        userBehavior: !!userBehavior.checked,
        dataRetention: Number(dataRetention.value) || 90
      };
      savePrefs(newPrefs);
      settingsMsg.textContent = 'Settings saved successfully!';
      setTimeout(() => settingsMsg.textContent = '', 1500);
    });
  }
});
