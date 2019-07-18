# twitter (Tréter)

A Python based Twitter monitor which features include:

- When a targetted user tweets the monitor will pick up on it.
    - All users tagged within a tweet have their bio and bio url checked.
    - Any links within the tweet are extracted and displayed in their full form instead of twitter's shorter form.
    - If the tweet quotes another tweet, both the tweet and the quoted tweet have their content checked for user mentions and       links. The poster of the quoted tweet has their bio checked.
- When a targetted user changes their bio or bio url the monitor will pick up the change.

Made with :heart: by Will.
