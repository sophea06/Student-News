const API_URL = "http://localhost:5000/api"
const token = localStorage.getItem("token") || sessionStorage.getItem("token")
const { bootstrap } = window

// Initialize dashboard
document.addEventListener("DOMContentLoaded", () => {
  if (!token) {
    window.location.href = "/login"
    return
  }

  loadDashboardStats()
  loadPosts()
  loadUsers()
  loadAdminProfile()

  // Add event listeners for navigation links
  const navLinks = document.querySelectorAll('.nav-link[data-section]')
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault()
      const sectionId = link.getAttribute('data-section')
      showSection(sectionId, e)
    })
  })

  // Add event listener for logout link
  const logoutLink = document.getElementById('logout-link')
  if (logoutLink) {
    logoutLink.addEventListener('click', (e) => {
      e.preventDefault()
      logout()
    })
  }

  // Add event listener for create post button
  const createPostBtn = document.querySelector('.create-post-btn')
  if (createPostBtn) {
    createPostBtn.addEventListener('click', (e) => {
      showCreatePostModal(e.target)
    })
  }

  // Handle modal hide to prevent aria-hidden focus issues
  const modal = document.getElementById("createPostModal")
  modal.addEventListener('hidden.bs.modal', () => {
    if (modal.contains(document.activeElement)) {
      document.activeElement.blur()
    }
  })
})

function showSection(sectionId, event) {
  // Hide all sections
  document.querySelectorAll(".content-section").forEach((el) => {
    el.classList.add("d-none")
  })

  // Show selected section
  document.getElementById(sectionId).classList.remove("d-none")

  // Update nav links
  document.querySelectorAll(".nav-link").forEach((el) => {
    el.classList.remove("active")
  })
  event.target.closest(".nav-link").classList.add("active")
}

async function loadDashboardStats() {
  try {
    const response = await fetch(`${API_URL}/admin/dashboard/stats`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const data = await response.json()
    const { total_students, total_posts, total_comments, recent_posts } = data

    document.getElementById("totalStudents").textContent = total_students
    document.getElementById("totalPosts").textContent = total_posts
    document.getElementById("totalComments").textContent = total_comments

    // Load recent posts
    const tbody = document.getElementById("recentPostsTable")
    tbody.innerHTML = recent_posts
      .map(
        (post) => `
            <tr>
                <td>${post.title}</td>
                <td>${post.author}</td>
                <td>${post.likes}</td>
                <td>${post.comments}</td>
                <td>${new Date(post.created_at).toLocaleDateString()}</td>
            </tr>
        `,
      )
      .join("")
  } catch (error) {
    console.error("Error loading stats:", error)
  }
}

async function loadPosts() {
  try {
    const response = await fetch(`${API_URL}/posts`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { posts } = await response.json()
    const tbody = document.getElementById("postsTable")

    tbody.innerHTML = posts
      .map(
        (post) => `
          <tr>
            <td>${post.title}</td>
            <td>${post.category}</td>
            <td><span class="badge bg-info">${post.visibility}</span></td>
            <td>${post.likes_count}</td>
            <td>${post.comments_count}</td>
            <td>
              <div class="dropdown">
                <button class="btn btn-sm btn-light dropdown-toggle" type="button" id="postActions${post.id}" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="bi bi-three-dots-vertical"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="postActions${post.id}">
                  <li>
                    <a class="dropdown-item edit-post-btn" href="#" data-post-id="${post.id}">
                      <i class="bi bi-pencil-square me-2"></i>Edit
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item delete-post-btn" href="#" data-post-id="${post.id}">
                      <i class="bi bi-trash me-2"></i>Delete
                    </a>
                  </li>
                </ul>
              </div>
            </td>
          </tr>
        `
      )
      .join("")

    // Add event listeners for edit buttons
    tbody.querySelectorAll('.edit-post-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault()
        const postId = btn.getAttribute('data-post-id')
        editPost(postId)
      })
    })

    // Add event listeners for delete buttons
    tbody.querySelectorAll('.delete-post-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault()
        const postId = btn.getAttribute('data-post-id')
        deletePost(postId)
      })
    })
  } catch (error) {
    console.error("Error loading posts:", error)
  }
}


