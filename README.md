# Akkiai_crew

This branch v6 updated on 29th January 2025.

NEW UPDATE-- Cached inputs into local and used a custom tool to fetch cached inputs -Crew 1&2

1. Added crew 1-9 for production
2. Output pydantic only done for crew 1 and 9, have to do for others
3. updated the directory of codes
4. Inputs limited only to STARTUP_INFO
5. updated the main.py with orchestration of crew runs
6. Added CHAT endpoint with anthropic API stateless
7. Text preprocessing to remove unwanted spaces or characters and passed that processed text to other llm to re validate the json format
