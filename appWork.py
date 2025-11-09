from openai import OpenAI

# Replace this with your actual API key
client = OpenAI(api_key="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")

file = client.files.create(
    file=open("feedback.json", "rb"),
    purpose="assistants"
)

print("✅ File uploaded successfully!")
print("File ID:", file.id)
