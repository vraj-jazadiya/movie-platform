# 🧪 Frontend Testing Guide

## Complete Testing Checklist for Movie Platform

This guide provides a comprehensive testing checklist to verify all frontend functionality.

---

## 🚀 Pre-Testing Setup

### 1. Ensure Both Servers Are Running
```bash
# Terminal 1 - Backend
cd movie-platform/backend
python app.py
# Should see: Running on http://localhost:5000

# Terminal 2 - Frontend
cd movie-platform/frontend
npm run dev
# Should see: Local: http://localhost:3000
```

### 2. Open Browser
Navigate to: **http://localhost:3000**

---

## ✅ Testing Checklist

### 1. Home Page Testing

#### Visual Elements
- [ ] Page loads without errors
- [ ] Hero section displays with gradient background
- [ ] "Movie Platform" title is visible with neon green gradient
- [ ] Search bar is centered and functional
- [ ] Production houses grid displays correctly
- [ ] All 37 production house cards are visible
- [ ] Icons display for each production house
- [ ] Features section shows at bottom

#### Interactions
- [ ] Hover over production house cards shows glow effect
- [ ] Cards lift up on hover (translateY animation)
- [ ] Search input focuses with green border glow
- [ ] Search button is clickable
- [ ] Navbar links are clickable
- [ ] Smooth scrolling works

#### Responsive Design
- [ ] Layout adjusts on mobile (< 768px)
- [ ] Grid changes to 2 columns on tablet
- [ ] Grid changes to 1 column on mobile
- [ ] Text sizes adjust appropriately

---

### 2. Navigation Bar Testing

#### Visual Elements
- [ ] Navbar is sticky at top
- [ ] Logo displays on left
- [ ] Menu items centered (Home, News, Chat, Contact)
- [ ] Login/Register buttons on right (when logged out)
- [ ] User greeting and Logout button (when logged in)
- [ ] Admin link visible for admin users

#### Interactions
- [ ] Click "Home" navigates to /
- [ ] Click "News" navigates to /news
- [ ] Click "Chat" navigates to /chat (requires login)
- [ ] Click "Contact" navigates to /contact
- [ ] Click "Profile" navigates to /profile (requires login)
- [ ] Click "Admin" navigates to /admin (admin only)
- [ ] Hover effects work on all links
- [ ] Underline animation appears on hover

---

### 3. Login Page Testing (/login)

#### Visual Elements
- [ ] Login form centered on page
- [ ] Card has dark background with border
- [ ] Title "Welcome Back" displays
- [ ] Username and Password fields visible
- [ ] "Remember Me" checkbox present
- [ ] Login button styled with gradient
- [ ] "Don't have an account?" link visible
- [ ] Demo credentials box shows admin credentials

#### Form Validation
- [ ] Empty username shows error
- [ ] Empty password shows error
- [ ] Invalid credentials show error message
- [ ] Success message on valid login

#### Interactions
- [ ] Input fields focus with green glow
- [ ] Password field hides characters
- [ ] Login button hover effect works
- [ ] "Sign up" link navigates to /register
- [ ] Successful login redirects to home
- [ ] JWT token stored in localStorage
- [ ] User data stored in context

#### Test Credentials
```
Username: admin
Password: admin
```

---

### 4. Register Page Testing (/register)

#### Visual Elements
- [ ] Registration form centered
- [ ] All fields visible (Username, Email, Password, Confirm Password)
- [ ] Register button styled correctly
- [ ] "Already have an account?" link visible

#### Form Validation
- [ ] Empty fields show errors
- [ ] Invalid email format shows error
- [ ] Password mismatch shows error
- [ ] Short password shows error (if implemented)
- [ ] Success message on registration

#### Interactions
- [ ] All input fields focus properly
- [ ] Register button hover effect
- [ ] "Log in" link navigates to /login
- [ ] Successful registration auto-logs in user
- [ ] Redirects to home after registration

#### Test Registration
```
Username: testuser
Email: test@example.com
Password: password123
Confirm Password: password123
```

---

### 5. Profile Page Testing (/profile)

#### Visual Elements
- [ ] Profile header displays with avatar circle
- [ ] Avatar shows first letter of name/username
- [ ] User name and username display
- [ ] Role badge shows (Admin/User)
- [ ] Edit Profile button visible
- [ ] Statistics cards show (Playlists, Favorites, Watchlist)
- [ ] "My Playlists" section displays
- [ ] Empty state shows if no playlists

#### Edit Profile
- [ ] Click "Edit Profile" shows form
- [ ] Name field pre-filled with current name
- [ ] Bio field pre-filled with current bio
- [ ] Save Changes button works
- [ ] Cancel button hides form
- [ ] Success message on save
- [ ] Profile updates immediately

#### Playlists Section
- [ ] "Create Playlist" button visible
- [ ] Playlist cards display in grid
- [ ] Each card shows name, description, movie count
- [ ] Public/Private indicator shows
- [ ] Hover effect on playlist cards

