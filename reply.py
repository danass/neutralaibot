import requests
from datetime import datetime, timezone

def post_reply_in_mention(pds_url, session_token, repo, mention, reply_text):
    # print("Mentioned:", mention)
    try:
        root_uri = mention.get('rooturi') or mention['uri']
        root_cid = mention.get('rootcid') or mention['cid']
        parent_uri = mention.get('parenturi') or mention['uri']
        parent_cid = mention.get('parentcid') or mention['cid']

        payload = {
            "repo": repo,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "reply": {
                    "root": {"uri": root_uri, "cid": root_cid},
                    "parent": {"uri": parent_uri, "cid": parent_cid}
                },
                "text": reply_text,
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
        }

        headers = {
            "Authorization": f"Bearer {session_token}",
            "Content-Type": "application/json"
        }
        print("Payload:", payload)
        print("Headers:", headers)
        
        response = requests.post(
            f"{pds_url}/xrpc/com.atproto.repo.createRecord",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        print("Reply posted successfully.")
    except requests.RequestException as error:
        print(f"Error posting reply: {error}")
        if error.response is not None:
            print("Response status code:", error.response.status_code)
            print("Response content:", error.response.content)