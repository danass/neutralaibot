import time
import requests
import os
from classifier import CommentClassifier
from credentials import load_credentials, login
from notifications import list_mentions, mark_notifications_as_read
from reply import post_reply

def get_messages_content(pds_url, session_token, uris):
    try:
        response = requests.get(
            f"{pds_url}/xrpc/app.bsky.feed.getPosts",
            headers={"Authorization": f"Bearer {session_token}"},
            params={"uris": uris},
            timeout=10
        )
        response.raise_for_status()
        posts = response.json().get("posts", [])
        return {post["uri"]: {"text": post["record"]["text"], "author": post["author"]["handle"]} for post in posts}
    except requests.RequestException as error:
        print(f"Error fetching message content: {error}")
        return {}

def main():
    pds_url, handle, password = load_credentials()
    session = login(pds_url, handle, password)
    session_token = session["accessJwt"]
    repo = session["did"]
    
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    classifier = CommentClassifier(MISTRAL_API_KEY, rate_limit_delay=1.5)

    while True:
        try:
            mentions = list_mentions(pds_url, session_token)

            if not mentions:
                print("No new mentions found.")
            else:
                parent_uris = [mention['parent'] for mention in mentions if mention['parent']]
                root_uris = [mention['root'] for mention in mentions if mention['root']]
                uris = list(set(parent_uris + root_uris))

                if uris:
                    messages_content = get_messages_content(pds_url, session_token, uris)
                else:
                    messages_content = {}

                print("\nMentions:")
                for mention in mentions:
                    print(f"- Author: @{mention['author']}")
                    print(f"  Text: {mention['text']}")
                    print(f"  CID: {mention['cid']}")
                    print(f"  Indexed At: {mention['indexedAt']}")
                    print(f"  Parent: {mention['parent']}")
                    if mention['parent']:
                        parent_content = messages_content.get(mention['parent'], {}).get("text", "No content found")
                        parent_author = messages_content.get(mention['parent'], {}).get("author", "unknown")
                        print(f"  Parent Content: {parent_content}")
                        print(f"  Parent Author: {parent_author}")
                    print(f"  Root: {mention['root']}")
                    if mention['root']:
                        root_content = messages_content.get(mention['root'], {}).get("text", "No content found")
                        print(f"  Root Content: {root_content}")

                    # Classify the parent and root comments
                    classification = classifier.classify_comments(root_content, parent_content)

                    print(f"  Root Comment: {classification['root_comment']}")
                    print(f"  Parent Comment: {classification['parent_comment']}")
                    print(f"  Classification: {', '.join(classification['classification'])}")

                    # Post a reply with the classification result
                    # Calculate the fixed length of the parts that won't change (classification and author)
                    classification_text = f"Classification: {', '.join(classification['classification'])}\n"
                    author_text = f"by: @{parent_author}"

                    fixed_length = len(classification_text) + len(author_text)

                    # Calculate the remaining space for parent_content
                    remaining_length = 290 - fixed_length

                    # Trim parent_content to fit the remaining space, ensuring it doesn't exceed the limit
                    if remaining_length > 0:
                        if len(parent_content) > remaining_length:
                            parent_content = parent_content[:remaining_length - 3] + "..."  # Truncate and add ellipsis
                    else:
                        parent_content = ""  # In case the classification and author take up the full 300 chars

                    # Construct the reply text with the trimmed parent_content
                    reply_text = (
                        f"Comment: {parent_content}\n"
                        f"Classification: {', '.join(classification['classification'])}\n"
                        f"by: @{parent_author}"
                    )

                    post_reply(pds_url, session_token, repo, mention['root'], mention['cid'], mention['parent'], mention['cid'], reply_text)

                mark_notifications_as_read(pds_url, session_token)

            time.sleep(60)  # Wait for 60 seconds

        except KeyboardInterrupt:
            print("Program interrupted manually. Exiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(10)  # Wait before retrying

if __name__ == "__main__":
    main()