const API_URL = "http://localhost:5000/api"
const token = localStorage.getItem("token")
let currentPage = 1
let currentCategory = null
let currentSearch = null
let currentPostId = null
const { bootstrap } = window

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  if (!token) {
    window.location.href = "/login"
    return
  }

  loadFeed()
  checkUnreadNotifications()
  setInterval(checkUnreadNotifications, 30000) // Check every 30s
})

async function loadFeed(page = 1) {
  try {
    let url = `${API_URL}/users/feed?page=${page}&per_page=5`

    if (currentCategory) {
      url += `&category=${currentCategory}`
    }

    if (currentSearch) {
      url += `&search=${currentSearch}`
    }

    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { posts, pages } = await response.json()
    currentPage = page

    displayFeed(posts)
    displayPagination(pages, page)
  } catch (error) {
    console.error("Error loading feed:", error)
  }
}

function displayFeed(posts) {
  const feed = document.getElementById("newsFeed")

  if (posts.length === 0) {
    feed.innerHTML = '<div class="alert alert-info">No posts available</div>'
    return
  }

  feed.innerHTML = posts
    .map(
      ({ id, image_url, title, content, author, created_at, category, view_count, is_liked, likes_count, comments_count }) => `
        <div class="card mb-4 post-card">
            ${image_url ? `<img src="${image_url}" class="card-img-top" alt="Post image">` : ""}
            <div class="card-body">
                <h5 class="card-title">${title}</h5>
                <p class="card-text">${content}</p>
                <small class="text-muted">By ${author} | ${new Date(created_at).toLocaleDateString()}</small>
                <div class="mt-3 d-flex gap-3">
                    <span class="badge bg-info">${category}</span>
                    <span class="badge bg-secondary">${view_count} views</span>
                </div>
                <div class="mt-3 d-flex gap-2">
                    <button class="btn btn-sm btn-outline-primary" onclick="likePost(${id}, this)">
                        <i class="bi ${is_liked ? "bi-heart-fill" : "bi-heart"}"></i> ${likes_count}
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="openPostDetail(${id})">
                        <i class="bi bi-chat"></i> ${comments_count}
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="copyPostLink(${id})">
                        <i class="bi bi-share"></i> Share
                    </button>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

function displayPagination(totalPages, currentPage) {
  const pagination = document.getElementById("pagination")
  pagination.innerHTML = ""

  if (currentPage > 1) {
    pagination.innerHTML += `<li class="page-item"><a class="page-link" href="#" onclick="loadFeed(${currentPage - 1})">Previous</a></li>`
  }

  for (let i = 1; i <= totalPages; i++) {
    pagination.innerHTML += `
            <li class="page-item ${i === currentPage ? "active" : ""}">
                <a class="page-link" href="#" onclick="loadFeed(${i})">${i}</a>
            </li>
        `
  }

  if (currentPage < totalPages) {
    pagination.innerHTML += `<li class="page-item"><a class="page-link" href="#" onclick="loadFeed(${currentPage + 1})">Next</a></li>`
  }
}

function filterByCategory(category) {
  currentCategory = category
  currentPage = 1
  loadFeed()
}

function searchNews() {
  currentSearch = document.getElementById("searchInput").value
  currentPage = 1
  loadFeed()
}

async function likePost(postId, button) {
  try {
    // First check current like status from the API
    const postResponse = await fetch(`${API_URL}/posts/${postId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!postResponse.ok) {
      alert("Failed to load post details")
      return
    }

    const postData = await postResponse.json()
    const isCurrentlyLiked = postData.is_liked
    const url = isCurrentlyLiked ? `${API_URL}/posts/${postId}/unlike` : `${API_URL}/posts/${postId}/like`

    const response = await fetch(url, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.ok) {
      const { likes_count } = await response.json()
      button.innerHTML = `<i class="bi ${isCurrentlyLiked ? "bi-heart" : "bi-heart-fill"}"></i> ${likes_count}`
    } else if (response.status === 404) {
      alert("Post not found")
    } else {
      alert("Failed to toggle like")
    }
  } catch (error) {
    console.error("Error:", error)
    alert("Failed to toggle like")
  }
}

