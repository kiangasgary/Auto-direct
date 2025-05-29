# Instagram DM Automation - Product Requirements Document (PRD)

## 1. Project Overview
An automated Instagram Direct Message (DM) sender for business outreach that sends personalized messages to target accounts based on their business category.

### 1.1 Objective
Create a reliable, safe, and efficient Python-based automation tool that can handle bulk Instagram DM outreach while respecting platform limitations and maintaining a human-like interaction pattern.

### 1.2 Target Users
- Digital marketing teams
- Business development representatives
- Social media managers

## 2. Technical Specifications

### 2.1 Technology Stack
- **Programming Language:** Python 3.10+
- **Core Libraries:**
  - `instagrapi`: Instagram API client
  - `pandas`: Data manipulation and CSV handling
  - `openpyxl`: Excel file support
  - `logging`: System logging
  - `python-dotenv`: Environment variable management
  - `typer`: CLI interface
  - `rich`: Enhanced terminal output

### 2.2 System Architecture
```
auto-direct/
├── src/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── instagram_client.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── user_loader.py
│   │   └── message_templates.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── dm_sender.py
│   │   └── rate_limiter.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── validators.py
├── data/
│   ├── users.csv
│   └── message_templates.json
├── logs/
│   └── sent_log.csv
├── tests/
│   └── __init__.py
├── .env.example
├── requirements.txt
├── README.md
└── main.py
```

## 3. Functional Requirements

### 3.1 Core Features

#### User Data Management
- Load user data from CSV/Excel files
- Required columns: username, business_category
- Validate data format and structure
- Handle duplicate entries

#### Message Template System
- Category-based message templates
- Support for multiple languages (Persian/English)
- Template variables for personalization
- Template validation and formatting

#### Instagram Authentication
- Secure credential management via environment variables
- Session persistence
- Auto-retry on connection issues
- Proxy support (optional)

#### DM Sending System
- Rate limiting and delay mechanism
- Random delays between messages (30-90 seconds)
- Daily sending limits (max 50 messages/day)
- Anti-spam measures

#### Logging and Monitoring
- Detailed activity logging
- Success/failure tracking
- Error reporting
- Statistics generation

### 3.2 Safety Features
- Rate limiting compliance with Instagram limits
- Session rotation
- IP rotation support (via proxies)
- Account activity monitoring
- Automatic pause on suspicious activity

## 4. Data Structures

### 4.1 Input File Format (users.csv)
```csv
username,category,status
business_account1,fashion,pending
business_account2,cosmetics,pending
```

### 4.2 Output Log Format (sent_log.csv)
```csv
timestamp,username,category,status,message_template,error
2024-03-20 14:30:00,business_account1,fashion,success,template1,null
2024-03-20 14:31:30,business_account2,cosmetics,failed,template2,rate_limit
```

## 5. Error Handling

### 5.1 Error Categories
- Authentication errors
- Rate limiting errors
- Network errors
- Data validation errors
- Instagram API errors
- Account blocking detection

### 5.2 Recovery Procedures
- Automatic retry for temporary failures
- Session refresh on authentication issues
- Graceful shutdown on critical errors
- Data checkpoint system

## 6. Performance Requirements

### 6.1 System Limits
- Maximum 50 messages per day
- Minimum 30-second delay between messages
- Maximum 500 users per input file
- Maximum 5 retry attempts per message

### 6.2 Resource Usage
- Maximum memory usage: 512MB
- CPU usage: Low to moderate
- Disk space: < 1GB for logs and data

## 7. Security Requirements

### 7.1 Authentication
- Secure credential storage
- No plaintext passwords
- Session token encryption
- Proxy credential protection

### 7.2 Data Protection
- Local data encryption
- Secure log file handling
- No sensitive data in logs
- Regular data cleanup

## 8. Deployment Requirements

### 8.1 Installation
- Python 3.10+ environment
- Virtual environment support
- Dependencies management via pip
- Configuration via .env file

### 8.2 Operating System Support
- Windows 10/11
- macOS 12+
- Linux (Ubuntu 20.04+)

## 9. Maintenance and Support

### 9.1 Monitoring
- Daily activity logs
- Error rate monitoring
- Success rate tracking
- Performance metrics

### 9.2 Updates
- Regular dependency updates
- Instagram API compatibility checks
- Security patches
- Feature enhancements

## 10. Compliance and Limitations

### 10.1 Instagram Policies
- Respect daily message limits
- Maintain human-like behavior
- No spam or harassment
- Content guidelines compliance

### 10.2 Legal Requirements
- Data protection compliance
- User consent requirements
- Privacy policy compliance
- Terms of service adherence 