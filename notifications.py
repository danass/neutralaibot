import requests
from datetime import datetime, timezone

def mark_notifications_as_read(pds_url, session_token):
    try:
        seen_at = datetime.now(timezone.utc).isoformat()
        response = requests.post(
            f"{pds_url}/xrpc/app.bsky.notification.updateSeen",
            headers={"Authorization": f"Bearer {session_token}"},
            json={"seenAt": seen_at},
            timeout=10
        )
        response.raise_for_status()
        print("All notifications marked as read.")
    except requests.RequestException as error:
        print(f"Error marking notifications as read: {error}")

def list_mentions(pds_url, session_token):
    try:
        response = requests.get(
            f"{pds_url}/xrpc/app.bsky.notification.listNotifications",
            headers={"Authorization": f"Bearer {session_token}"},
            params={"limit": 50},
            timeout=10
        )
        response.raise_for_status()
        notifications = response.json().get("notifications", [])
        print(f"Fetched {len(notifications)} notifications.")

        mentions = [
            {
                "cid": notif.get("cid"),
                "author": notif.get("author", {}).get("handle"),
                "text": notif.get("record", {}).get("text"),
                "indexedAt": notif.get("indexedAt"),
                "parent": notif.get("record", {}).get("reply", {}).get("parent", {}).get("uri"),
                "root": notif.get("record", {}).get("reply", {}).get("root", {}).get("uri"),
            }
            for notif in notifications
            if notif.get("reason") == "mention" and not notif.get("isRead", False)
        ]

        print(f"Found {len(mentions)} mentions.")
        return mentions

    except requests.RequestException as error:
        print(f"Error fetching notifications: {error}")
        return []