async function openPostDetail(postId) {
  currentPostId = postId

  try {
    const response = await fetch(`${API_URL}/posts/${postId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { title, content, author, created_at, likes_count, image_url, is_liked, comments } = await response.json()

    document.getElementById("postTitle").textContent = title
    document.getElementById("postContent").textContent = content
    document.getElementById("postAuthor").textContent = author
    document.getElementById("postDate").textContent = new Date(created_at).toLocaleDateString()
    document.getElementById("likeCount").textContent = likes_count

    if (image_url) {
      document.getElementById("postImage").src = image_url
      document.getElementById("postImage").style.display = "block"
    } else {
      document.getElementById("postImage").style.display = "none"
    }

    // Update like button
    const likeBtn = document.getElementById("likeBtn")
    likeBtn.innerHTML = `<i class="bi ${is_liked ? "bi-heart-fill" : "bi-heart"}"></i> Like (${likes_count})`

    // Load comments
    const commentsList = document.getElementById("commentsList")
    commentsList.innerHTML = comments
      .map(
        ({ author, content, created_at }) => `
            <div class="comment-item mb-2">
                <strong>${author}</strong>
                <p class="mb-0">${content}</p>
                <small class="text-muted">${new Date(created_at).toLocaleDateString()}</small>
            </div>
        `,
      )
      .join("")

    const modalElement = document.getElementById("postDetailModal")
    const modal = new bootstrap.Modal(modalElement)

    // Store the currently focused element to restore focus later
    const previouslyFocusedElement = document.activeElement

    modal.show()

    // Restore focus when modal is hidden
    modalElement.addEventListener('hidden.bs.modal', function() {
      if (previouslyFocusedElement && previouslyFocusedElement.focus) {
        previouslyFocusedElement.focus()
      }
    }, { once: true })
  } catch (error) {
    console.error("Error:", error)
  }
}

async function toggleLike() {
  try {
    // First check current like status from the API
    const postResponse = await fetch(`${API_URL}/posts/${currentPostId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!postResponse.ok) {
      alert("Failed to load post details")
      return
    }

    const postData = await postResponse.json()
    const isCurrentlyLiked = postData.is_liked
    const url = isCurrentlyLiked ? `${API_URL}/posts/${currentPostId}/unlike` : `${API_URL}/posts/${currentPostId}/like`

    const response = await fetch(url, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.ok) {
      const { likes_count } = await response.json()
      const likeBtn = document.getElementById("likeBtn")
      likeBtn.innerHTML = `<i class="bi ${isCurrentlyLiked ? "bi-heart" : "bi-heart-fill"}"></i> Like (${likes_count})`
      document.getElementById("likeCount").textContent = likes_count
    } else if (response.status === 404) {
      alert("Post not found")
    } else {
      alert("Failed to toggle like")
    }
  } catch (error) {
    console.error("Error:", error)
    alert("Failed to toggle like")
  }
}

async function addComment() {
  const content = document.getElementById("commentInput").value

  if (!content.trim()) return

  try {
    const response = await fetch(`${API_URL}/posts/${currentPostId}/comments`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content }),
    })

    if (response.ok) {
      document.getElementById("commentInput").value = ""
      openPostDetail(currentPostId) // Refresh comments
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

function sharePost() {
  copyPostLink(currentPostId)
}

function copyPostLink(postId) {
  const url = `${window.location.origin}/posts/${postId}`
  navigator.clipboard.writeText(url).then(() => {
    alert("Link copied to clipboard!")
  }).catch((error) => {
    console.error("Failed to copy link:", error)
    alert("Failed to copy link to clipboard.")
  })
}

async function checkUnreadNotifications() {
  try {
    const response = await fetch(`${API_URL}/users/unread-count`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { unread_count } = await response.json()

    const badge = document.getElementById("notificationBadge")
    const countEl = document.getElementById("unreadCount")

    if (unread_count > 0) {
      badge.style.display = "inline-block"
      countEl.textContent = unread_count
    } else {
      badge.style.display = "none"
      countEl.textContent = ""
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function loadNotifications() {
  try {
    const response = await fetch(`${API_URL}/users/notifications`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { notifications } = await response.json()

    const dropdown = document.getElementById("notificationDropdown")
    const list = document.getElementById("notificationsList")

    if (dropdown.style.display === "none" || dropdown.style.display === "") {
      dropdown.style.display = "block"

      list.innerHTML =
        notifications
          .map(
            ({ message, created_at }) => `
                <div class="notification-item p-2 border-bottom">
                    <p class="mb-1">${message}</p>
                    <small class="text-muted">${new Date(created_at).toLocaleDateString()}</small>
                </div>
            `,
          )
          .join("") || '<div class="p-2">No notifications</div>'
    } else {
      dropdown.style.display = "none"
    }
  } catch (error) {
    console.error("Error:", error)
  }
}

async function showProfile() {
  try {
    const response = await fetch(`${API_URL}/auth/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const { name, email, created_at } = await response.json()

    document.getElementById("profileContent").innerHTML = `
            <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" class="form-control" value="${name}" disabled>
            </div>
            <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" value="${email}" disabled>
            </div>
            <div class="mb-3">
                <label class="form-label">Joined</label>
                <input type="text" class="form-control" value="${new Date(created_at).toLocaleDateString()}" disabled>
            </div>
            <button class="btn btn-primary" onclick="editProfile()">Edit Profile</button>
            <button class="btn btn-secondary" onclick="changePassword()">Change Password</button>
        `

    new bootstrap.Modal(document.getElementById("profileModal")).show()
  } catch (error) {
    console.error("Error:", error)
  }
}

function editProfile() {
  alert("Profile edit functionality coming soon")
}

function changePassword() {
  alert("Change password functionality coming soon")
}

async function logout() {
  try {
    const response = await fetch(`${API_URL}/auth/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      credentials: 'include'
    })
  } catch (error) {
    console.error('Logout error:', error);
  }

  // Clear session and redirect
  sessionStorage.clear();
  localStorage.clear();
  window.location.href = "/logout";
}
