# Avery's Riddle Me This?

A fun, interactive riddle game for kids built with Streamlit and powered by Meta AI's Llama 3.2 model. Solve riddles, stump the AI with your own riddles, or chat with a friendly AI assistant in multiple languages! 🎉

**Built with Meta Llama 3**

## Features
- **Solve Riddles**: Choose from Easy, Medium, or Hard riddles, with dynamic generation using Llama-3.2-3B-Instruct.
- **Stump the AI**: Challenge the AI with your own riddles.
- **Chat with AI**: Ask for hints or have fun conversations in a child-friendly environment.
- **Multilingual Support**: Play in English, Spanish, French, German, Italian, Portuguese, Hindi, or Thai.
- **Text-to-Speech**: Hear AI responses aloud.
- **Safety First**: Uses Llama Guard to ensure all inputs and outputs are safe for kids.

## Prerequisites
- **Python**: Version 3.9 or higher.
- **Hugging Face Account**: Required for accessing the Llama-3.2-3B-Instruct and Llama-Guard-3-8B models.
- **Hardware**: 
  - Minimum: Intel Core i5 (10th Gen or equivalent), 16 GB RAM, 10 GB free disk space.
  - Recommended for local execution: CPU with 4+ cores, 16 GB+ RAM.
- **Internet Connection**: Required for Hugging Face Inference API (optional if running models locally).

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd averys-riddle-me-this
#### Notes on the `README.md`
- **License Compliance**: Includes the required “Built with Meta Llama 3” acknowledgment in multiple places (project description, footer, and license section).
- **Setup Instructions**: Guides users on installing dependencies, configuring the Hugging Face token, and running or deploying the app.
- **Usage**: Explains how to play the game and use its features.
- **Troubleshooting**: Addresses common issues like memory constraints and API errors, tailored to your CPU-based setup.

#### Additional Files
No additional license files are strictly required beyond the `README.md`, as the Llama 3.2 Community License is referenced via the link in the `README.md`. However, you may optionally include a `LICENSE` file for clarity:

**LICENSE** (optional):
```text
Avery's Riddle Me This? is built with Meta Llama 3.2, licensed under the Llama 3.2 Community License Agreement. See https://llama.meta.com/responsible-use-guide for details.

The source code of this project is licensed under the MIT License:

MIT License

Copyright (c) 2025 ijones90002

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
