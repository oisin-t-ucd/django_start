This guide provides a step-by-step workflow to get your Django application sending emails from Render by setting up a Brevo account and integrating it via `django-anymail`.

---

## Step 1: Create and Configure your Brevo Account

Before writing code, you must set up your provider to ensure your emails are delivered successfully.

1. **Sign Up**: Go to [Brevo.com](https://www.brevo.com/) and create a free account.
2. **Verify your Account**: If you signed up using your Gmail account, your email is already verified as the account owner.
3. **Add Your Sender**: Even if your account is verified, you must explicitly add your email address as a "Sender" so Brevo knows you are authorized to use it.
* Navigate to **Senders & IP** in the Brevo dashboard (found under your profile menu).
* Go to the **Senders** tab.
* Add your Gmail address. If you didn't sign up with Gmail, you will receive a verification code at that address; enter it in Brevo to confirm ownership.


4. **Generate your API Key**:
* Click on your profile icon in the top right corner and select **SMTP & API**.
* Go to the **API Keys** tab.
* Click **Generate a new API key**, name it (e.g., "Django App"), and copy the key. Store this securely; you cannot see it again once you close the window.



---

## Step 2: Install Dependencies

In your local terminal, navigate to your project directory (ensure your virtual environment is active) and install `django-anymail`. Use quotes to ensure your terminal handles the brackets correctly:

```bash
pip install 'django-anymail[brevo]'

```

Update your `requirements.txt` file so Render installs this dependency during your next deployment:

```bash
pip freeze > requirements.txt

```

---

## Step 3: Configure `settings.py`

Open your `settings.py` file and update your configuration to use the Anymail backend.

```python

# Add 'anymail' to your installed apps
INSTALLED_APPS = [
    # ... your other apps
    'anymail',
]

# Set the email backend to Brevo
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"

# The email address you verified in Step 1
DEFAULT_FROM_EMAIL = "your-email@gmail.com"

# Brevo API configuration
ANYMAIL = {
    "BREVO_API_KEY": os.environ.get("BREVO_API_KEY"),
}

```

---

## Step 4: Manage Environment Variables

Keep your API key secure by using a local file for development and Render's dashboard for production.

### Local Development (`.env`)

Create a file named `.env` in the root of your project:

```text
BREVO_API_KEY=your_actual_api_key_from_brevo_dashboard

```

*Ensure your project is configured to load this file (e.g., using `python-dotenv`).*

### Production (Render)

1. Log in to your **Render Dashboard**.
2. Select your **Web Service**.
3. Click the **Environment** tab in the sidebar.
4. Under **Environment Variables**, click **Add Environment Variable**.
* **Key**: `BREVO_API_KEY`
* **Value**: Paste the API key you generated in the Brevo dashboard.


5. Click **Save Changes**. (Render will automatically re-deploy your app.)

---

## Step 5: Final Checklist

Before testing your password reset flow, verify the following:

* **Verified Sender**: Ensure the email address in `DEFAULT_FROM_EMAIL` matches the email you added/verified inside your Brevo "Senders" tab.
* **No IP Whitelisting**: Do not enable "Authorized IPs" for your API keys in the Brevo dashboard. Render uses dynamic IP addresses, and whitelisting will cause your app to be blocked.
* **Repo Update**: Ensure your `requirements.txt` and `settings.py` changes are committed to Git and pushed to your provider (GitHub/GitLab).

Once the deployment completes, your generic password reset views will automatically route emails through the Brevo API, bypassing the SMTP restrictions on Render's free tier.