async function loadUsers() {
  try {
    const response = await fetch(`${API_URL}/admin/users`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { users } = await response.json()

    const tbody = document.getElementById("usersTable")
    tbody.innerHTML = users
      .map(
        (user) => `
            <tr>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.posts_count}</td>
                <td><span class="badge ${user.is_blocked ? "bg-danger" : "bg-success"}">${user.is_blocked ? "Blocked" : "Active"}</span></td>
                <td>
                    ${
                      user.is_blocked
                        ? `<button class="btn btn-sm btn-success unblock-user-btn" data-user-id="${user.id}">Unblock</button>`
                        : `<button class="btn btn-sm btn-warning block-user-btn" data-user-id="${user.id}">Block</button>`
                    }
                    <button class="btn btn-sm btn-info reset-pwd-btn" data-user-id="${user.id}">Reset PWD</button>
                </td>
            </tr>
        `,
      )
      .join("")

    // Add event listeners for block buttons
    tbody.querySelectorAll('.block-user-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const userId = btn.getAttribute('data-user-id')
        blockUser(userId)
      })
    })

    // Add event listeners for unblock buttons
    tbody.querySelectorAll('.unblock-user-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const userId = btn.getAttribute('data-user-id')
        unblockUser(userId)
      })
    })

    // Add event listeners for reset password buttons
    tbody.querySelectorAll('.reset-pwd-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const userId = btn.getAttribute('data-user-id')
        resetPassword(userId)
      })
    })
  } catch (error) {
    console.error("Error loading users:", error)
  }
}

function showCreatePostModal(button) {
  // Remove focus from the button to prevent aria-hidden issues
  if (button) button.blur()
  const modal = new bootstrap.Modal(document.getElementById("createPostModal"))
  modal.show()
}

