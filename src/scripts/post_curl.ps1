Invoke-RestMethod -Uri http://localhost:11434/api/chat -Method Post -ContentType "application/json" -Body '{
    "model": "deepseek-r1:14b",
    "messages": [
        {
            "role": "user",
            "content": "who wrote the book godfather?"
        }
    ],
    "stream": false
}'