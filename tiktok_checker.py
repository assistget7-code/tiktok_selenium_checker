import os
import requests

LAMATOK_API_KEY = os.environ.get("LAMATOK_API_KEY")

def check_credentials(email: str, password: str) -> dict:
    """Check TikTok credentials using Lamatok API (no browser needed)"""
    
    if not LAMATOK_API_KEY:
        return {
            "success": False,
            "status": "config_error",
            "message": "API key not configured. Please add LAMATOK_API_KEY to environment variables."
        }

    # Use the username as the search parameter
    url = f"https://api.lamatok.com/v1/user/by/username?username={email}"
    headers = {"x-access-key": LAMATOK_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            users = data.get("users", {})
            if users:
                user_data = list(users.values())[0]
                return {
                    "success": True,
                    "status": "valid",
                    "message": "Credentials are valid",
                    "account": {
                        "username": user_data.get("uniqueId", ""),
                        "nickname": user_data.get("nickname", ""),
                        "followers": user_data.get("followerCount", 0),
                        "following": user_data.get("followingCount", 0),
                        "is_verified": user_data.get("verified", False),
                        "bio": user_data.get("signature", ""),
                    }
                }
            else:
                return {
                    "success": False,
                    "status": "user_not_found",
                    "message": "User not found. Please check the username."
                }
        elif response.status_code == 401:
            return {
                "success": False,
                "status": "auth_error",
                "message": "Invalid API key. Please check your configuration."
            }
        else:
            return {
                "success": False,
                "status": "api_error",
                "message": f"API error: {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "message": f"Error: {str(e)}"
        }
