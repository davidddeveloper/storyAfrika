# Testing StoryAfrika API with Swagger UI

## Quick Start Guide

### Step 1: Access Swagger UI

Visit: `http://localhost:8000/api/docs/`

---

## Step 2: Register a New User (Get Tokens)

1. Find the **`POST /api/users/register/`** endpoint
2. Click "Try it out"
3. Enter the request body:
   ```json
   {
     "email": "yourname@example.com",
     "full_name": "Your Name",
     "password": "YourPassword123!",
     "password_confirm": "YourPassword123!"
   }
   ```
4. Click "Execute"
5. **Copy the `access` token** from the response (looks like `eyJhbGc...`)

**Response Example:**
```json
{
  "user": {
    "id": "uuid",
    "email": "yourname@example.com",
    "full_name": "Your Name",
    ...
  },
  "tokens": {
    "refresh": "eyJ...",
    "access": "eyJhbGc..."  ← COPY THIS
  }
}
```

---

## Step 3: Authorize in Swagger UI

1. Click the **"Authorize" button** (🔒 lock icon) at the top right
2. You'll see two authentication options:
   - **cookieAuth (apiKey)** - Leave this empty
   - **jwtAuth (http, Bearer)** - This is what you need
3. In the **jwtAuth** field, paste your access token (just the token, NOT "Bearer ...")
4. Click "Authorize"
5. Click "Close"

**Important:** Paste only the token string, Swagger will add "Bearer " automatically.

---

## Step 4: Test Authenticated Endpoints

Now you can test protected endpoints like:

### Get Current User
- **Endpoint:** `GET /api/users/me/`
- Click "Try it out" → "Execute"
- Should return your user profile

### Apply to Become a Writer
- **Endpoint:** `POST /api/writer-applications/`
- Request body:
  ```json
  {
    "writing_sample": "Your writing sample (300-500 words)...",
    "motivation": "Why you want to write for StoryAfrika..."
  }
  ```

### Bookmark a Story
- **Endpoint:** `POST /api/bookmarks/`
- Request body:
  ```json
  {
    "story": "story-uuid-from-GET-/api/stories/"
  }
  ```

---

## Step 5: Test Public Endpoints (No Auth)

These work without authorization:

### List Stories
- `GET /api/stories/`

### List Countries
- `GET /api/countries/`

### List Categories
- `GET /api/categories/`

### Search Stories
- `GET /api/stories/search/?q=keyword`

---

## Token Expiration

**Access tokens expire after 60 minutes.** If you get a 401 error after testing for a while:

### Option 1: Refresh Your Token
1. Use the **`POST /api/auth/token/refresh/`** endpoint
2. Request body:
   ```json
   {
     "refresh": "your-refresh-token"
   }
   ```
3. Copy the new `access` token
4. Click "Authorize" again and paste the new token

### Option 2: Re-register or Login
- Use **`POST /api/users/login/`** with your credentials
- Or register a new user

---

## Common Issues

### ❌ "Not authenticated" or 401 Error
- **Solution:** Make sure you clicked "Authorize" and pasted a valid access token

### ❌ "Given token not valid for any token type"
- **Solution:** Token might be expired (60 min limit). Get a new token via register/login

### ❌ "You do not have permission to perform this action"
- **Solution:** Some endpoints require writer status. Apply via `/api/writer-applications/` (requires admin approval)

---

## Testing Workflow Example

### Complete User Journey:

1. **Register** → Copy access token
2. **Authorize** → Paste token in Swagger
3. **Apply to Write** → Submit writer application
4. **(Admin approves application via Django admin)**
5. **Create Story** → `POST /api/stories/`
6. **Submit for Review** → `POST /api/stories/{slug}/submit/`
7. **(Editor reviews via Django admin)**
8. **(Story gets published)**
9. **Public sees story** → `GET /api/stories/`

---

## Quick Reference

| Endpoint | Auth Required | Purpose |
|----------|---------------|---------|
| `POST /api/users/register/` | No | Get JWT tokens |
| `POST /api/users/login/` | No | Login to get tokens |
| `GET /api/users/me/` | Yes | Current user profile |
| `POST /api/writer-applications/` | Yes | Apply to write |
| `GET /api/stories/` | No | List published stories |
| `POST /api/stories/` | Yes (Writer) | Create story |
| `GET /api/countries/` | No | List countries |
| `GET /api/categories/` | No | List categories |

---

## Django Admin Access

For approving writers and publishing stories:

1. Visit: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. You'll see: **"StoryAfrika Editorial Dashboard"**

Create a superuser if you haven't:
```bash
cd backend
python manage.py createsuperuser
```

---

**Happy Testing!** 🎉

For full API documentation, see: `backend/API_DOCUMENTATION.md`
