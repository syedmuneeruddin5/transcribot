## Feature

Add Support for openrouter for generating captions based on transcription. Gives users the access to change the model, whether to allow all models or only free models. Give the users the option to save the API key in .env file. Give the users option to copy the generated caption to clipboard.

## Implementation

- Make changes in settings.json and default_setting.json and add:
    - Open Router Model (set to default "deepseek/deepseek-r1-0528:free" model)
    - Only Free Model (set to default to true)
    - Prompt : set default to ""