#### Interactions
- [ ] Avatar circle has gradient background
- [ ] Stats cards have hover effect
- [ ] Edit form validates inputs
- [ ] Profile updates reflect immediately

---

### 6. News Page Testing (/news)

#### Visual Elements
- [ ] Page title "Latest Entertainment News" displays
- [ ] Subtitle shows
- [ ] News grid layout (3 columns on desktop)
- [ ] Each news card shows:
  - [ ] Image (if available)
  - [ ] Category badge
  - [ ] Title
  - [ ] Excerpt
  - [ ] Author and date
  - [ ] "Read More" button

#### Empty State
- [ ] Shows message if no news articles
- [ ] Displays newspaper icon
- [ ] "Check back soon" message

#### Interactions
- [ ] News cards have hover effect
- [ ] Cards lift on hover
- [ ] "Read More" button clickable
- [ ] Category badges styled correctly
- [ ] Responsive grid (1 column on mobile)

---

### 7. Chat Page Testing (/chat)

#### Visual Elements
- [ ] Chat header with title and subtitle
- [ ] Chat box with messages container
- [ ] Message input form at bottom
- [ ] Send button visible
- [ ] Empty state if no messages

#### Message Display
- [ ] Sent messages align right (green gradient)
- [ ] Received messages align left (gray background)
- [ ] Timestamps show for each message
- [ ] Messages scroll properly
- [ ] Container height fixed at 500px

#### Interactions
- [ ] Type in message input
- [ ] Send button disabled when empty
- [ ] Click Send or press Enter to send
- [ ] Message appears immediately
- [ ] Input clears after sending
- [ ] Scroll to bottom on new message
- [ ] Loading state while sending

#### Test Messages
```
"Hello, I need help with my account"
"Can you help me find a movie?"
"Thank you for your assistance"
```

---

### 8. Contact Page Testing (/contact)

#### Visual Elements
- [ ] Page title "Get in Touch" displays
- [ ] Two-column layout (info + form)
- [ ] Contact info cards on left:
  - [ ] Email card with icon
  - [ ] Phone card with icon
  - [ ] Location card with icon
- [ ] Contact form on right with all fields:
  - [ ] Name
  - [ ] Email
  - [ ] Subject
  - [ ] Message
  - [ ] Submit button

#### Form Validation
- [ ] Empty name shows error
- [ ] Invalid email shows error
- [ ] Empty subject shows error
- [ ] Empty message shows error
- [ ] Success message on submission

#### Interactions
- [ ] All input fields focus properly
- [ ] Textarea expands for message
- [ ] Submit button hover effect
- [ ] Form clears after submission
- [ ] Success alert displays
- [ ] Info cards have hover effect

#### Test Submission
```
Name: John Doe
Email: john@example.com
Subject: Website Feedback
Message: Great platform! Love the design.
```

---

### 9. Admin Dashboard Testing (/admin)

**Note:** Only accessible with admin credentials

#### Visual Elements
- [ ] Page title "Admin Dashboard" with crown icon
- [ ] Statistics cards show:
  - [ ] News Articles count
  - [ ] Contact Messages count
  - [ ] Active Chats count
- [ ] Quick Actions section with buttons:
  - [ ] Create News Article
  - [ ] Manage Users
  - [ ] View All Chats
  - [ ] Manage Movies
- [ ] Recent Contact Messages section
- [ ] Contact items display in list

#### Statistics
- [ ] Stats update with real data
- [ ] Icons display correctly
- [ ] Numbers are accurate

#### Contact Messages
- [ ] Shows last 5 messages
- [ ] Each message shows:
  - [ ] Name and date
  - [ ] Email
  - [ ] Subject (bold)
  - [ ] Message content
- [ ] Empty state if no messages

#### Interactions
- [ ] Stat cards have hover effect
- [ ] Action buttons clickable
- [ ] Contact items styled as cards
- [ ] Responsive layout on mobile

---

### 10. Movie Search Testing

#### Search Functionality
- [ ] Enter movie title in search bar
- [ ] Click search button
- [ ] Loading spinner appears
- [ ] Results display in grid
- [ ] Each movie card shows:
  - [ ] Poster image
  - [ ] Title
  - [ ] Year
  - [ ] Rating
  - [ ] Genre

#### Movie Card Interactions
- [ ] Hover shows overlay
- [ ] Action buttons appear on hover
- [ ] Add to playlist button works
- [ ] Add to favorites button works
- [ ] View details button works

#### Test Searches
```
"Avengers"
"The Matrix"
"Inception"
"Shawshank Redemption"
```

---

### 11. Authentication Flow Testing

#### Login Flow
1. [ ] Start at home page (logged out)
2. [ ] Click "Login" in navbar
3. [ ] Enter credentials
4. [ ] Click "Login"
5. [ ] Redirected to home
6. [ ] Navbar shows user greeting
7. [ ] Profile link appears
8. [ ] Logout button appears

#### Logout Flow
1. [ ] Click "Logout" button
2. [ ] Redirected to home
3. [ ] Navbar shows Login/Register
4. [ ] Profile link disappears
5. [ ] Token removed from localStorage

