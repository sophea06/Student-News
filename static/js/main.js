async function logout() {
  try {
    // Call the logout API to clear server-side session
    const response = await apiCall('/api/auth/logout', {
      method: 'POST'
    });

    if (response.ok) {
      // Clear client-side storage
      localStorage.removeItem("token")
      localStorage.removeItem("user")
      window.location.href = "/login"
    } else {
      console.error("Logout failed on server");
      // Still clear client-side and redirect
      localStorage.removeItem("token")
      localStorage.removeItem("user")
      window.location.href = "/login"
    }
  } catch (error) {
    console.error("Logout error:", error)
    // Fallback: clear client-side and redirect
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    window.location.href = "/login"
  }
}

function getCurrentUser() {
  const user = localStorage.getItem("user")
  return user ? JSON.parse(user) : null
}

function getAuthToken() {
  return localStorage.getItem("token")
}

function apiCall(url, options = {}) {
  const token = getAuthToken()
  const headers = options.headers || {}

  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  return fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
  })
}

document.addEventListener("DOMContentLoaded", async () => {
  const user = getCurrentUser()
  if (user) {
    const userNameElement = document.getElementById("user-name")
    if (userNameElement) {
      userNameElement.textContent = user.name
    }
  } else if (
    window.location.pathname !== "/login" &&
    window.location.pathname !== "/register" &&
    window.location.pathname !== "/"
  ) {
    window.location.href = "/login"
  }

  // Initialize Bootstrap dropdowns
  const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
  const dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl)
  })
})