async function createPost(event) {
  event.preventDefault()

  const { value: title } = document.getElementById("postTitle")
  const { value: content } = document.getElementById("postContent")
  const { value: category } = document.getElementById("postCategory")
  const { value: visibility } = document.getElementById("postVisibility")
  const { value: imageUrl } = document.getElementById("postImageUrl")
  const imageFile = document.getElementById("postImage").files[0]

  const formData = new FormData()
  formData.append('title', title)
  formData.append('content', content)
  formData.append('category', category)
  formData.append('visibility', visibility)
  if (imageUrl) {
    formData.append('image_url', imageUrl)
  }
  if (imageFile) {
    formData.append('image', imageFile)
  }

  try {
    const response = await fetch(`${API_URL}/posts`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    if (response.ok) {
      alert("Post created successfully")
      bootstrap.Modal.getInstance(document.getElementById("createPostModal")).hide()
      document.getElementById("createPostForm").reset()
      loadPosts()
    } else {
      alert("Error creating post")
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function editPost(postId) {
  try {
    const response = await fetch(`${API_URL}/posts/${postId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!response.ok) {
      throw new Error('Failed to load post')
    }

    const post = await response.json()

    // Populate form
    document.getElementById("postTitle").value = post.title
    document.getElementById("postContent").value = post.content
    document.getElementById("postCategory").value = post.category
    document.getElementById("postVisibility").value = post.visibility
    document.getElementById("postImageUrl").value = post.image_url || ""
    document.getElementById("postImage").value = "" // Clear file input

    // Change submit handler
    const form = document.getElementById("createPostForm")
    form.setAttribute("onsubmit", `updatePost(event, ${postId})`)

    // Change modal title
    document.querySelector("#createPostModal .modal-title").textContent = "Edit Post"

    // Change button text
    form.querySelector("button[type=submit]").textContent = "Update Post"

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById("createPostModal"))
    modal.show()
  } catch (error) {
    console.error("Error loading post:", error)
  }
}

async function updatePost(event, postId) {
  event.preventDefault()

  const { value: title } = document.getElementById("postTitle")
  const { value: content } = document.getElementById("postContent")
  const { value: category } = document.getElementById("postCategory")
  const { value: visibility } = document.getElementById("postVisibility")
  const { value: imageUrl } = document.getElementById("postImageUrl")
  const imageFile = document.getElementById("postImage").files[0]

  const formData = new FormData()
  formData.append('title', title)
  formData.append('content', content)
  formData.append('category', category)
  formData.append('visibility', visibility)
  if (imageUrl) {
    formData.append('image_url', imageUrl)
  }
  if (imageFile) {
    formData.append('image', imageFile)
  }

  try {
    const response = await fetch(`${API_URL}/posts/${postId}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    if (response.ok) {
      alert("Post updated successfully")
      bootstrap.Modal.getInstance(document.getElementById("createPostModal")).hide()
      document.getElementById("createPostForm").reset()

      // Reset form back to create
      const form = document.getElementById("createPostForm")
      form.setAttribute("onsubmit", "createPost(event)")
      document.querySelector("#createPostModal .modal-title").textContent = "Create New Post"
      form.querySelector("button[type=submit]").textContent = "Create Post"

      loadPosts()
    } else {
      alert("Error updating post")
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function deletePost(postId) {
  if (!confirm("Are you sure?")) return

  try {
    const response = await fetch(`${API_URL}/posts/${postId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.ok) {
      alert("Post deleted")
      loadPosts()
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function blockUser(userId) {
  try {
    const response = await fetch(`${API_URL}/admin/users/${userId}/block`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ reason: "Blocked by admin" })
    })

    if (response.ok) {
      loadUsers()
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function unblockUser(userId) {
  try {
    const response = await fetch(`${API_URL}/admin/users/${userId}/unblock`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({})
    })

    if (response.ok) {
      loadUsers()
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function resetPassword(userId) {
  try {
    const response = await fetch(`${API_URL}/admin/users/${userId}/reset-password`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}` },
    })

    const { temporary_password } = await response.json()
    alert(`New temporary password: ${temporary_password}`)
  } catch (error) {
    console.error("Error:", error)
  }
}

async function sendAnnouncement(event) {
  event.preventDefault()

  const { value: message } = document.getElementById("announcementMessage")

  const announcement = {
    message,
  }

  try {
    const response = await fetch(`${API_URL}/admin/send-announcement`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(announcement),
    })

    const { message: responseMessage } = await response.json()
    alert(responseMessage)
    document.getElementById("announcementMessage").value = ""
  } catch (error) {
    console.error("Error:", error)
  }
}

async function loadAdminProfile() {
  try {
    const response = await fetch(`${API_URL}/users/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.ok) {
      const user = await response.json()

      const nameEl = document.getElementById('admin-name')
      if (nameEl) nameEl.value = user.name

      const emailEl = document.getElementById('admin-email')
      if (emailEl) emailEl.value = user.email

      // Set profile picture
      const picEl = document.getElementById('admin-profile-picture')
      if (picEl && user.profile_picture) {
        picEl.src = user.profile_picture
      }
    }
  } catch (error) {
    console.error('Error loading admin profile:', error)
  }
}

// Handle admin profile picture upload
document.getElementById('admin-profile-picture-input')?.addEventListener('change', async (e) => {
  const file = e.target.files[0]
  if (!file) return

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    alert('Please select a valid image file (JPG, PNG, GIF)')
    return
  }

  // Validate file size (5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('Image file too large (max 5MB)')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await fetch(`${API_URL}/uploads/profile-picture`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData
    })

    if (response.ok) {
      const result = await response.json()
      document.getElementById('admin-profile-picture').src = result.profile_picture
      alert('Profile picture updated successfully')
    } else {
      const error = await response.json()
      alert(error.error || 'Failed to upload profile picture')
    }
  } catch (error) {
    console.error('Error uploading profile picture:', error)
    alert('Failed to upload profile picture')
  }
})

// Handle admin profile form submission
document.getElementById('admin-profile-form')?.addEventListener('submit', async (e) => {
  e.preventDefault()

  const updateData = {
    name: document.getElementById('admin-name').value
  }

  if (document.getElementById('admin-password').value) {
    updateData.password = document.getElementById('admin-password').value
  }

  try {
    const response = await fetch(`${API_URL}/users/update-profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(updateData)
    })

    if (response.ok) {
      alert('Profile updated successfully')
    } else {
      alert('Failed to update profile')
    }
  } catch (error) {
    console.error('Error updating profile:', error)
    alert('Failed to update profile')
  }
})

function logout() {
  // Clear all storage
  localStorage.removeItem("token")
  sessionStorage.removeItem("token")
  // Clear session cookie
  document.cookie = "session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
  // Redirect to server logout endpoint which clears server session
  window.location.href = "/logout"
}
