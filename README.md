# 🏛️ Kratos' Autobot - Internship Hunter

> *"By the rage of Kratos and the wisdom of Mimir"* ⚔️

An automated internship application bot with a God of War inspired dashboard that hunts for paid internships and sends personalized applications via email.

## 🌟 Features

- **Automated Job Scraping**: Searches for paid internships on Indeed with Cloudflare bypass
- **Smart Application Tracking**: SQLite database prevents duplicate applications
- **Personalized Cover Letters**: Jinja2 templating with keyword extraction
- **Gmail Integration**: Automated email sending via Gmail API
- **Proxy Rotation**: Free proxy support for enhanced scraping
- **Epic Dashboard**: Two God of War themed dashboards for monitoring
- **Mobile Responsive**: Works seamlessly on mobile devices

## 🏗️ Project Structure

```
kratos-autobot/
├── src/
│   ├── main.py              # Main application entry point
│   ├── scraper.py           # Web scraping with Selenium
│   ├── emailer.py           # Gmail API integration
│   ├── coverletter.py       # Cover letter generation
│   ├── db.py               # Database operations
│   └── proxy_manager.py    # Proxy management
├── dashboard/
│   ├── index.html          # Epic dashboard v1
│   ├── index2.html         # Clean dashboard v2
│   └── script.js           # Dashboard JavaScript
├── templates/
│   └── cover_letter_template.j2  # Cover letter template
├── config/
│   ├── .env               # Environment variables
│   └── proxies.txt        # Proxy list (auto-populated)
├── data/
│   └── applications.db    # SQLite database (auto-created)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Chrome/Chromium browser
- ChromeDriver
- Gmail account with API access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kratos-autobot.git
   cd kratos-autobot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Gmail API
   - Create credentials (OAuth 2.0 Client ID)
   - Download `credentials.json` and place in `config/` folder

4. **Install ChromeDriver**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install chromium-chromedriver
   
   # macOS
   brew install chromedriver
   
   # Windows - Download from https://chromedriver.chromium.org/
   ```

5. **Configure settings**
   ```bash
   # Edit templates/cover_letter_template.j2 with your details
   # Customize skills and experience in src/coverletter.py
   ```

### Running the Bot

**Direct Python execution:**
```bash
python src/main.py
```

**Using Docker:**
```bash
docker build -t kratos-autobot .
docker run -v $(pwd)/config:/app/config -v $(pwd)/data:/app/data kratos-autobot
```

### Dashboard Access

Open either dashboard in your browser:
- **Epic Dashboard**: `dashboard/index.html` - Full God of War theme with animations
- **Clean Dashboard**: `dashboard/index2.html` - Minimalist GoW inspired design

## 📋 Requirements

```txt
selenium==4.15.0
beautifulsoup4==4.12.2
requests==2.31.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
jinja2==3.1.2
sqlite3
```

## ⚙️ Configuration

### Cover Letter Customization

Edit `templates/cover_letter_template.j2`:
```jinja2
Dear {{ company }} Hiring Team,

I am excited to apply for the {{ job_title }} internship at {{ company }}. 
Your focus on {{ keyword }} aligns with my skills in {{ skills }} and 
passion for {{ industry }}.

# Customize these variables in src/coverletter.py:
- skills: Your technical skills
- industry: Target industry
- experience: Your relevant experience
```

### Environment Variables

Create `config/.env`:
```bash
# Gmail API settings (if needed)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret

# Scraping settings
MAX_APPLICATIONS_PER_RUN=50
DELAY_BETWEEN_APPLICATIONS=5
```

### Proxy Configuration

The bot automatically fetches free proxies from free-proxy-list.net. For premium proxies, modify `src/proxy_manager.py`.

## 🎮 Dashboard Features

### Epic Dashboard (`index.html`)
- Animated runes background
- Pulsing status indicators
- God of War themed styling
- Real-time statistics
- Recent battles log
- Floating animations

### Clean Dashboard (`index2.html`)
- Minimalist design
- Better mobile compatibility
- Subtle GoW theming
- Cleaner typography
- Professional appearance

