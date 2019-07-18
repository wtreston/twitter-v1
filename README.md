# twitter (Tréter)

A Python based Twitter monitor which features include:

- When a targetted user tweets the monitor will pick up on it.
    - All users tagged within a tweet have their bio and bio url checked.
    - Any links within the tweet are extracted and displayed in their full form instead of twitter's shorter form.
    - If the tweet quotes another tweet, both the tweet and the quoted tweet have their content checked for user mentions and       links. The poster of the quoted tweet has their bio checked.
- When a targetted user changes their bio or bio url the monitor will pick up the change.
- :soon: If a retweeted tweet contains a link users will be notified - otherwise.
- :soon: Discord Invite URLs will be extracted from the tweets using regex.
- :soon: Discord Bot integration.
    - Can add and remove users you're monitoring via a Discord Bot.
    - Can add and remove webhook URLS you wish to send to.
        - Can send the notification to multiple webhooks.
- :question: Check for keywords (password/pw etc.) and generate complete password link for user to click on.

Made with :heart: by Will.
