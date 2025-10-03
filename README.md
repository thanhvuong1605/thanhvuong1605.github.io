# Personal Website - Interactive Terminal

A fully interactive terminal-style personal website inspired by [https://sdsa.ai/](https://sdsa.ai/).

## Features

- 🖥️ **Interactive Terminal** - Type commands anywhere on the page
- ⌨️ **Keyboard Input** - Real-time command input with visual feedback
- ✨ **Blinking Cursor** - Authentic terminal feel
- 📝 **Command History** - See all your previous commands
- 🎨 **Minimalist Design** - Dark gradient background with clean typography
- 📱 **Fully Responsive** - Works on all devices
- ⚡ **Tab Autocomplete** - Press Tab to autocomplete commands

## Available Commands

Type any of these commands:

- `about` - Learn about what you're building
- `jobs` - View open positions
- `who` - Meet the team
- `ls` - List all available commands
- `help` - Show help message with all commands
- `clear` - Clear the terminal

## How to Use

1. **Open the website** - Simply open `index.html` in your browser
2. **Start typing** - Click anywhere and start typing commands
3. **Press Enter** - Execute the command
4. **Click links** - Click on the orange links to execute commands instantly
5. **Tab completion** - Start typing a command and press Tab to autocomplete

## Customization

### Update Your Content

Edit `script.js` to customize the command responses:

```javascript
const commands = {
    about: `
        <div class="command-output">
            <p>Your custom about text here</p>
        </div>
    `,
    jobs: `
        <div class="command-output">
            <p>Your custom jobs information here</p>
        </div>
    `,
    // Add more commands...
};
```

### Change the Headline

Edit `index.html` (line 18):

```html
<h1 class="headline">Your custom headline here<br>second line optional.</h1>
```

### Modify the Terminal Path

Edit both `index.html` and `script.js` to change `/dev/agents` to your custom path:

```html
<span class="prompt-path">/your/custom/path</span>
```

### Customize Colors

Edit `styles.css`:

```css
/* Background gradient */
background: linear-gradient(135deg, #2d3436 0%, #3a4a4a 100%);

/* Link and cursor color */
color: #ff6b6b;  /* Change to your preferred color */

/* Text color */
color: #ffffff;

/* Prompt color */
color: #9ca3af;
```

### Add New Commands

In `script.js`, add new commands to the `commands` object:

```javascript
const commands = {
    // existing commands...
    blog: `
        <div class="command-output">
            <p>Check out my latest blog posts:</p>
            <p>• <a href="#">Post title 1</a></p>
            <p>• <a href="#">Post title 2</a></p>
        </div>
    `,
    contact: `
        <div class="command-output">
            <p>Get in touch:</p>
            <p>Email: <a href="mailto:you@example.com">you@example.com</a></p>
        </div>
    `
};
```

## Project Structure

```
personal_web/
├── index.html      # Main HTML structure
├── styles.css      # Styling and animations
├── script.js       # Interactive terminal logic
└── README.md       # This file
```

## Technical Details

### Keyboard Handling
- Captures all keyboard input globally
- Displays characters in real-time
- Backspace support
- Tab autocomplete
- Enter to execute commands

### Command Execution
- Validates commands against available list
- Displays command output
- Shows error for invalid commands
- Maintains command history
- Auto-scrolls to latest output

### Special Features
- Click anywhere to focus terminal
- Links are clickable and execute commands
- `clear` command resets terminal
- Tab autocomplete for faster typing
- Blinking cursor animation

## Browser Support

Works on all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Deployment

### GitHub Pages
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-repo-url
git push -u origin main
```

Then enable GitHub Pages in repository settings.

### Netlify
Drag and drop the `personal_web` folder to [Netlify](https://app.netlify.com/drop).

### Vercel
```bash
npm i -g vercel
vercel
```

## Tips for Customization

1. **Keep it simple** - The beauty is in the minimalism
2. **Use concise text** - Terminal-style works best with brief, clear information
3. **Add relevant links** - Include links to your GitHub, LinkedIn, etc.
4. **Test commands** - Make sure all your commands work properly
5. **Update regularly** - Keep your content fresh and relevant

## Inspiration

Design and functionality inspired by [sdsa.ai](https://sdsa.ai/) - a beautiful example of terminal-style web design.

---

Built with HTML, CSS, and JavaScript