### Dashboard Controls
- **⚔️ UNLEASH KRATOS**: Start the bot
- **🛡️ RECALL KRATOS**: Stop the bot
- **🐦 TEST RAVEN MESSAGE**: Test email functionality

## 🗄️ Database Schema

```sql
CREATE TABLE applications (
    job_id TEXT PRIMARY KEY,
    company TEXT,
    email TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Advanced Usage

### Custom Job Sources

Extend `src/scraper.py` to add more job boards:
```python
def search_linkedin_internships():
    # LinkedIn scraping logic
    pass

def search_glassdoor_internships():
    # Glassdoor scraping logic
    pass
```

### Enhanced Email Templates

Add multiple templates in `templates/`:
- `cover_letter_tech.j2` - For tech companies
- `cover_letter_finance.j2` - For finance companies
- `cover_letter_startup.j2` - For startups

### WhatsApp Notifications

Integrate with WhatsApp API for status updates:
```python
# Add to src/main.py
def send_whatsapp_update(message):
    # WhatsApp API integration
    pass
```

## 🚨 Important Disclaimers

### Legal & Ethical Use
- **Respect Rate Limits**: The bot includes delays to avoid overwhelming servers
- **Follow ToS**: Ensure compliance with job board terms of service
- **Quality Applications**: Review and customize cover letters for each company
- **Email Limits**: Gmail API has daily sending limits

### Anti-Detection Features
- User agent rotation
- Random delays between requests
- Proxy rotation
- Headless browsing
- Cloudflare handling (basic)

## 🐛 Troubleshooting

### Common Issues

**ChromeDriver not found:**
```bash
# Add ChromeDriver to PATH or specify location
export PATH=$PATH:/path/to/chromedriver
```

**Gmail API quota exceeded:**
- Wait 24 hours for quota reset
- Use multiple Gmail accounts
- Implement exponential backoff

**Cloudflare blocking:**
- The bot includes basic Cloudflare handling
- Consider using residential proxies
- Add longer delays between requests

**Proxy timeouts:**
```python
# Increase timeout in src/scraper.py
driver.set_page_load_timeout(30)
```

## 📊 Monitoring & Analytics

### View Statistics
```python
# Connect to database
import sqlite3
conn = sqlite3.connect('data/applications.db')
cursor = conn.cursor()

# Get success rate
cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'Sent' THEN 1 ELSE 0 END) as successful,
        ROUND(AVG(CASE WHEN status = 'Sent' THEN 1.0 ELSE 0.0 END) * 100, 2) as success_rate
    FROM applications
""")
```

### Logs Location
- Application logs: Console output
- Database: `data/applications.db`
- Email status: Stored in database

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black src/
isort src/
```

## 🛡️ Security Considerations

- Store credentials securely (never commit `credentials.json`)
- Use environment variables for sensitive data
- Regularly rotate API keys
- Monitor for suspicious activity
- Keep dependencies updated

## 📈 Performance Tips

- Use SSD for database storage
- Implement connection pooling
- Cache proxy validation
- Batch database operations
- Monitor memory usage

## 🔄 Updates & Maintenance

### Regular Maintenance
- Update ChromeDriver monthly
- Refresh proxy lists weekly
- Monitor job board changes
- Update selectors if sites change
- Review and improve cover letter templates

### Version History
- v1.0.0 - Initial release with basic functionality
- v1.1.0 - Added dashboard interface
- v1.2.0 - Improved Cloudflare handling
- v1.3.0 - Added proxy rotation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kratos-autobot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kratos-autobot/discussions)
- **Email**: workadit2@gmail.com

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- God of War series for the epic theme inspiration
- Free proxy providers for enabling scraping
- Open source community for excellent libraries
- Job seekers everywhere - may Kratos bring you victory! ⚔️

---

*"The warrior's path is never easy, but with Kratos' rage and modern automation, even the gods of corporate hiring cannot stand in our way!"* 

**Happy Job Hunting!** 🏆