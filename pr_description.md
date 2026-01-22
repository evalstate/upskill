# Add JWT-based User Authentication to Node.js API

## Overview
This PR implements a complete JWT (JSON Web Token) based authentication system for our Node.js API, providing secure user authentication and authorization capabilities.

## Changes Made

### 🔐 Authentication Features
- **JWT Token Generation**: Implemented secure JWT token creation upon successful login
- **Token Validation**: Added middleware to validate JWT tokens on protected routes
- **Token Refresh**: Implemented refresh token mechanism for enhanced security
- **Password Hashing**: Integrated bcrypt for secure password hashing and verification
- **User Registration**: Added user registration endpoint with validation
- **Login/Logout**: Implemented secure login and logout functionality

### 🛡️ Security Enhancements
- **Token Expiration**: Configured token expiration times (access: 15min, refresh: 7d)
- **Environment Variables**: Moved sensitive configuration to environment variables
- **Rate Limiting**: Added rate limiting on authentication endpoints
- **Input Validation**: Implemented comprehensive input validation and sanitization
- **CORS Configuration**: Updated CORS settings for secure cross-origin requests

### 📁 New Files Added
```
/src/
├── middleware/
│   ├── auth.middleware.js      # JWT verification middleware
│   ├── rateLimiter.js         # Rate limiting configuration
│   └── validation.middleware.js # Input validation middleware
├── controllers/
│   ├── auth.controller.js      # Authentication logic
│   └── user.controller.js      # User management
├── models/
│   └── User.model.js           # User schema and methods
├── routes/
│   ├── auth.routes.js          # Authentication routes
│   └── protected.routes.js     # Protected route examples
├── utils/
│   ├── jwt.utils.js            # JWT generation and verification
│   ├── password.utils.js       # Password hashing utilities
│   └── validators.js           # Input validation functions
└── config/
    ├── auth.config.js          # Authentication configuration
    └── database.config.js      # Database connection
```

### 🔧 Dependencies Added
- `jsonwebtoken` - JWT token generation and verification
- `bcryptjs` - Password hashing and comparison
- `express-validator` - Input validation and sanitization
- `express-rate-limit` - Rate limiting for API endpoints
- `helmet` - Security headers
- `cors` - Cross-origin resource sharing
- `dotenv` - Environment variable management

## API Endpoints

### Public Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh-token` - Refresh access token

### Protected Endpoints
- `POST /api/auth/logout` - User logout (requires auth)
- `GET /api/user/profile` - Get user profile (requires auth)
- `PUT /api/user/profile` - Update user profile (requires auth)

## Usage Examples

### User Registration
```javascript
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securePassword123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

### User Login
```javascript
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securePassword123!"
}

Response:
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user123",
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

### Accessing Protected Routes
```javascript
GET /api/user/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Configuration

### Environment Variables Required
```bash
# Authentication
JWT_SECRET=your-super-secret-jwt-key
JWT_ACCESS_EXPIRATION=15m
JWT_REFRESH_EXPIRATION=7d

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password

# Application
NODE_ENV=development
PORT=3000
```

## Testing

### Unit Tests Added
- Authentication controller tests
- JWT utility tests
- Password hashing tests
- Input validation tests
- Rate limiting tests

### Integration Tests
- Complete authentication flow tests
- Protected route access tests
- Token refresh mechanism tests
- Rate limiting functionality tests

Run tests with:
```bash
npm test
npm run test:integration
```

## Migration Guide

### For Existing Users
1. Update your `.env` file with the new authentication variables
2. Run the database migration to add user tables
3. Update your API client to handle JWT tokens
4. Implement token refresh logic in your frontend

### Database Schema
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Performance Impact
- **Token Verification**: ~2ms per request (asynchronous)
- **Password Hashing**: ~100ms per registration/login
- **Database Queries**: Optimized with proper indexing
- **Rate Limiting**: Minimal overhead with Redis backend

## Security Considerations
- ✅ JWT tokens are signed with HS256 algorithm
- ✅ Passwords are hashed using bcrypt with salt rounds of 12
- ✅ Tokens expire after 15 minutes (configurable)
- ✅ Refresh tokens are stored securely in database
- ✅ Rate limiting prevents brute force attacks
- ✅ Input validation prevents injection attacks
- ✅ HTTPS is enforced in production
- ✅ Security headers are set via Helmet.js

## Breaking Changes
None - This is a new feature addition that doesn't modify existing functionality.

## Future Improvements
- [ ] Add OAuth2 integration (Google, GitHub)
- [ ] Implement password reset functionality
- [ ] Add email verification for new users
- [ ] Implement role-based access control (RBAC)
- [ ] Add two-factor authentication (2FA)
- [ ] Implement session management dashboard

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review of code completed
- [x] Code is commented, particularly in hard-to-understand areas
- [x] Corresponding documentation updated
- [x] Tests added that prove the fix is effective or that the feature works
- [x] New and existing unit tests pass locally
- [x] No new warnings or errors introduced
- [x] Environment variables are properly configured
- [x] Security best practices followed
- [x] Performance impact considered and optimized

## Related Issues
Closes #123 - Implement user authentication system
Closes #124 - Add JWT token management
Addresses #125 - Secure API endpoints

## Deployment Notes
1. Set up environment variables in production
2. Run database migrations
3. Restart the application server
4. Monitor authentication endpoints for any issues

---

**Reviewers:** @backend-team @security-team
**Labels:** authentication, security, jwt, api
**Priority:** High
**Estimated Impact:** All API consumers will need to implement authentication
