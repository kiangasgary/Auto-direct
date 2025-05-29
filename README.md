# Instagram DM Automation Tool

An automated Instagram Direct Message (DM) sender for business outreach that sends personalized messages to target accounts based on their business category.

## Features

- 🔄 Automated Instagram DM sending
- 📊 Category-based message templating
- 🔒 Safe and compliant with Instagram's limits
- 📝 Detailed logging and tracking
- ⚡ Rate limiting and anti-spam measures
- 🔐 Secure credential management

## Prerequisites

- Python 3.10 or higher
- Instagram Business Account
- Windows 10/11, macOS 12+, or Linux

## Installation

1. Clone the repository:
```powershell
git clone https://github.com/yourusername/auto-direct.git
cd auto-direct
```

2. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Set up environment variables:
```powershell
Copy-Item .env.example .env
```
Then edit the `.env` file with your credentials and settings.

## Usage

1. Prepare your user list:
   - Create a CSV file in the `data` folder named `users.csv`
   - Format: `username,category,status`

2. Configure message templates:
   - Edit `data/message_templates.json`
   - Create templates for each business category

3. Run the application:
```powershell
python main.py send-messages
```

## Command Line Options

```
Commands:
  send-messages    Start sending DMs to users
  show-stats       Display sending statistics
  clear-logs       Clear log files
  test-connection  Test Instagram connection
```

## Safety Features

- Random delays between messages (30-90 seconds)
- Daily message limit (default: 50)
- Session persistence
- Automatic pause on suspicious activity
- Proxy support

## Logging

Logs are stored in the `logs` directory:
- `app.log`: Application logs
- `sent_log.csv`: Message sending history

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for legitimate business communication only. Users are responsible for complying with Instagram's Terms of Service and applicable laws regarding automated messaging. 