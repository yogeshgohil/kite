from kiteconnect import KiteConnect

api_key = "tw1tc6dl9940mwtu"
api_secret = "3mxljcytvzodgv1kfe8bsv6jjxwhklab"

kite = KiteConnect(api_key=api_key)

# Step 1: Open this link in your browser
print("Login URL:", kite.login_url())

request_token = "BKYLfkQrboF01pLgqjekyFENnFD30pzC"

data = kite.generate_session(request_token, api_secret=api_secret)
print("Your access token is:", data["access_token"])