#### Protected Routes
- [ ] /profile redirects to /login when logged out
- [ ] /chat redirects to /login when logged out
- [ ] /admin redirects to / for non-admin users
- [ ] After login, redirects to intended page

---

### 12. Responsive Design Testing

#### Desktop (> 1200px)
- [ ] Full navbar with all links
- [ ] 5-column grid for production houses
- [ ] 3-column grid for news
- [ ] 3-column grid for movies
- [ ] Two-column contact layout

#### Tablet (768px - 1200px)
- [ ] Navbar still visible
- [ ] 3-4 column grids
- [ ] Readable text sizes
- [ ] Proper spacing

#### Mobile (< 768px)
- [ ] Navbar menu hidden (or hamburger)
- [ ] 1-2 column grids
- [ ] Stacked contact layout
- [ ] Larger touch targets
- [ ] Readable font sizes
- [ ] Profile header stacks vertically

---

### 13. Performance Testing

#### Load Times
- [ ] Home page loads < 2 seconds
- [ ] Images load progressively
- [ ] No layout shift during load
- [ ] Smooth animations (60fps)

#### Interactions
- [ ] Button clicks respond immediately
- [ ] Form submissions < 1 second
- [ ] Page transitions smooth
- [ ] No lag on hover effects

#### Network
- [ ] Works on slow 3G
- [ ] Handles API errors gracefully
- [ ] Shows loading states
- [ ] Retry mechanism works

---

### 14. Browser Compatibility Testing

#### Chrome
- [ ] All features work
- [ ] Animations smooth
- [ ] Styles render correctly

#### Firefox
- [ ] All features work
- [ ] Gradients display correctly
- [ ] Forms work properly

#### Safari
- [ ] All features work
- [ ] Webkit prefixes work
- [ ] Smooth scrolling works

#### Edge
- [ ] All features work
- [ ] Modern features supported
- [ ] No console errors

---

### 15. Error Handling Testing

#### Network Errors
- [ ] Backend down shows error message
- [ ] Failed API calls show error
- [ ] Retry button appears
- [ ] User-friendly error messages

#### Form Errors
- [ ] Validation errors display clearly
- [ ] Error messages are helpful
- [ ] Fields highlight in red
- [ ] Success messages are green

#### 404 Errors
- [ ] Invalid routes show 404 page
- [ ] "Go Home" button works
- [ ] Styled consistently

---

### 16. Accessibility Testing

#### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Enter key submits forms
- [ ] Escape key closes modals
- [ ] Focus indicators visible

#### Screen Reader
- [ ] Alt text on images
- [ ] ARIA labels on buttons
- [ ] Form labels associated
- [ ] Semantic HTML used

#### Color Contrast
- [ ] Text readable on backgrounds
- [ ] Meets WCAG AA standards
- [ ] Links distinguishable
- [ ] Focus states visible

---

## 🐛 Common Issues to Check

### CSS Issues
- [ ] No horizontal scrollbar
- [ ] No overlapping elements
- [ ] Consistent spacing
- [ ] Proper z-index layering

### JavaScript Errors
- [ ] No console errors
- [ ] No undefined variables
- [ ] Promises handled correctly
- [ ] Event listeners work

### API Integration
- [ ] CORS configured correctly
- [ ] Tokens sent in headers
- [ ] Error responses handled
- [ ] Loading states shown

---

## 📊 Testing Results Template

```
Date: [DATE]
Tester: [NAME]
Browser: [BROWSER + VERSION]
Device: [DEVICE]

✅ Passed: [COUNT]
❌ Failed: [COUNT]
⚠️ Issues: [COUNT]

Critical Issues:
1. [ISSUE]
2. [ISSUE]

Minor Issues:
1. [ISSUE]
2. [ISSUE]

Notes:
[ADDITIONAL NOTES]
```

---

## 🎯 Priority Testing Order

1. **Critical Path** (Must Work):
   - Home page loads
   - Login/Register works
   - Navigation works
   - Basic search works

2. **High Priority**:
   - Profile management
   - Chat functionality
   - Contact form
   - Admin dashboard

3. **Medium Priority**:
   - News display
   - Playlist management
   - Responsive design
   - Animations

4. **Low Priority**:
   - Advanced features
   - Edge cases
   - Browser compatibility
   - Performance optimization

---

## ✅ Sign-Off Checklist

Before considering testing complete:

- [ ] All critical features tested
- [ ] No blocking bugs found
- [ ] Responsive design verified
- [ ] Forms validate correctly
- [ ] Authentication works
- [ ] API integration works
- [ ] Error handling works
- [ ] Performance acceptable
- [ ] Accessibility basics covered
- [ ] Documentation updated

---

## 🚀 Ready for Production?

Once all tests pass:
1. Document any known issues
2. Create bug tickets for fixes
3. Update deployment documentation
4. Prepare for user acceptance testing
5. Plan production deployment

---

**Happy Testing! 🧪**
